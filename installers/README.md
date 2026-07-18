# Installers — mapping layout từng harness

Claude Code là đường chính (marketplace — xem README gốc). Script này cho các harness còn
lại: copy skill + command vào layout mặc định của từng bên. **Layout các harness đổi khá
nhanh** — v1 chủ đích chỉ copy-file + bảng mapping này, không abstract hóa sớm.

```bash
./installers/install.sh --target codex --dry-run   # xem sẽ ghi gì, không ghi
./installers/install.sh --target codex             # ghi thật
```

| Target | Skill copy tới | Command/prompt copy tới | Cách harness nhận |
| --- | --- | --- | --- |
| `claude` | `~/.claude/skills/flow-trace-genesis/` | (không copy — SKILL.md tự là `/flow-trace-genesis`, Claude Code đã hợp nhất command/skill; copy thêm command file sẽ tạo skill trùng tên) | Skill user-global (dùng khi không muốn marketplace) |
| `codex` | `~/.codex/skills/flow-trace-genesis/` | `~/.codex/prompts/flow-trace-genesis.md` | Prompt `/flow-trace-genesis`; trỏ skill từ `~/.codex/AGENTS.md` nếu bản Codex chưa tự đọc skills dir |
| `opencode` | `~/.config/opencode/skills/flow-trace-genesis/` | `~/.config/opencode/commands/flow-trace-genesis.md` | Command custom; wire skill qua AGENTS.md/config nếu cần |
| `cursor` | `~/.cursor/skills-cursor/flow-trace-genesis/` | `~/.cursor/commands/flow-trace-genesis.md` | Cursor Agent Skills (native, cùng format SKILL.md) — Cursor tự nhận theo description |
| `antigravity` | `~/.gemini/skills/flow-trace-genesis/` | (không copy) | Antigravity đọc global rules `~/.gemini/GEMINI.md` — thêm dòng `@./skills/flow-trace-genesis/SKILL.md` vào đó (script chỉ in hướng dẫn, không tự sửa file của bạn) |

## Verify sau khi cài (per-harness)

1. Mở harness, gọi `/flow-trace-genesis` (hoặc paste nội dung command file) trên một project
   thử — playbook phải chạy từ Bước 1 (intake, dò flow-trace local).
2. Skill folder phải đủ: `SKILL.md`, `references/` (core-template, report-template,
   html-render, profile-questionnaire, profiles/), `render/` (build.py, check.py,
   templates/, assets/).
3. `python3 <skill>/render/build.py --help` chạy được (cần python3 + PyYAML).

## Doctor — kiểm kê & cài tool phụ trợ

```bash
./installers/doctor.sh            # scan read-only: tool × tier (required/trace/optional) × mất gì × lệnh fix
./installers/doctor.sh --install  # cài interactive tool user-space (pip --user / npm -g), y/N từng tool
```

- Exit code 0 = đủ tool required (python3 + PyYAML); 1 = thiếu required — dùng được cho
  smoke test/CI.
- KHÔNG bao giờ tự `sudo`: package hệ thống (python3, ripgrep, nodejs, gopls) chỉ in lệnh
  đúng cho package manager của máy (dnf/apt/pacman/zypper/brew) để user tự chạy.
- Agent/skill không tự chạy doctor `--install` — bước Khảo sát chỉ trỏ user tới script.

## Ghi chú

- Script KHÔNG xóa gì; cài đè lên bản cũ chỉ ghi đè file trùng tên.
- MCP bundle (serena/markitdown/docling) không tự cài — cấu hình theo
  `plugins/flow-trace-genesis/.mcp.json`, mỗi harness có cách khai báo MCP riêng.
- Repo private: cài bằng `git clone git@github.com:mthang1801/flow-trace-genesis.git`
  rồi chạy script từ trong repo.
