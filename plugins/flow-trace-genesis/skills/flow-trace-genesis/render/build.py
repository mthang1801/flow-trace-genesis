#!/usr/bin/env python3
"""build.py — md-source → self-contained HTML cho cẩm nang flow-trace.

Usage:  python3 .agents/skills/flow-trace/render/build.py docs/flows/<slug>
        (doc-folder là đường dẫn tương đối cwd hoặc tuyệt đối)

Reads  <doc-folder>/_doc.yml  +  <doc-folder>/NN-slug.md
Writes <doc-folder>.html  (self-contained: tokens.css + engine.js inline, KHÔNG CDN/font link)

Phỏng theo scripts/build.py của mAIvt, đã cắt phần Obsidian bridge / KB / DSA và
thêm highlight TypeScript (workspace Lending là NestJS/React).
"""
import os, re, sys, json, html as _html

try:
    import yaml
except ImportError:
    sys.exit("cần PyYAML: pip install pyyaml (hoặc python3 -m pip install --user pyyaml)")

RENDER = os.path.dirname(os.path.abspath(__file__))

def esc(s): return _html.escape(s, quote=False)

# ─────────────────────────── syntax highlighter ───────────────────────────
SQL_KW = set("""SELECT FROM WHERE INSERT INTO UPDATE DELETE CREATE OR REPLACE FUNCTION PROCEDURE
RETURNS RETURN BEGIN END DECLARE IF THEN ELSE ELSIF LOOP FOR WHILE RAISE EXCEPTION WHEN
LANGUAGE AS IN OUT AND NOT NULL IS JOIN LEFT RIGHT FULL INNER OUTER CROSS LATERAL ON
WITH RECURSIVE UNION INTERSECT EXCEPT ALL ANY GROUP BY ORDER HAVING LIMIT OFFSET VALUES SET TABLE VIEW
MATERIALIZED INDEX TRIGGER BEFORE AFTER EACH ROW EXECUTE USING PERFORM CALL DO COMMIT ROLLBACK
TRANSACTION ISOLATION LEVEL SERIALIZABLE REPEATABLE READ COMMITTED DISTINCT CASE COALESCE
NULLIF DEFAULT PRIMARY KEY FOREIGN REFERENCES CONSTRAINT CHECK UNIQUE GRANT REVOKE
VACUUM ANALYZE EXPLAIN TRUNCATE ALTER DROP ADD COLUMN RENAME TO
CASCADE ASC DESC NULLS FIRST LAST OVER PARTITION WINDOW FILTER RETURNING CONFLICT
NOTHING LOCK SHARE MODE EXCLUSIVE CONCURRENTLY TYPE CAST LIKE ILIKE BETWEEN EXISTS ARRAY""".split())
SQL_TP = set("""INT INTEGER INT4 INT8 BIGINT SMALLINT TEXT VARCHAR CHAR BOOLEAN BOOL
NUMERIC DECIMAL REAL DOUBLE PRECISION FLOAT TIMESTAMP TIMESTAMPTZ DATE TIME INTERVAL UUID JSON JSONB
BYTEA SERIAL BIGSERIAL VOID RECORD""".split())
GO_KW = set("""package import func var const type struct interface map chan go defer return if else for range
switch case default break continue fallthrough select goto nil true false iota make len cap append copy delete
new panic recover close print println any""".split())
GO_TP = set("""int int8 int16 int32 int64 uint uint8 uint16 uint32 uint64 uintptr byte rune string bool error
float32 float64 complex64 complex128 Context WaitGroup Mutex RWMutex Once Pool Cond""".split())
TS_KW = set("""import export from default class extends implements interface type enum const let var function
return if else for while do switch case break continue new this super async await try catch finally throw
typeof instanceof in of delete void yield static readonly public private protected abstract get set namespace
declare module as is keyof infer never true false null undefined""".split())
TS_TP = set("""string number boolean object symbol bigint any unknown Array Promise Record Partial Readonly
Pick Omit Map Set Date RegExp Error Buffer Observable""".split())

def highlight(code, lang):
    lang = (lang or '').lower()
    if lang in ('sql', 'plpgsql', 'postgres', 'psql', 'pgsql'):
        kw, tp, lc, ci = SQL_KW, SQL_TP, '--', True
    elif lang in ('go', 'golang'):
        kw, tp, lc, ci = GO_KW, GO_TP, '//', False
    elif lang in ('ts', 'typescript', 'js', 'javascript', 'tsx', 'jsx'):
        kw, tp, lc, ci = TS_KW, TS_TP, '//', False
    else:
        return esc(code)
    tok = re.compile(r"""
        (?P<ws>\s+)
      | (?P<lc>%s[^\n]*)
      | (?P<bc>/\*.*?\*/)
      | (?P<str>'(?:[^'\\]|\\.|'')*'|"(?:[^"\\]|\\.)*"|`[^`]*`)
      | (?P<num>\b\d+(?:\.\d+)?\b)
      | (?P<id>[A-Za-z_$][A-Za-z0-9_$]*)
      | (?P<other>.)
    """ % re.escape(lc), re.S | re.X)
    toks = list(tok.finditer(code))
    out = []
    for i, m in enumerate(toks):
        k, t = m.lastgroup, m.group()
        if k == 'ws':
            out.append(esc(t))
        elif k in ('lc', 'bc'):
            out.append(f'<span class="cm">{esc(t)}</span>')
        elif k == 'str':
            out.append(f'<span class="s">{esc(t)}</span>')
        elif k == 'num':
            out.append(f'<span class="n">{esc(t)}</span>')
        elif k == 'id':
            key = t.upper() if ci else t
            nxt = next((toks[j].group() for j in range(i + 1, len(toks)) if toks[j].lastgroup != 'ws'), '')
            if key in kw:
                out.append(f'<span class="kw">{esc(t)}</span>')
            elif key in tp:
                out.append(f'<span class="tp">{esc(t)}</span>')
            elif nxt == '(':
                out.append(f'<span class="fn">{esc(t)}</span>')
            else:
                out.append(esc(t))
        else:
            out.append(esc(t))
    return ''.join(out)

# ─────────────────────────── inline formatting ───────────────────────────
def inline(t):
    # Stash `code` spans as NUL placeholders FIRST so **bold**/*italic* spanning a
    # code span still pair correctly.
    codes = []
    def _stash(m):
        codes.append(m.group(1)); return f'\x00{len(codes)-1}\x00'
    s = re.sub(r'`([^`]+)`', _stash, t)
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(?=\S)(.+?)(?<=\S)\*', r'<em>\1</em>', s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    return re.sub(r'\x00(\d+)\x00', lambda m: f'<code>{esc(codes[int(m.group(1))])}</code>', s)

# ─────────────────────────── block renderer ───────────────────────────
NOTE_MAP = {'info': ('note-info', '💡'), 'tip': ('note-info', '💡'),
            'success': ('note-ok', '✅'), 'ok': ('note-ok', '✅'),
            'warning': ('note-warn', '⚠️'), 'warn': ('note-warn', '⚠️'),
            'danger': ('note-danger', '🚨'), 'error': ('note-danger', '🚨'),
            'inference': ('note-warn', '🧠')}  # [!inference] = block [AI suy luận]
BOX_MAP = {'problem': ('pb', 'pb-lbl', 'Đặt vấn đề'),
           'solution': ('sb-box', 'sb-lbl', 'Giải pháp'),
           'conclusion': ('cb', 'cb-lbl', 'Kết luận')}

def render_code(lang, title, code):
    file = f'<span class="code-file">{esc(title)}</span>' if title else ''
    return ('<div class="code-wrap"><div class="code-hdr">'
            f'<span class="code-lang">{esc(lang)}</span>{file}'
            '<button class="code-copy">Copy</button></div>'
            f'<pre>{highlight(code, lang)}</pre></div>')

def render_image(alt, src, ctx):
    src = rebase(src, ctx)
    cap = f'<div class="concept-img-caption">{inline(alt)}</div>' if alt else ''
    return (f'<div class="concept-img-wrapper"><img alt="{esc(alt)}" loading="lazy" src="{esc(src)}">{cap}</div>')

def rebase(src, ctx):
    if re.match(r'^[a-z]+://', src) or src.startswith('data:'):
        return src
    absp = os.path.normpath(os.path.join(ctx['md_dir'], src))
    return os.path.relpath(absp, ctx['out_dir']).replace(os.sep, '/')

def render_table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    if len(cells) >= 2 and all(re.match(r'^:?-+:?$', c) for c in cells[1]):
        header, body = cells[0], cells[2:]
    else:
        header, body = cells[0], cells[1:]
    th = ''.join(f'<th>{inline(c)}</th>' for c in header)
    trs = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body)
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def render_callout(ctype, title, inner, ctx):
    ctype = ctype.lower()
    if ctype == 'doc':
        return ''  # bridge link chỉ dành cho editor gốc — bỏ khỏi HTML
    inner_html = render_md(inner, ctx)
    if ctype in NOTE_MAP:
        cls, ico = NOTE_MAP[ctype]
        t = f'<strong>{inline(title)}</strong><br>' if title else ''
        return f'<div class="note {cls}"><span class="ni">{ico}</span><div>{t}{inner_html}</div></div>'
    if ctype in BOX_MAP:
        cls, lbl, deft = BOX_MAP[ctype]
        return f'<div class="{cls}"><div class="{lbl}">{esc(title or deft)}</div>{inner_html}</div>'
    if ctype == 'concept':
        t = f'<div class="cbox-title">{inline(title)}</div>' if title else ''
        return f'<div class="cbox"><div class="cbox-label">💡 Khái niệm</div>{t}{inner_html}</div>'
    if ctype == 'example':
        return (f'<div class="ex-card"><div class="ex-hdr"><span class="ex-title">{inline(title)}</span></div>'
                f'<div class="ex-body">{inner_html}</div></div>')
    return f'<div class="note note-info"><span class="ni">💡</span><div>{inner_html}</div></div>'

def render_refs(items):
    out = []
    for r in (items or []):
        star = f'<div class="ref-star">{esc(str(r.get("star","")))}</div>' if r.get('star') else ''
        url = str(r.get('url', ''))
        href = url if re.match(r'^[a-z]+://', url) else ('https://' + url if url else '')
        out.append(
            f'<a class="ref-card" href="{esc(href)}" target="_blank" rel="noopener">'
            f'<div class="ref-ico">{esc(str(r.get("icon","📄")))}</div>'
            f'<div class="ref-body"><div class="ref-title">{esc(str(r.get("title","")))}</div>'
            f'<div class="ref-desc">{esc(str(r.get("desc","")))}</div>'
            f'<div class="ref-url">{esc(re.sub(r"^[a-z]+://", "", url))}</div></div>{star}</a>')
    return '\n'.join(out)

_BLOCK_START = re.compile(r'^(```|>|#{1,6}\s|!\[|\||\s*[-*]\s|\s*\d+\.\s|---\s*$|\*\*\*\s*$)')

def render_md(body, ctx):
    lines = body.split('\n')
    n, i, out = len(lines), 0, []
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1; continue
        m = re.match(r'^```([^\s`]*)(.*)$', line)
        if m:
            lang = m.group(1) or 'text'
            tm = re.search(r'title="([^"]+)"', m.group(2))
            title = tm.group(1) if tm else ''
            code = []
            i += 1
            while i < n and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            i += 1
            body_code = '\n'.join(code)
            if lang == 'refs':
                out.append(render_refs(yaml.safe_load(body_code)))
            else:
                out.append(render_code(lang, title, body_code))
            continue
        im = re.match(r'^!\[(.*?)\]\((.*?)\)\s*$', line)
        if im:
            out.append(render_image(im.group(1), im.group(2), ctx)); i += 1; continue
        cm = re.match(r'^>\s*\[!(\w+)\]\s*(.*)$', line)
        if cm:
            buf = []
            i += 1
            while i < n and lines[i].startswith('>'):
                buf.append(re.sub(r'^>\s?', '', lines[i])); i += 1
            out.append(render_callout(cm.group(1), cm.group(2).strip(), '\n'.join(buf), ctx))
            continue
        hm = re.match(r'^(#{3,6})\s+(.*)$', line)
        if hm:
            tag = 'h3' if len(hm.group(1)) == 3 else 'h4'
            # Trailing `{#id}` = anchor tường minh (đích cho __SUBMAP__ / deep-link)
            text, aid = hm.group(2), ''
            am = re.match(r'^(.*?)\s*\{#([\w-]+)\}\s*$', text)
            if am:
                text, aid = am.group(1), f' id="{am.group(2)}"'
            out.append(f'<{tag}{aid}>{inline(text)}</{tag}>'); i += 1; continue
        if re.match(r'^(---|\*\*\*)\s*$', line):
            out.append('<hr class="div">'); i += 1; continue
        if line.lstrip().startswith('|'):
            tbl = []
            while i < n and lines[i].lstrip().startswith('|'):
                tbl.append(lines[i]); i += 1
            out.append(render_table(tbl)); continue
        if re.match(r'^\s*([-*]|\d+\.)\s+', line):
            ordered = bool(re.match(r'^\s*\d+\.', line))
            items = []
            while i < n and re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]):
                items.append(re.sub(r'^\s*([-*]|\d+\.)\s+', '', lines[i])); i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag} class="md-list">' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue
        if line.lstrip().startswith('<'):  # raw HTML passthrough (inline SVG diagram, escape hatch)
            raw = [line]; i += 1
            while i < n and lines[i].strip():
                raw.append(lines[i]); i += 1
            out.append('\n'.join(raw)); continue
        para = [line]; i += 1
        while i < n and lines[i].strip() and not _BLOCK_START.match(lines[i]) and not lines[i].lstrip().startswith('<'):
            para.append(lines[i]); i += 1
        out.append(f'<p class="prose">{inline(" ".join(para))}</p>')
    return '\n'.join(out)

# ─────────────────────────── frontmatter / doc assembly ───────────────────────────
def split_front(text):
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', text, re.S)
    if m:
        return yaml.safe_load(m.group(1)) or {}, m.group(2)
    return {}, text

BADGE = {'basic': ('b-bas', 'CƠ BẢN'), 'advanced': ('b-adv', 'NÂNG CAO'),
         'expert': ('b-exp', 'EXPERT'),
         'draft': ('b-bas', 'DRAFT'), 'verified': ('b-exp', 'VERIFIED'),
         'inference': ('b-adv', 'AI SUY LUẬN'), 'deterministic': ('b-exp', 'DETERMINISTIC')}

def favicon_uri(txt):
    txt = esc(txt or 'FT')
    return ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
            "<rect width='32' height='32' rx='6' fill='%230d0f14'/>"
            "<text x='50%25' y='55%25' dominant-baseline='middle' text-anchor='middle' "
            f"font-size='14' font-weight='700' fill='%2300d4ff'>{txt}</text></svg>")

def strip_bridge(body):
    return re.sub(r'^>\s*\[!doc\][^\n]*\n(?:>[^\n]*\n)*\s*\n?', '', body, flags=re.M)

def build(doc_dir):
    doc_dir = doc_dir.rstrip('/')
    abs_dir = os.path.abspath(doc_dir)
    if not os.path.isdir(abs_dir):
        sys.exit(f'không thấy doc folder: {abs_dir}')
    out_dir = os.path.dirname(abs_dir)
    doc = yaml.safe_load(open(os.path.join(abs_dir, '_doc.yml'), encoding='utf-8'))

    # load sections: NN-slug.md, id mặc định = slug bỏ prefix số
    sec = {}
    for fn in os.listdir(abs_dir):
        if re.match(r'^\d+.*\.md$', fn):
            fm, body = split_front(open(os.path.join(abs_dir, fn), encoding='utf-8').read())
            fm.setdefault('id', re.sub(r'^\d+-', '', fn[:-3]))
            sec[fm['id']] = {'fm': fm, 'body': body}

    ctx = {'md_dir': abs_dir, 'out_dir': out_dir}
    order = [i for g in doc['groups'] for i in g['items']]
    missing = [i for i in order if i not in sec]
    if missing:
        sys.exit(f"_doc.yml khai báo section không có file md: {missing}")

    # sidebar
    sb = []
    first = order[0]
    for g in doc['groups']:
        sb.append(f'  <div class="nav-sec"><div class="nav-sec-title">{esc(g["title"])}</div>')
        for i in g['items']:
            fm = sec[i]['fm']
            active = ' active' if i == first else ''
            label = fm.get('nav', fm['title'])
            sb.append(f'    <button class="nav-btn{active}" data-target="{i}">{esc(label)}</button>')
        sb.append('  </div>')
    # topnav
    tn = []
    for i in doc.get('topnav', order):
        fm = sec[i]['fm']
        active = ' active' if i == first else ''
        tn.append(f'  <button class="tn-btn{active}" data-target="{i}">{esc(fm.get("tnav", fm.get("nav", fm["title"])))}</button>')
    # sections
    secs = []
    for i in order:
        fm, body = sec[i]['fm'], sec[i]['body']
        cls, txt = BADGE.get(fm.get('level', 'basic'), BADGE['basic'])
        btxt = fm.get('badge', txt)
        active = ' active' if i == first else ''
        sub = f'<div class="sec-sub">{inline(fm["subtitle"])}</div>' if fm.get('subtitle') else ''
        html = render_md(strip_bridge(body), ctx)
        secs.append(
            f'<section class="sec{active}" id="s-{i}">\n'
            f'  <div class="sec-hdr">\n'
            f'    <div class="sec-num">{esc(str(fm.get("num", "")))}</div>\n'
            f'    <div><div class="sec-title">{inline(fm["title"])}</div>{sub}</div>\n'
            f'    <span class="badge {cls}">{esc(btxt)}</span>\n'
            f'  </div>\n{html}\n</section>')

    css = open(os.path.join(RENDER, 'assets/tokens.css'), encoding='utf-8').read()
    js = open(os.path.join(RENDER, 'assets/engine.js'), encoding='utf-8').read()
    submap = {}
    for sec_id, subs in (doc.get('subs') or {}).items():
        for sub in (subs or []):
            submap[sub] = sec_id
    js = f'window.__SUBMAP__ = {json.dumps(submap)};\n' + js
    tpl = open(os.path.join(RENDER, 'templates/base.html'), encoding='utf-8').read()
    out = tpl
    for k, v in {
        'TITLE': doc['title'], 'DESCRIPTION': doc.get('description', ''),
        'FAVICON': favicon_uri(doc.get('favicon', 'FT')),
        'LOGO_ICON': doc.get('logo_icon', 'FT'), 'LOGO_TITLE': doc.get('logo_title', ''),
        'LOGO_SUB': doc.get('logo_sub', ''),
        'SIDEBAR': '\n'.join(sb), 'TOPNAV': '\n'.join(tn),
        'SECTIONS': '\n\n'.join(secs), 'CSS': css, 'JS': js,
    }.items():
        out = out.replace('{{%s}}' % k, v if k in ('SIDEBAR', 'TOPNAV', 'SECTIONS', 'CSS', 'JS') else esc(str(v)) if k in ('TITLE', 'DESCRIPTION', 'LOGO_TITLE', 'LOGO_SUB') else str(v))

    out_html = abs_dir + '.html'
    open(out_html, 'w', encoding='utf-8').write(out)
    print(f'✓ built {out_html}  ({len(out)} bytes, {len(order)} sections)')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: python3 build.py <doc-folder>')
    build(sys.argv[1])
