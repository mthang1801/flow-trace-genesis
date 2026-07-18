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

### 2026-07-18 — Gỡ CI: tài khoản GitHub bị khoá billing, không phải lỗi workflow

**Loại**: Revert (blocked by external constraint, không phải bug của repo)

**Thay đổi**:
- `ci.yml` (P1, commit trước) chạy đúng cục bộ (build+check golden, doctor.sh,
  shellcheck, render-sync guard — cả 4 pass khi test local) nhưng **mọi run trên GitHub
  đều fail trong <1 giây, không được gán runner**. Chẩn đoán qua API: `steps: []`,
  `runner_name: ""`, rerun cùng lỗi → không phải lỗi cú pháp/workflow. User check UI xác
  nhận nguyên nhân thật: *"The job was not started because your account is locked due to
  a billing issue"* — GitHub yêu cầu payment method hợp lệ dù usage thực tế $0 (đã được
  included-usage bù đủ). User chọn không thêm payment method → gỡ CI thay vì chờ mở khoá.
- Gỡ: `.github/workflows/ci.yml`, badge CI khỏi README EN/VI, câu "these are exactly what
  CI runs" trong CONTRIBUTING.md (thay bằng "không có CI gate tự động — tự chạy trước khi
  mở PR"), tham chiếu "CI's render-sync job" (thay bằng hướng dẫn chạy tay).
- **KHÔNG gỡ**: `scripts/check-render-sync.sh` (vẫn dùng tay được, còn nguyên giá trị),
  Pages (`pages-build-deployment` không đi qua hàng đợi Actions bị khoá — verify bằng 3
  lần build Pages `success` ngay trong lúc billing đang khoá), tag/release v0.1.0.
- Nếu sau này user tự gỡ khoá billing (thêm payment method hoặc GitHub Support xử lý),
  `ci.yml` có thể phục hồi nguyên trạng từ git history (commit `1c90ce2`).

**Trạng thái**: `Done` (P1 coi như rollback — không tính vào punch list hoàn thành).

### 2026-07-18 — CI, tag/release, no-fork guard, Pages demo, CONTRIBUTING

**Loại**: Distribution / DX / Docs (punch list P1-P5 sau audit repo public)

**Thay đổi**:
- **P1 CI** (`.github/workflows/ci.yml`, 3 job): render golden (`build.py`+`check.py` trên
  `examples/grpc-go`), doctor.sh smoke (exit code), shellcheck 3 script. Badge CI ở đầu
  README EN/VI. Verify local trước khi push: cả 3 job pass y hệt logic CI.
- **P3 no-fork guard**: `scripts/check-render-sync.sh` (generic, N thư mục, treesum
  md5) — verify thật: 3 bản Lending+genesis đang identical. Wire vào CI job thứ 4
  (`render-sync`): tự phát hiện mọi bản `render/` trong repo, chỉ diff khi ≥2 bản (hiện
  genesis chỉ có 1 bản canonical nên job là guard-tương-lai, không phải no-op vô nghĩa).
  Copy script sang Lending `.agents/scripts/` để dùng trong harness (so 2 bản nội bộ
  Lending) — không commit bên đó, thuộc phạm vi khác.
- **P4 Pages**: `.nojekyll` (chặn Jekyll build tự động xử lý sai file), README EN/VI thêm
  link "Open the live demo" trỏ thẳng sample HTML qua GitHub Pages — không cần tải 4.3MB.
- **P5**: `CONTRIBUTING.md` (checklist evidence-first, no-fork rule, dependency floor,
  no-secrets) + `.github/pull_request_template.md`; README.vi thêm quy ước "EN là nguồn
  sự thật". Mermaid syntax lint (node+jsdom) — HOÃN, đúng khuyến nghị gốc là điều kiện
  ("đáng làm nếu tần suất viết fence mermaid tăng"), chưa tới ngưỡng.
- P2 (tag v0.1.0 + Release + asset) thực hiện riêng sau khi commit này lên main — xem
  entry kế tiếp.

**Trạng thái**: `Done`.

### 2026-07-18 — Gỡ profiles/lending.md khỏi repo public (kể cả git history)

**Loại**: Security / Compliance (sanitize-before-public)

**Thay đổi**:
- Phát hiện: repo đã chuyển Public nhưng `profiles/lending.md` (mẫu vàng viết tay, đánh
  dấu INTERNAL/sanitize-before-public từ lúc scaffold) chưa được sanitize — chứa tên công
  ty, layout service nội bộ, tên hệ thống đối tác tích hợp, message constants nội bộ, tên
  file tài liệu nội bộ.
- Xử lý: backup nội dung đầy đủ vào Lending repo private (không public), `git rm` khỏi
  working tree, **`git filter-repo` xoá file khỏi TOÀN BỘ git history** (repo mới 13
  commit, 0 star/fork lúc xử lý — rewrite an toàn), force-push.
- SKILL.md bước 4 (mẫu vàng để so chất lượng PROFILE): đổi tham chiếu từ
  `profiles/lending.md` sang `examples/grpc-go/skill/SKILL.md` (public-safe, đã có sẵn).
- Record lịch sử (`changes/bootstrap/*.md`, CHANGELOG entry cũ) giữ nguyên — chỉ nhắc tên
  file, không leak nội dung.

**Trạng thái**: `Done`.

### 2026-07-18 — Đồng bộ định vị mọi-domain vào description/manifest

**Loại**: Docs / Positioning

**Thay đổi**:
- README đã đổi hướng "từ tech đến business" nhưng manifest/description còn thuần dev →
  dò và sửa: marketplace.json (2 description + keywords thêm business-analysis/
  process-documentation/knowledge-graph), plugin.json (description + keywords),
  SKILL.md genesis (frontmatter description thêm audience + trigger "tài liệu hoá quy
  trình từ code cho cả team"; intro thêm đoạn cẩm nang phục vụ cả team),
  installers/prompts (description), core-template.md (description của skill SINH RA —
  mọi project sau này kế thừa: thêm trigger "quy trình này thực sự chạy thế nào" +
  audience BA/PO/PM/QA).
- Nguyên tắc: GIỮ nguyên từ khóa trigger cũ (description điều khiển auto-trigger),
  chỉ bổ sung — không thay thế.
- Verify: JSON parse OK; `claude --plugin-dir ... plugin details` load OK, Skills (1),
  ~353 tok always-on (tăng từ ~243 do description dài hơn).

**Trạng thái**: `Done`.

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
