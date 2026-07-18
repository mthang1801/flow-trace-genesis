---
description: Khảo sát project đích rồi sinh skill flow-trace local — biến flow trong code thành cẩm nang từ tech đến business cho cả dev lẫn BA/PO/PM/QA (CORE+PROFILE, golden-flow gate)
argument-hint: TARGET_DIR=<path> [PRD=<file>] [ADVISOR=gitnexus|deepwiki|none]
---

Thực thi skill `flow-trace-genesis` theo đúng playbook 6 bước trong SKILL.md của plugin.

Tham số từ `$ARGUMENTS`:

- `TARGET_DIR` (bắt buộc): root project/workspace đích.
- `PRD` (tùy chọn): tài liệu nghiệp vụ — convert qua MarkItDown/Docling trước khi đọc,
  dùng làm ngữ cảnh Q10 (chọn golden flow) và chế độ đối chiếu PRD của skill sinh ra.
- `ADVISOR` (tùy chọn): ép dùng/bỏ Candidate advisor. Mặc định: dùng cái gì sẵn có.

Ràng buộc phải giữ nguyên (không được nới):

1. Dò flow-trace local trước — có rồi thì KHÔNG ghi đè khi chưa show diff + user confirm.
2. Mỗi câu trả lời questionnaire kèm `file:line` đã Read; không xác minh được → "Chưa xác minh".
3. Gate ở bước 2, 3, 5 (trình user), bước 6 (user chấm golden flow) — không nhảy cóc.
4. Liệt kê file sẽ ghi + confirm trước khi ghi vào repo đích; không commit hộ.
5. SKILL.md sinh ra: stamp `generated-by`, vùng CORE/PROFILE đánh dấu rõ, không còn `{{placeholder}}`.
