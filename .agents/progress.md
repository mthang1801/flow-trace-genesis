# flow-trace-genesis — Progress Dashboard

> Newest first. Giữ compact — chi tiết bền vững nằm trong change records.

## Activity Log

| 2026-07-17 | claude | Scaffold governance lean (CLAUDE.md shim, AGENTS.md routing, .agents core rules, changes contract, harness grep-based). | `.agents/` |

## Active Change Registry

| Slug | Status | Mô tả | Tham chiếu |
| --- | --- | --- | --- |
| `bootstrap` | Open | Plan tổng cho plugin v1 (genesis skill, CORE templates, questionnaire, profiles/lending, command, .mcp.json, installer 4 platform). Chưa lập plan — chờ user ra lệnh. | `.agents/changes/bootstrap/` |

## Execution Queue

1. Lập plan `bootstrap` (proposal + plans + tasks) — executor gate đóng cho đến khi user approve.
2. Phase 2-4 (golden Go → Dni → dogfood Lending) chỉ vào queue sau khi plan được duyệt.

## Current Risks

| Risk | Mitigation |
| --- | --- |
| Nội dung profile nội bộ (lending/dni/fv) lộ khi repo chuyển public | `plugins/**/profiles/` được đánh dấu sanitize-before-public trong `.agents/AGENTS.md`; tách sẵn từ đầu |
| CORE trong repo này và skill Lending gốc trôi nhau | Dogfood Phase 4: regenerate chính Lending để ép hội tụ |
| Máy đích thiếu uv/pip cho Serena/Docling | Rule degrade-gracefully bắt buộc trong playbook |

## Status Vocabulary

Dùng đúng bảng trong `.agents/AGENTS.md`.
