#!/usr/bin/env python3
"""check.py — static validation gate cho HTML build từ md-source (flow-trace).

Usage:  python3 .agents/skills/flow-trace/render/check.py docs/flows/<slug>
Reads   <doc-folder>/_doc.yml + NN-*.md  và  <doc-folder>.html (sibling)
Exit != 0 nếu có hard-fail — chạy sau MỖI lần build.

Encode các failure mode cơ học: render leak (** / *italic*), leftover callout
marker, unbalanced tags, external resource (phải self-contained tuyệt đối),
section/nav wiring drift, và rớt nhãn [AI suy luận].
"""
import os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("cần PyYAML: pip install pyyaml")

# flow-trace nghiêm hơn mAIvt: KHÔNG cả Google Fonts. Chỉ chừa xmlns của SVG.
ALLOWED_HOSTS = ('www.w3.org',)

def strip_regions(html):
    """Body HTML with <script>, <pre>, inline <code> removed → 'prose' only."""
    body = html.split('<body>', 1)[-1]
    body = re.sub(r'<script\b.*?</script>', '', body, flags=re.S)
    prose = re.sub(r'<pre\b.*?</pre>', '', body, flags=re.S)
    prose = re.sub(r'<code\b.*?</code>', '', prose, flags=re.S)
    return body, prose

def check(doc_dir):
    doc_dir = doc_dir.rstrip('/')
    abs_dir = os.path.abspath(doc_dir)
    html_path = abs_dir + '.html'
    fails = []
    def fail(msg): fails.append(msg)

    if not os.path.exists(html_path):
        print(f'✗ {doc_dir}: built HTML missing ({html_path}) — chạy build.py trước')
        return 1
    html = open(html_path, encoding='utf-8').read()
    body, prose = strip_regions(html)

    # 1. Bold leak
    if '**' in prose:
        ex = re.search(r'.{0,30}\*\*.{0,30}', prose)
        fail(f"literal '**' in prose (code-inside-bold?) e.g. …{ex.group(0).strip()}…")

    # 2. Italic leak
    m = re.search(r'(?<![\w*])\*(?=\S)[^*\n]{1,120}?(?<=\S)\*(?![\w*])', prose)
    if m:
        fail(f"unrendered '*italic*' in prose e.g. …{m.group(0)[:50]}…")

    # 3. Leftover callout markers / heading-anchor syntax (outside code/pre)
    for pat in (r'~~~', r'\{#[\w-]+\}',
                r'\[!(?:problem|solution|conclusion|concept|example|info|'
                        r'tip|warning|warn|danger|error|success|ok|note|doc|inference)\b'):
        m = re.search(pat, prose, re.I)
        if m:
            ctx = prose[max(0, m.start()-20):m.start()+30].strip()
            fail(f"leftover marker '{m.group(0)}' in HTML e.g. …{ctx}…")

    # 4. Tag balance
    body_nopre = re.sub(r'<pre\b.*?</pre>', '', body, flags=re.S)
    for tag in ('div', 'section', 'ul', 'ol', 'table', 'nav', 'main', 'svg'):
        o = len(re.findall(r'<%s\b' % tag, body_nopre))
        c = len(re.findall(r'</%s>' % tag, body_nopre))
        if o != c:
            fail(f"unbalanced <{tag}>: {o} open vs {c} close")

    # 5. Self-contained: chỉ hyperlink (<a href>) được ra ngoài; mọi RESOURCE phải local.
    #    Strip NỘI DUNG <script> (giữ tag để vẫn bắt <script src=...>): URL trong JS vendored
    #    (license comment của cytoscape...) chỉ là string, không phải resource load.
    html_no_script_body = re.sub(r'(<script\b[^>]*>).*?(</script>)', r'\1\2', html, flags=re.S)
    html_no_anchors = re.sub(r'<a\s[^>]*>', '', html_no_script_body)
    for host in set(re.findall(r'https?://([a-zA-Z0-9.\-]+)', html_no_anchors)):
        if host not in ALLOWED_HOSTS:
            fail(f"external host '{host}' — artifact phải self-contained")

    # 6. Section count: HTML == md files == _doc.yml order
    doc = yaml.safe_load(open(os.path.join(abs_dir, '_doc.yml'), encoding='utf-8'))
    order = [i for g in doc['groups'] for i in g['items']]
    md_files = [f for f in os.listdir(abs_dir) if re.match(r'^\d+.*\.md$', f)]
    n_html = len(re.findall(r'<section class="sec', html))
    if not (n_html == len(md_files) == len(order)):
        fail(f"section count drift: html={n_html} md={len(md_files)} _doc.yml={len(order)}")

    # 7. Nav wiring
    ids = set(re.findall(r'<section class="sec[^"]*" id="s-([^"]+)"', html))
    nav_targets = set(re.findall(r'class="(?:nav|tn)-btn[^"]*"\s+data-target="([^"]+)"', html))
    for t in nav_targets:
        if t not in ids:
            fail(f"nav button data-target='{t}' has no matching <section id='s-{t}'>")
    for i in order:
        if i not in ids:
            fail(f"_doc.yml lists '{i}' but no <section id='s-{i}'> in HTML")

    # 8b. Knowledge graph: fence ```kg ↔ graph.json ↔ banner Candidate phải đồng bộ
    kg_files = [f for f in md_files
                if re.search(r'^```kg\b', open(os.path.join(abs_dir, f), encoding='utf-8').read(), re.M)]
    has_graph = os.path.exists(os.path.join(abs_dir, 'graph.json'))
    if kg_files and not has_graph:
        fail(f"có fence ```kg ({kg_files}) nhưng thiếu graph.json — chạy render/kg/extract.py")
    if has_graph and not kg_files:
        fail("graph.json tồn tại nhưng không md nào dùng fence ```kg — xóa hoặc thêm section")
    for f in kg_files:
        if 'Candidate' not in open(os.path.join(abs_dir, f), encoding='utf-8').read():
            fail(f"{f}: section KG thiếu banner Candidate tier (graph máy sinh phải ghi rõ nguồn gốc)")
    if kg_files and 'kg-canvas' not in html:
        fail("md có fence ```kg nhưng HTML không có #kg-canvas — build lại")

    # 8c. Mermaid: fence ```mermaid phải thành diagram thật (lib nhúng + pre.mermaid),
    #     không được rớt về code block tĩnh.
    mmd_files = [f for f in md_files
                 if re.search(r'^```mermaid\b', open(os.path.join(abs_dir, f), encoding='utf-8').read(), re.M)]
    if mmd_files:
        if '<pre class="mermaid">' not in html:
            fail(f"md có fence ```mermaid ({mmd_files}) nhưng HTML không có pre.mermaid — build lại")
        if 'mermaid.initialize' not in html:
            fail("HTML có pre.mermaid nhưng thiếu mermaid vendored (mermaid.initialize) — build lại")

    # 8. Nhãn suy luận không được rớt: nếu md nguồn có "[AI suy luận" thì HTML cũng phải có
    md_has_inference = any(
        '[AI suy luận' in open(os.path.join(abs_dir, f), encoding='utf-8').read()
        for f in md_files)
    if md_has_inference and '[AI suy luận' not in html and 'AI SUY LUẬN' not in html:
        fail("md nguồn có nhãn '[AI suy luận' nhưng HTML render rớt mất nhãn")

    tag = os.path.basename(doc_dir)
    if fails:
        for f in fails: print(f'  ✗ {tag}: {f}')
        print(f'✗ check FAILED: {doc_dir} ({len(fails)} issue(s))')
        return 1
    print(f'✓ check OK: {doc_dir} ({n_html} sections)')
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: python3 check.py <doc-folder>')
    sys.exit(check(sys.argv[1]))
