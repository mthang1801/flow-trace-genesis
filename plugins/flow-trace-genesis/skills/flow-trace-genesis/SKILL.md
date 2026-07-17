---
name: flow-trace-genesis
description: Lần đầu tiếp cận một project CHƯA có skill flow-trace local — khảo sát codebase (Evidence/Candidate/Ingest tier) rồi SINH skill flow-trace local self-contained cho project đó (CORE + PROFILE, version stamp, golden-flow gate Draft→Verified). Dùng khi user gọi /flow-trace-genesis, muốn "dạy AI trace flow project này", hoặc muốn regenerate CORE của flow-trace đã sinh. KHÔNG dùng khi project đã có flow-trace local và user chỉ muốn trace — khi đó dùng chính skill local.
argument-hint: TARGET_DIR=<path> [PRD=<file>] [ADVISOR=gitnexus|deepwiki|none]
---

# Flow-Trace Genesis — sinh skill flow-trace cho project lạ

Sản phẩm cuối **không phải bản trace**, mà là **một skill `flow-trace` local** nằm trong
project đích: tự đứng được (self-contained), đúng convention project, kèm bộ render
md-source → HTML, và chỉ được coi là xong khi qua golden-flow gate.

## Nguyên tắc sản phẩm (bất biến — trùng `.agents/AGENTS.md` repo này)

1. **Evidence tier**: chỉ nội dung đã Read với `file:line` được thành citation trong
   PROFILE và trong mọi bản trace. Candidate tier (GitNexus/DeepWiki/Understand-Anything/
   GitDiagram) chỉ gợi ý. Ingest tier (MarkItDown/Docling) chỉ convert tài liệu.
2. **CORE/PROFILE**: CORE từ `references/core-template.md` — ghi đè được khi regenerate;
   PROFILE từ questionnaire — regenerate PHẢI bảo toàn.
3. **Degrade gracefully**: máy thiếu tool nào thì ghi rõ và đi tiếp bằng grep + Read,
   không chặn việc, không giả vờ tool đã chạy.
4. **Không ghi đè**: project đã có flow-trace local → chỉ regenerate sau khi show diff
   CORE cũ/mới và user confirm; không confirm thì dừng.

## Playbook 6 bước (mỗi bước có gate — không nhảy cóc)

### Bước 1 — Intake & guard

- Nhận `TARGET_DIR` (bắt buộc), `PRD`/`ADVISOR` (tùy chọn).
- Dò skill flow-trace local có sẵn: `.agents/skills/flow-trace/`, `.claude/skills/
  flow-trace/`, hoặc SKILL.md có stamp `generated-by: flow-trace-genesis`.
  - Có + user muốn trace → dừng, chỉ họ dùng skill local.
  - Có + user muốn nâng cấp → **chế độ regenerate**: đọc stamp version, diff CORE cũ vs
    `core-template.md` hiện tại, show diff, chờ confirm; PROFILE giữ nguyên vùng
    `<!-- PROFILE:BEGIN/END -->`.
  - Chưa có → tiếp bước 2.

### Bước 2 — Khảo sát (đắt, làm 1 lần)

- Detect service/ngôn ngữ/build markers (manifest files, layout folder).
- Kiểm kê tool thật trên máy (chạy thử, không đoán): LSP, Serena (uvx), ast-grep, grep
  variant, GitNexus index, markitdown/docling MCP. Tool bên thứ ba CHƯA cài → audit trước,
  hỏi user trước khi cài (safety rule).
- Chạy Candidate advisor nếu sẵn để lấy bản đồ sơ bộ; đánh dấu mọi output là "ứng viên".
- **Gate**: bản kiểm kê tool + bản đồ service sơ bộ trình user trước khi đào sâu.

### Bước 3 — Điền questionnaire

- Trả lời Q1-Q10 trong `references/profile-questionnaire.md`, mỗi mục có `file:line`
  đã Read. Không xác minh được → "Chưa xác minh" + đã thử gì.
- **Gate**: bảng trả lời trình user duyệt (đặc biệt Q2 transport và Q10 golden flow —
  user phải chọn golden flow, genesis không tự chọn).

### Bước 4 — Sinh skill local

- CORE: copy từ `core-template.md`, điền placeholder, đóng dấu
  `generated-by: flow-trace-genesis v<version> · <date> · status: Draft`.
- PROFILE: từ questionnaire theo `profiles/_TEMPLATE.md` → chèn vào vùng PROFILE.
- Kèm references (`report-template.md`, `html-render.md` đã điền OUTPUT_DIR) và
  **copy nguyên trạng `render/`** (build.py/check.py/base.html/tokens.css/engine.js).
- So chất lượng với mẫu vàng `profiles/lending.md` (mục nào lending có mà PROFILE mới
  trống → tự hỏi đã khảo sát đủ chưa).

### Bước 5 — Cài vào project đích

- Theo governance dò được (Q9): có `.agents/` → đặt `.agents/skills/flow-trace/` (+sync
  `.claude/skills/` nếu repo có quy ước đó); chỉ có `.claude/` → đặt đó; không có gì → hỏi.
- **Liệt kê đầy đủ file sẽ tạo + hỏi confirm TRƯỚC khi ghi.** Không ghi ngoài danh sách.

### Bước 6 — Golden-flow gate (bắt buộc)

- Chạy trace đầu tiên bằng skill VỪA SINH (không phải genesis) trên golden flow user chọn.
- Build + check HTML nếu user muốn.
- User chấm: đạt → sửa stamp `status: Draft` → `Verified`; chưa đạt → sửa PROFILE/CORE
  theo feedback, trace lại. **Genesis không tự kết thúc ở "đã sinh xong file".**

## Giới hạn & an toàn

- Genesis đọc-only với source code project đích; chỉ ghi file skill (bước 5, sau confirm)
  và báo cáo golden flow.
- Không cài đặt tool/dependency mới khi chưa audit + user đồng ý.
- Không commit trong repo đích — bàn giao danh sách file, user tự commit theo quy ước họ.
- Mọi placeholder `{{...}}` phải được điền hoặc xóa — SKILL.md sinh ra không được còn
  placeholder sống (check bằng grep `{{` trước khi bàn giao).
