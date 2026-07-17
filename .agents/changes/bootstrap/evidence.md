# Evidence — bootstrap v1

Status: Done (2026-07-17) — 19/19 task; 5.2 đóng bằng `--plugin-dir` validation + fix lệch.

## Verification 5.2 (fresh, sau fix)

```text
$ claude --plugin-dir <repo>/plugins/flow-trace-genesis plugin details flow-trace-genesis
flow-trace-genesis 0.1.0 · Skills (1) flow-trace-genesis · MCP servers (3) serena, markitdown, docling
Always-on: ~243 tok
```

Lệch đã phát hiện & fix trước khi push:
- Claude Code hợp nhất commands/skills → `commands/flow-trace-genesis.md` trong plugin
  thành skill thứ 2 trùng tên (Skills (2), 305 tok). Fix: `git mv` ra
  `installers/prompts/`, SKILL.md thêm `argument-hint`; installer target `claude` bỏ copy
  command file (guard CMD_DST rỗng).
- marketplace.json: `description` chuyển lên top-level khớp schema marketplace thật đang
  cài trên máy.

## Verification (fresh, 2026-07-17)

```text
$ bash .agents/scripts/governance-harness.sh
[governance] pass

$ python3 -c "json.load x3"          # marketplace.json + plugin.json + .mcp.json
JSON OK x3

$ diff -r <Lending>/.agents/skills/flow-trace/render plugins/.../skills/flow-trace-genesis/render
render copy identical

# Base render trong plugin chạy độc lập — build lại golden flow Lending, output byte-identical:
$ md5sum docs/flows/resubmit-a2.html                 → 67955dc08301170fd6ce38341c024558
$ python3 <plugin>/render/build.py docs/flows/resubmit-a2
✓ built ... (81864 bytes, 11 sections)
$ python3 <plugin>/render/check.py docs/flows/resubmit-a2
✓ check OK: docs/flows/resubmit-a2 (11 sections)
$ md5sum docs/flows/resubmit-a2.html                 → 67955dc08301170fd6ce38341c024558 (không đổi)

$ ./installers/install.sh --target {codex,opencode,cursor,claude} --dry-run
# cả 4 in đúng mapping + danh sách file, không ghi gì
```

## Đã có

- Governance lean + harness: commit `b2dbbf5`.
- Toàn bộ sản phẩm v1 (18 task nhóm 1-4): marketplace + plugin manifest, CORE templates
  (core-template với vùng CORE/PROFILE + placeholder table, report-template, html-render),
  questionnaire Q1-Q10 + _TEMPLATE + profiles/lending.md (INTERNAL mẫu vàng), SKILL.md
  playbook 6 bước, command, .mcp.json, installer 4 target + README, root README.
- `render/` port nguyên trạng — luật "không fork, sửa phải sync ngược Lending" ghi trong
  html-render.md của plugin.

## Chưa làm / chờ

- **5.2 (manual)**: cài thử marketplace trong session Claude Code —
  `/plugin marketplace add /home/mvt/Repositories/plugins/flow-trace-genesis` →
  `/plugin install flow-trace-genesis@flow-trace-genesis-marketplace` → skill
  `flow-trace-genesis` xuất hiện. (CLI `claude plugin` bản này không có install
  non-interactive — đã thử `details`/`--plugin-dir`, không hỗ trợ.)
- Commit: chưa — chờ user yêu cầu (NO AUTO-COMMIT).
- Golden Go (go-core-adapter-service) → change record riêng sau khi v1 được nghiệm thu.
