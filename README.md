# flow-trace-genesis

Plugin Claude Code (kèm installer cho Codex/OpenCode/Cursor): lần đầu gặp một project lạ,
nó **khảo sát** codebase rồi **sinh ra skill `flow-trace` local** cho chính project đó —
skill trace end-to-end business flow xuyên service, xuất cẩm nang md-source + HTML
self-contained.

> Đúc từ skill `flow-trace` viết tay cho workspace Lending (nghiệm thu golden flow
> `resubmit-a2`, 2026-07-17). Repo private-first — `plugins/**/profiles/` chứa convention
> nội bộ, phải sanitize trước khi public.

## Cài đặt

**Claude Code (đường chính — marketplace):**

```text
/plugin marketplace add mthang1801/flow-trace-genesis   # hoặc đường dẫn clone local
/plugin install flow-trace-genesis@flow-trace-genesis-marketplace
```

**Codex / OpenCode / Cursor:**

```bash
git clone git@github.com:mthang1801/flow-trace-genesis.git
cd flow-trace-genesis
./installers/install.sh --target codex --dry-run    # xem trước
./installers/install.sh --target codex              # codex|opencode|cursor|claude
```

## Dùng

```text
/flow-trace-genesis TARGET_DIR=/path/to/project [PRD=/path/to/doc.pdf] [ADVISOR=none]
```

Playbook 6 bước, mỗi bước có gate (chi tiết: `plugins/flow-trace-genesis/skills/flow-trace-genesis/SKILL.md`):

1. **Intake** — dò flow-trace local có sẵn; có thì chuyển chế độ regenerate (diff + confirm).
2. **Khảo sát** — detect service/ngôn ngữ; kiểm kê tool thật trên máy; degrade gracefully.
3. **Questionnaire** — Q1-Q10, mỗi câu trả lời kèm bằng chứng `file:line` đã Read.
4. **Sinh skill** — CORE (từ template, stamp `generated-by`) + PROFILE (từ questionnaire)
   + bộ render md-source→HTML.
5. **Cài vào project đích** — theo governance dò được; liệt kê file + confirm trước khi ghi.
6. **Golden-flow gate** — trace thật 1 flow user chọn, user chấm đạt mới `Draft` → `Verified`.

## Kiến trúc

- **CORE/PROFILE**: CORE là thuật toán trace 5 phase + guardrails + archetype phổ quát —
  regenerate ghi đè được; PROFILE là convention riêng project (transport, DI, FE chain,
  gotchas) — regenerate bảo toàn. Version stamp trong SKILL.md sinh ra.
- **Tool tiers**: Evidence (Read/LSP/Serena/ast-grep — được thành citation) · Candidate
  (GitNexus/DeepWiki/Understand-Anything/GitDiagram — chỉ gợi ý) · Ingest (MarkItDown/
  Docling — convert tài liệu). Thiếu tool → degrade xuống grep + Read, không chặn việc.
- **Render**: `skills/flow-trace-genesis/render/` — build md-source (`_doc.yml` + section
  md) thành HTML self-contained (không CDN/font ngoài), kèm gate `check.py`. Port nguyên
  trạng từ bản Lending, không fork.

## Cấu trúc repo

```text
.claude-plugin/marketplace.json      # marketplace cho Claude Code
plugins/flow-trace-genesis/
├── .claude-plugin/plugin.json
├── skills/flow-trace-genesis/       # SKILL.md (kiêm /flow-trace-genesis) + references/ + render/
└── .mcp.json                        # serena + markitdown + docling (optional, degrade được)
installers/                          # install.sh + mapping per-harness
└── prompts/flow-trace-genesis.md    # prompt cho Codex/OpenCode/Cursor (ngoài plugin surface)
.agents/                             # governance nội bộ repo này (lean, tự chứa)
```

## Security notes

- Genesis đọc-only với project đích; chỉ ghi file skill sau khi liệt kê + confirm.
- Không tự cài tool bên thứ ba — audit + hỏi user trước.
- Không commit hộ vào repo đích.
- `profiles/lending.md` (và các profile nội bộ sau này) là INTERNAL — sanitize trước khi
  repo chuyển public.

## License

Apache-2.0.
