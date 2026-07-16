# Change Records — Contract (lean)

Mỗi việc có ý nghĩa = một thư mục `.agents/changes/<slug>/`:

| File | Vai trò | Bắt buộc |
| --- | --- | --- |
| `proposal.md` | Vấn đề, giải pháp, impact, out-of-scope | ✅ |
| `plans.md` | Nguồn sự thật trước khi thực thi — quyết định, bước, risk, verification | ✅ |
| `tasks.md` | Checklist phân rã, tick theo tiến độ | ✅ |
| `evidence.md` | Trạng thái + bằng chứng verification (lệnh + output), blocker | ✅ |
| `design.md` | Diagram/data flow | Tùy chọn |

Quy tắc:

- Status dùng đúng Status Vocabulary trong `.agents/AGENTS.md`.
- Executor gate: `plans.md` chưa được user approve → không viết nội dung sản phẩm.
- `evidence.md` chỉ được ghi `Done` khi có bằng chứng fresh; golden-flow gate ghi rõ
  ai chấm, ngày, kết quả.
- Mỗi checkpoint: sync `.agents/progress.md` (dashboard) + `.agents/CHANGELOG.md`
  (entry chi tiết). Chi tiết bền vững nằm ở change record, dashboard giữ compact.
