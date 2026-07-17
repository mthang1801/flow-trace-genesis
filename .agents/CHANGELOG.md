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
