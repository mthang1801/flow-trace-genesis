# Render HTML — pipeline md-source → artifact document

Cẩm nang flow **không viết HTML tay**: soạn **md-source đa file** (mỗi section một markdown)
+ `_doc.yml` (menu) rồi **build** ra HTML self-contained bằng bộ `render/` đi kèm skill.
MD là source of truth — không bao giờ sửa HTML mà không sửa MD trước.

> `render/` trong plugin này là bản **port nguyên trạng** từ Lending
> `.agents/skills/flow-trace/render/` (đã verify với golden flow `resubmit-a2` 2026-07-17;
> gốc phỏng theo hệ thống doc `~/mAIvt`). **Không fork chỉnh riêng** — sửa base thì sync
> ngược về nguồn.

## Cấu trúc một cẩm nang

```text
{{OUTPUT_DIR}}<slug>/              # md-source (nguồn chân lý)
├── _doc.yml                       # title, description, favicon, logo, groups (sidebar), topnav, subs
├── 01-overview.md                 # mỗi section 1 file, prefix số = thứ tự đọc
├── 02-sequence.md
├── ...
└── 11-history.md
{{OUTPUT_DIR}}<slug>.html          # output build — KHÔNG sửa tay
```

`_doc.yml` tối thiểu:

```yaml
title: Flow <slug> — <tên nghiệp vụ>
description: <1-3 câu>
favicon: FT            # 1-2 ký tự vẽ vào favicon SVG
logo_icon: FT
logo_title: FLOW-TRACE
logo_sub: <slug> · <project>
groups:                # sidebar — 3 nhóm chuẩn của template
- title: Flow
  items: [overview, knowledge-graph, sequence, steps, graph]
- title: Phân tích
  items: [validation, business, failure-modes, security-ops, code-review]
- title: Meta
  items: [open-items, history]
# topnav: [...]        # optional, mặc định = thứ tự groups
# subs: {sectionId: [anchorId, ...]}  # optional, deep-link #anchor → mở đúng section
```

Frontmatter mỗi section md:

```yaml
---
id: overview           # = data-target của nav; mặc định là slug bỏ prefix số
num: '01'
title: Tóm tắt
subtitle: <optional>
level: draft           # draft|verified|deterministic|inference|basic|advanced|expert → badge
badge: <optional>      # override chữ trên badge
nav: 01 · Tóm tắt      # label sidebar
tnav: Tóm tắt          # label topnav
---
```

## Build & gate

```bash
python3 <skill-dir>/render/build.py {{OUTPUT_DIR}}<slug>   # → {{OUTPUT_DIR}}<slug>.html
python3 <skill-dir>/render/check.py {{OUTPUT_DIR}}<slug>   # gate — PHẢI pass sau mỗi build
```

Cần `python3` + PyYAML. `check.py` chặn các lỗi cơ học: `**`/`*italic*` leak, callout marker
sót, tag không cân, resource external (self-contained tuyệt đối — không cả Google Fonts),
section/nav drift, và **rớt nhãn `[AI suy luận`** khi md nguồn có.

## Cú pháp md được hỗ trợ (những gì build.py hiểu)

| Cú pháp | Render thành |
| --- | --- |
| `> [!info/warn/danger/ok]` callout | `.note` box (💡/⚠️/🚨/✅) |
| `> [!inference]` | `.note-warn` 🧠 — dùng cho block `[AI suy luận]` |
| `> [!problem]` / `[!solution]` / `[!conclusion]` | box Đặt vấn đề / Giải pháp / Kết luận |
| `> [!concept]` / `[!example]` | concept box / example card |
| ` ```ts/js/sql/go title="file.ts" ` | code block highlight + copy button |
| ` ```mermaid ` | **diagram render thật** (mermaid vendored ~3.5MB, nhúng chỉ khi doc có fence) — render lazy khi section active (mermaid đo getBBox, vẽ trong `display:none` sẽ hỏng); source gốc giữ trong `<details>` collapse để copy. Source PHẢI parse được với mermaid 11 — bẫy đã gặp: label dotted-edge kiểu `-.text.->` không được chứa `.` (dùng `-.->|text|` thay thế); check.py bắt fence↔pre.mermaid↔lib nhúng nhưng KHÔNG bắt syntax lỗi (chỉ hiện bomb lúc runtime) — verify bằng browser hoặc `mermaid.parse` |
| ` ```kg ` (fence rỗng) | canvas knowledge graph tương tác (Cytoscape.js vendored) — data từ `<doc-folder>/graph.json` do `render/kg/extract.py` sinh; thiếu graph.json thì build fail |
| ` ```refs ` (YAML `{icon,title,desc,url,star}`) | ref-card grid |
| Bảng md | `.tbl` (cell `code` màu cyan — dùng cho `file:line`) |
| `### Heading {#anchor-id}` | h3 có id — đích cho `subs` deep-link |
| Dòng bắt đầu `<` | **raw HTML passthrough** — dùng nhúng inline SVG diagram (bọc `<div class="flowcard"><div class="flowcap">Tiêu đề</div><svg…>`), KHÔNG được có dòng trống bên trong block |

**Bẫy đã biết**: (1) list item phải nằm **một dòng** — bullet wrap xuống dòng sẽ vỡ render
(bold leak → check.py fail); (2) marker SVG (`url(#id)`) phải có `<defs>` trong **chính SVG
đó** với id duy nhất toàn document; (3) không dùng blockquote trần `>` — chỉ dùng dạng
callout `> [!type]`; (4) ngôn ngữ ngoài ts/js/sql/go không được highlight (render plain) —
chấp nhận được, đừng chế thêm highlighter khi chưa cần; (5) build.py vô hiệu hoá
`</script|</body|</html` trong bundle JS thành `<\/...` — lib vendored (DOMPurify trong
mermaid) chứa literal `"</body></html>"`, live-server inject snippet live-reload vào trước
`</body>` ĐẦU TIÊN của response → nếu không escape, script inline bị đóng sớm và toàn bộ
JS của trang vỡ (SyntaxError + nửa sau parse thành HTML).

## Mapping section report-template → section md (có KG từ 2026-07-18)

| Section report | File md | level/badge |
| --- | --- | --- |
| Header meta + 1. Tóm tắt | `01-overview.md` — meta thành bảng, không dùng blockquote | `draft` (→ `verified` sau golden-flow) |
| 2. Knowledge graph (máy sinh) | `02-knowledge-graph.md` — banner `> [!warn]` ghi rõ **Candidate tier** (check.py enforce) + fence ` ```kg ` | `basic`, badge `CANDIDATE` |
| 3. Sequence diagram | `03-sequence.md` — inline SVG (flowcard) + mermaid fence nguồn đầy đủ | `deterministic` |
| 4. Bảng bước | `04-steps.md` | `deterministic` |
| 5. Graph quan hệ (vẽ tay) | `05-graph.md` — inline SVG + mermaid fence | `deterministic` |
| 6. Validation & Rules | `06-validation.md` | `deterministic` |
| 7. Business spec ngược (+PRD nếu có) | `07-business.md` — mở đầu bằng `> [!inference]` chứa nguyên văn `[AI suy luận — cần domain owner xác nhận]` | `inference` |
| 8. Failure modes | `08-failure-modes.md` | `advanced`, badge tùy số archetype |
| 9. Security & Ops | `09-security-ops.md` — mở đầu `> [!inference]` | `inference` |
| 10. Ghi chú code review | `10-code-review.md` | `basic` |
| 11. Chưa xác định / chưa trace | `11-open-items.md` — bắt buộc tồn tại, kể cả "không có" | `basic` |
| 12. Lịch sử trace | `12-history.md` | `basic` |

## Knowledge graph (section 02) — pipeline script-first, ~0 token

1. Seeds = tên symbol trong bảng bước (đã Read); mỗi repo GitNexus một danh sách.
2. Chạy extractor (KHÔNG để agent đọc/chép graph data — token gần 0):

```bash
python3 <skill-dir>/render/kg/extract.py --doc {{OUTPUT_DIR}}<slug> \
  --repo <gitnexus-repo> --seeds "ClassA,MethodB@path-substring" \
  [--repo <repo2> --seeds "..."] [--hops 2] [--cap 200]
```

3. `02-knowledge-graph.md`: banner Candidate + fence ` ```kg ` (rỗng). Build tự nhúng
   cytoscape.min.js + graph.json (chỉ doc có fence kg mới chịu +~430KB).
4. Repo chưa có index GitNexus → `npx -y gitnexus@<ver> analyze` trước; version CLI phải
   đọc được storage version của index (lỗi "Database file version" = drift — dùng bản mới
   hơn hoặc re-analyze; extractor có `--gitnexus-version`).
5. Render 2 tông: node/edge trùng seeds (bảng bước) = verified sáng, k-hop = candidate mờ
   nét đứt. Cross-repo edge chưa có ở v1 — nói rõ trong section. Repo không có index thì
   BỎ section này và ghi chú (trừ khi governance đích yêu cầu bắt buộc analyze).

## Ràng buộc (không đổi)

- Tuyệt đối không CDN/external resource — kể cả Google Fonts (check.py enforce; hyperlink `<a>` thì được).
- Mọi `file:line` giữ dạng `` `code` `` — không biến thành link tuyệt đối theo máy.
- Nhãn `[AI suy luận]` không được rớt khi render (check.py enforce).
- Regenerate: HTML sinh lại toàn bộ từ md-source bằng build.py, không patch tay HTML.
- Share qua claude.ai: publish bằng Artifact tool (private mặc định).
