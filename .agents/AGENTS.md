# .agents — Luật lõi cho flow-trace-genesis (bản lean)

Cutoff từ governance Lending: giữ luật, bỏ bộ máy (không role cards, không SKILL-MAP,
không superpowers adapters). Một người, một mục đích — governance tương xứng.

## Universal Safety Rules

- **NO AUTO-COMMIT**: KHÔNG `git commit` / `git push` khi user chưa yêu cầu rõ.
- **NO AUTO-PUBLISH**: KHÔNG publish plugin, tạo release, đổi visibility repo tự ý.
- **USER CONFIRMATION** cho hành động phá hủy hoặc hướng ra ngoài (ghi file vào repo
  khác, cài tool vào máy, đổi cấu hình global).

### Restricted Commands (cần user duyệt trước)

- GROUP 1 — cực nguy hiểm: `rm -rf`, `rm -r`, `rm`, `unlink`, `shred`
- GROUP 2 — nguy hiểm cao: `rmdir`, `cp --remove-destination`
- GROUP 4 — gián tiếp: `mv`, `install`, script cài đặt bên thứ ba chưa audit

## Commit Message Rules

- Conventional Commits: `<type>(<scope>): <subject>` — scope theo vùng
  (`genesis`, `core`, `installer`, `profile-lending`, `agents`...).
- **CO-AUTHOR bắt buộc**: kết thúc commit body bằng trailer tương ứng harness thực hiện:
  - `Co-authored-by: Claude <noreply@anthropic.com>` hoặc
  - `Co-authored-by: Codex <noreply@openai.com>`
- Chỉ commit khi user yêu cầu (xem NO AUTO-COMMIT).

## Core Workflow

1. **Đọc context trước khi làm**: file này, `.agents/progress.md`,
   `.agents/changes/README.md`, và change record đang active.
2. **Scaffold change**: việc có ý nghĩa tạo `.agents/changes/<slug>/` gồm
   `proposal.md`, `plans.md`, `tasks.md`, `evidence.md` (design.md tùy chọn).
3. **Approval — Executor gate**: KHÔNG viết nội dung sản phẩm (skill, template,
   installer, command) trước khi user duyệt plan bằng "Specs approved" hoặc
   "approve". Gate đóng = chỉ được sửa artifact planning.
4. **Implementation**: thực thi theo plans.md; cập nhật `tasks.md` + `evidence.md`
   theo tiến độ; mọi claim hoàn thành phải có bằng chứng fresh (lệnh + output).
5. **Verification**: chạy `bash .agents/scripts/governance-harness.sh` khi chạm
   `.agents/`/`AGENTS.md`/`CLAUDE.md`; golden-flow gate cho sản phẩm genesis
   (skill sinh ra chỉ `Verified` sau khi user chấm 1 flow đạt).
6. **Grill gate sau hoàn thành**: kết thúc việc có ý nghĩa bằng tóm tắt
   (việc đã xong, bằng chứng, file thay đổi, blocker) + nêu next executable item
   + MỘT câu hỏi kèm recommended answer. Không tự chạy item kế tiếp khi chưa
   được duyệt.
7. **Sync sổ sách**: sau checkpoint có ý nghĩa, cập nhật `.agents/progress.md`
   và thêm entry `.agents/CHANGELOG.md`.

## Nguyên tắc sản phẩm (áp cho nội dung plugin)

- **Evidence tier bất biến**: node/claim vào báo cáo flow-trace phải qua Read +
  `file:line`; graph/wiki/LLM-generated (GitNexus, DeepWiki, Understand-Anything)
  chỉ là Candidate — không bao giờ thành citation.
- **CORE/PROFILE split**: CORE regenerate được ghi đè; PROFILE của project đích
  phải được bảo toàn khi regenerate.
- **Degrade gracefully**: playbook kiểm tra tool có sẵn (Serena/Docling/markitdown/LSP);
  thiếu thì fallback grep/Read và ghi rõ đã degrade — không fail cứng, không giả vờ.
- **Sanitize trước public**: `plugins/**/profiles/` chứa convention nội bộ
  (lending, dni, fv...) — không được lộ khi repo chuyển public.

## Status Vocabulary

| Status | Ý nghĩa |
| --- | --- |
| `Open` | Đã lên kế hoạch, chưa bắt đầu. |
| `In Progress` | Đang làm. |
| `Blocked` | Kẹt, cần gỡ blocker nêu rõ. |
| `Review` | Chờ user review/nghiệm thu. |
| `Done` | Xong, có bằng chứng verification liên kết. |
| `Parked` | Chủ động hoãn. |
| `Canceled` | Không làm nữa. |
