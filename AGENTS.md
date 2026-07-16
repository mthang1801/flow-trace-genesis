# flow-trace-genesis — Agent Routing Entrypoint

Repo này chứa plugin `flow-trace-genesis`: global skill sinh ra `flow-trace` local
chuyên biệt cho từng project (Claude Code plugin + installer cho Codex/OpenCode/Cursor).

Governance của repo này là **bản lean tự chứa** — không dùng chung `.agents/` của
workspace Lending hay bất kỳ project nào khác.

## Default Route

Khi nhận prompt không tầm thường:

1. Đọc `.agents/AGENTS.md` — luật lõi (safety, commit, workflow, gates).
2. Đọc `.agents/progress.md` — trạng thái đang chạy.
3. Công việc có ý nghĩa đi qua change record `.agents/changes/<slug>/`
   (proposal → plans → approval → tasks/evidence) theo contract trong
   `.agents/changes/README.md`.
4. Xác minh governance bằng `bash .agents/scripts/governance-harness.sh` sau mỗi
   thay đổi chạm vào `.agents/`, `AGENTS.md`, `CLAUDE.md`.

## Bypass planning

Chỉ khi user viết rõ một trong các directive: `no planning`, `skip planning`,
`fast`, `quick`, `direct`, `không cần planning`, `bỏ qua planning`, `làm nhanh`,
`xử lý trực tiếp`. Bypass không vô hiệu hóa safety rules và commit rules.

## Workspace Boundaries

- Repo độc lập, git remote: `github.com/mthang1801/flow-trace-genesis`.
- Sản phẩm plugin nằm dưới `plugins/flow-trace-genesis/` (skills, commands, .mcp.json);
  installer nằm dưới `installers/`. KHÔNG trộn artifact governance (`.agents/`) vào
  nội dung plugin phân phối cho user.
- Bãi thử golden flow (go-core-adapter-service, Dni, Lending) nằm NGOÀI repo này —
  không ghi gì vào các repo đó khi chưa được user duyệt.

## Safety

- KHÔNG tự ý `git commit`, `git push`, publish, release — chỉ khi user yêu cầu rõ.
- Lệnh phá hủy (`rm -rf`, `rm`, `mv`, ghi đè hàng loạt) phải được user xác nhận trước.
- Không ghi đè `flow-trace` local có sẵn của project đích khi chưa diff + confirm.
