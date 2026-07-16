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
