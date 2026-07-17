# Tasks — bootstrap v1

## 1. Khung phân phối

- [x] 1.1 `.claude-plugin/marketplace.json`
- [x] 1.2 `plugins/flow-trace-genesis/.claude-plugin/plugin.json`

## 2. CORE templates (port + generic hóa từ Lending)

- [x] 2.1 `references/core-template.md` — 5 phase, guardrails, 6 archetype phổ quát,
      vùng CORE/PROFILE đánh dấu regenerate, placeholder table
- [x] 2.2 `references/report-template.md` — 11 section + 6b PRD (generic hóa tên repo)
- [x] 2.3 `references/html-render.md` — theo pipeline md-source (`_doc.yml` + section md)
- [x] 2.3b `skills/flow-trace-genesis/render/` — copy nguyên trạng 5 file từ Lending
      (diff -r identical; build lại golden resubmit-a2 từ bản plugin → md5 không đổi)
- [x] 2.4 `references/profile-questionnaire.md` (Q1-Q10) + `profiles/_TEMPLATE.md`
- [x] 2.5 `references/profiles/lending.md` — mẫu vàng (INTERNAL, sanitize-before-public)

## 3. Genesis playbook

- [x] 3.1 `skills/flow-trace-genesis/SKILL.md` — 6 bước + gates + giới hạn an toàn
- [x] 3.2 `commands/flow-trace-genesis.md`

## 4. Tooling & phân phối

- [x] 4.1 `.mcp.json` — serena + markitdown + docling (ghi chú dependency + degrade)
- [x] 4.2 `installers/install.sh` — codex|opencode|cursor|claude + `--dry-run`
- [x] 4.3 `installers/README.md` — mapping layout + verify per-harness
- [x] 4.4 Root `README.md`

## 5. Verification

- [x] 5.1 Governance harness pass
- [x] 5.2 Validate plugin trên bản Claude Code đang chạy — qua `claude --plugin-dir <plugin>
      plugin details flow-trace-genesis`: load OK, MCP 3 server nhận đủ. Phát hiện + fix lệch:
      (a) commands/ trong plugin bị hợp nhất command/skill → skill trùng tên ×2 → chuyển ra
      `installers/prompts/`, thêm `argument-hint` vào SKILL.md → Skills (1);
      (b) marketplace.json đưa `description` lên top-level khớp schema marketplace đã cài
      trên máy (`~/.claude/plugins/marketplaces/skill-evolver`). Smoke test interactive
      `/plugin marketplace add` (optional) user có thể chạy thêm.
- [x] 5.3 `install.sh --dry-run` đúng cho cả 4 target (codex/opencode/cursor/claude)
- [x] 5.4 Sync progress.md + CHANGELOG.md; grill gate; commit khi user yêu cầu
