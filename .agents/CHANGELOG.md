# flow-trace-genesis — Changelog

> Ghi lại thay đổi requirement, tiến độ, quyết định kiến trúc để agent đọc nhanh.

## Bối cảnh dự án

- **Sản phẩm**: Claude Code plugin `flow-trace-genesis` — lần đầu gặp project lạ sẽ
  khảo sát (Evidence: Read/LSP/Serena/ast-grep · Candidate: GitNexus/DeepWiki-Open/
  Understand-Anything/GitDiagram · Ingest: MarkItDown/Docling) rồi SINH `flow-trace`
  local self-contained cho project đó (CORE + PROFILE, version stamp, regenerate
  bảo toàn PROFILE, golden-flow gate Draft→Verified).
- **Nguồn gốc**: đúc từ skill `flow-trace` viết tay cho workspace Lending
  (nghiệm thu golden flow `resubmit-a2` ngày 2026-07-17).
- **Phân phối**: plugin marketplace (Claude Code) + installer Codex/OpenCode/Cursor.
- **Bãi thử**: go-core-adapter-service (Go+gRPC) → Dni workspace → dogfood Lending.
- **Repo**: `github.com/mthang1801/flow-trace-genesis` · private-first, Apache-2.0,
  sanitize profiles trước khi public.

## Changelog Chi Tiết

### 2026-07-18 — examples/grpc-go + README "See it in action"

**Loại**: Docs / Distribution

**Thay đổi**:
- `examples/grpc-go/`: sample công khai từ lần chạy thật trên grpc-go@7d870454 — skill
  sinh ra (SKILL.md CORE+PROFILE), md-source 12 section + graph.json, HTML self-contained
  4.3MB, README giải thích cách sinh + cách rebuild. grpc-go là OSS công khai nên đưa
  được (profile Lending vẫn INTERNAL).
- Screenshot 4 section (overview/KG/sequence/steps) chụp từ HTML mở qua file:// (tự
  chứng minh self-contained) → `docs/images/`.
- README EN/VI: section "See it in action"/"Xem kết quả thật" (3 ảnh + link sample +
  link tải HTML), intro trỏ anchor, Repo layout thêm examples/ + docs/images/ + doctor.sh.

**Trạng thái**: `Done`.

### 2026-07-18 — installers/doctor.sh: kiểm kê + cài tool opt-in

**Loại**: Distribution / DX

**Thay đổi**:
- `installers/doctor.sh` 2 chế độ: scan read-only (tool × tier required/trace/optional ×
  impact × lệnh fix đúng package manager của máy — dnf/apt/pacman/zypper/brew) và
  `--install` cài user-space (pip --user / npm -g) sau y/N từng tool. Không bao giờ tự
  sudo; exit 1 khi thiếu required (python3/PyYAML) — dùng được cho smoke test.
- SKILL.md bước Khảo sát: thiếu tool → nói rõ mất gì + trỏ user tới doctor, agent không
  tự chạy install. README EN/VI thêm mục "Get the most out of it"; installers/README.md
  thêm section Doctor.
- Verify trên máy thật: bắt đúng rg thiếu (fact đã biết), no-tty tự skip an toàn.

**Trạng thái**: `Done`.

### 2026-07-18 — Mermaid render thật trong HTML (sync từ Lending)

**Loại**: Feature (sync — luật không-fork)

**Thay đổi**:
- `render/` nhận bản mới: `assets/mermaid.min.js` 11.16.0 vendored (3.5MB, nhúng chỉ khi
  doc có fence) + `mermaid-init.js` (render lazy theo section active — getBBox hỏng trong
  `display:none`); build.py: fence ```mermaid → diagram thật + source trong `<details>`,
  và escape `</script|</body|</html` trong bundle JS (DOMPurify của mermaid chứa
  `"</body></html>"` → live-server inject làm vỡ toàn bộ inline script); check.py check 8c
  fence↔pre.mermaid↔lib.
- `references/html-render.md`: row mermaid mới + bẫy (5) live-server injection; lưu ý
  source phải parse được mermaid 11 (label dotted-edge không chứa `.`).
- Golden grpc-go rebuild 4286742 bytes, check pass; 2 fence parse OK qua `mermaid.parse`.

**Trạng thái**: `Done` — evidence chi tiết bên Lending
(`.agents/changes/flow-trace-knowledge-graph/evidence.md`, iteration 4).

### 2026-07-18 — KG control panel + hỗ trợ Cursor/Antigravity + README cộng đồng

**Loại**: Feature / Distribution / Docs

**Thay đổi**:
- Sync KG iteration 2 từ Lending: control panel kiểu Obsidian graph view (search, filter
  loại node + verified-only, slider node-size/link-thickness/text-fade, re-layout/fit/
  reset); content 1560px, canvas 680px.
- Installer xác minh trên máy thật: **Cursor có Agent Skills native** →
  `~/.cursor/skills-cursor/` (sửa path cũ sai `~/.cursor/skills/`); thêm target
  **antigravity** → `~/.gemini/skills/` + in hướng dẫn thêm dòng
  `@./skills/flow-trace-genesis/SKILL.md` vào `~/.gemini/GEMINI.md` (không tự sửa file
  user). Dry-run pass cả 6 target.
- README viết lại theo hướng cộng đồng: bỏ toàn bộ tham chiếu project test local,
  thêm "Vì sao cần nó", nguyên tắc cứng, yêu cầu, đóng góp.

**Trạng thái**: `Done`.

### 2026-07-18 — Sync tính năng Knowledge Graph (section 02, Candidate tier)

**Loại**: Feature (sync từ Lending — luật không-fork)

**Thay đổi**:
- `render/` nhận bản mới: `kg/extract.py` (GitNexus cypher, k-hop từ seeds, graph.json,
  pin `gitnexus@1.6.6` đọc được storage v40+v41, chống cắt stdout 64KB),
  `assets/cytoscape.min.js` 3.34.0 + `kg-init.js` (2 tông verified/candidate),
  build.py fence ` ```kg ` nhúng có điều kiện, check.py 4 check KG.
- `references/html-render.md`: template 12 section (KG=02 sau Tóm tắt), pipeline
  script-first ~0 token, luật degrade khi repo đích không có index (trừ khi governance
  đích bắt buộc analyze).
- Golden grpc-go đã dùng thật: analyze 1:57ph (crash cleanup — index vẫn hợp lệ),
  build+check pass 12 sections.

**Trạng thái**: `Done` — chi tiết evidence bên Lending
(`.agents/changes/flow-trace-knowledge-graph/`).

### 2026-07-18 — Golden Go: genesis chạy end-to-end lần đầu (grpc-go)

**Loại**: Dogfood / Verification

**Thay đổi**:
- Chạy đủ playbook 6 bước trên `grpc-go@7d870454`: intake (không flow-trace local),
  khảo sát tool thật (gopls/uvx có; ast-grep/rg không — degrade grep), questionnaire
  Q1-Q10 với bằng chứng file:line, sinh skill `.claude/skills/flow-trace/` (CORE+PROFILE
  grpc-go: registry init() thay DI, HTTP/2 wire thay broker, gotchas G1-G5 có citation),
  cài sau confirm vị trí (AskUserQuestion), trace golden `unary-invoke-client`.
- Cẩm nang golden: 24 bước file:line, 12 rule validation, 8 failure mode — finding đắt
  nhất: unary `SendMsg` trả `nil` khi transport write lỗi (`stream.go:1147-1155`).
  Build + check pass ngay lần đầu (76302 bytes, 11 sections).

**Trạng thái**: `Review` — chờ user chấm gate 6b (Draft→Verified).


### 2026-07-17 — 5.2 validated + fix lệch manifest; bootstrap Done

**Loại**: Fix / Verification

**Thay đổi**:
- Validate plugin trên bản Claude Code đang chạy qua `claude --plugin-dir ... plugin details`:
  load OK, MCP 3 server. Phát hiện Claude Code hợp nhất commands/skills → command file
  trong plugin tạo skill trùng tên (Skills ×2). Fix: chuyển `commands/flow-trace-genesis.md`
  → `installers/prompts/` (chỉ dành cho Codex/OpenCode/Cursor), SKILL.md thêm
  `argument-hint`, installer target `claude` bỏ copy command. Kết quả: Skills (1), ~243 tok.
- marketplace.json: `description` top-level, khớp schema marketplace đã cài thật trên máy.
- Bãi thử golden Go đổi theo chỉ đạo user: `~/Repositories/Go/grpc-go`.

**Trạng thái**: `Done` — bootstrap 19/19; push lên remote sau commit này.

### 2026-07-17 — Bootstrap v1 thực thi xong (executor gate mở bằng "Specs approved")

**Loại**: Product / Bootstrap

**Thay đổi**:
- Khung phân phối: `.claude-plugin/marketplace.json` + `plugins/flow-trace-genesis/
  .claude-plugin/plugin.json` (v0.1.0, Apache-2.0).
- Skill genesis: `SKILL.md` playbook 6 bước có gate (intake/chống ghi đè → khảo sát
  degrade-gracefully → questionnaire Q1-Q10 bằng chứng file:line → sinh CORE+PROFILE
  stamp `generated-by` → cài theo governance đích có confirm → golden-flow gate
  Draft→Verified) + `commands/flow-trace-genesis.md`.
- References: `core-template.md` (CORE với vùng `<!-- CORE/PROFILE:BEGIN/END -->`,
  6 archetype phổ quát, placeholder table), `report-template.md` + `html-render.md`
  (generic hóa từ Lending, pipeline md-source), `profile-questionnaire.md`,
  `profiles/_TEMPLATE.md`, `profiles/lending.md` (mẫu vàng — INTERNAL).
- `render/` port nguyên trạng từ Lending (diff identical; build lại golden resubmit-a2
  từ bản plugin → output md5 không đổi). Luật không-fork ghi trong html-render.md.
- Phân phối: `.mcp.json` (serena/markitdown/docling + ghi chú degrade),
  `installers/install.sh` 4 target + `--dry-run` (đã test cả 4), `installers/README.md`,
  root `README.md`.

**Trạng thái**: `Review` — chờ user test manual cài marketplace trong session Claude Code
(`/plugin marketplace add` — CLI không có đường non-interactive) và lệnh commit.

### 2026-07-17 — Amend plan bootstrap: base render md-source → HTML

**Loại**: Plan (amend)

**Thay đổi**:
- Cẩm nang flow do skill sinh ra sẽ persist dạng md-source đa file (`_doc.yml` menu +
  mỗi section một `NN-slug.md`) và build HTML self-contained bằng bộ `render/`
  (build.py + check.py + base.html + tokens.css + engine.js — phỏng theo ~/mAIvt).
- Bộ base này đã được xây và verify bên Lending
  (`.agents/skills/flow-trace/render/`, golden `docs/flows/resubmit-a2/` build + check
  pass 2026-07-17). Bootstrap thêm bước 2b: **copy nguyên trạng, không fork** — mọi sửa
  base phải sync ngược về Lending để chống trôi CORE.

**Trạng thái**: `Review` — executor gate vẫn đóng.

### 2026-07-17 — Plan bootstrap v1 persisted

**Loại**: Plan

**Thay đổi**:
- Persist `proposal/plans/tasks/evidence` cho change `bootstrap`: cấu trúc repo đích
  (marketplace + plugin + installers), playbook genesis 6 bước có gates (intake với
  chống ghi đè, khảo sát degrade-gracefully, questionnaire bằng chứng file:line,
  sinh CORE+PROFILE có version stamp, cài theo governance đích, golden-flow gate),
  thứ tự thực thi 8 bước, verification (harness + cài thử marketplace local +
  installer dry-run), 5 risks có mitigation.
- CORE sẽ generic hóa từ bản Lending; chi tiết nội bộ dồn về `profiles/lending.md`
  (INTERNAL, sanitize-before-public).

**Trạng thái**: `Review` — executor gate đóng, chờ user approve plans.md.

### 2026-07-17 — Scaffold governance lean

**Loại**: Agent System / Bootstrap

**Thay đổi**:
- `CLAUDE.md` shim `@AGENTS.md`; root `AGENTS.md` routing + boundaries + safety.
- `.agents/AGENTS.md`: luật lõi cutoff từ Lending — safety rules, restricted commands,
  Conventional Commits + Co-authored-by (Claude/Codex), workflow 7 bước với executor
  gate và grill gate, nguyên tắc sản phẩm (evidence tier, CORE/PROFILE, degrade
  gracefully, sanitize-before-public), status vocabulary.
- `.agents/changes/README.md`: contract change record 4 file bắt buộc.
- `.agents/progress.md`: dashboard khởi tạo với registry `bootstrap` (Open).
- `.agents/scripts/governance-harness.sh`: harness kiểm tra bất biến governance —
  dùng `grep -F` thuần POSIX (bài học từ Lending: harness gọi `rg` fail giả 86 lỗi
  trên máy không có binary ripgrep).

**Trạng thái**: `Done` — harness pass (xem output trong lịch sử phiên).
