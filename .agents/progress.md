# flow-trace-genesis — Progress Dashboard

> Newest first. Giữ compact — chi tiết bền vững nằm trong change records.

## Activity Log

| 2026-07-18 | claude | KG panel kiểu Obsidian + layout 1560px (sync từ Lending); installer thêm target antigravity (`~/.gemini/skills/`) và sửa cursor sang `~/.cursor/skills-cursor/` (Agent Skills native — xác minh trên máy); README viết lại hướng cộng đồng (bỏ project test local). | `installers/`, `README.md`, `plugins/.../render/` |

| 2026-07-18 | claude | Nhận sync tính năng Knowledge Graph từ Lending (không fork): render/ (+kg/extract.py, cytoscape vendored, kg-init.js, build/check mở rộng) + html-render.md (12 section, KG=02, pipeline script-first). Áp cho golden grpc-go: analyze 1:57ph, extract 200 nodes/332 edges, build+check pass. | `plugins/.../render/`, `references/html-render.md` |

| 2026-07-18 | claude | Golden Go chạy end-to-end trên `grpc-go@7d870454`: khảo sát + questionnaire bằng chứng, sinh skill `.claude/skills/flow-trace/` (CORE+PROFILE, stamp Draft, 0 placeholder), trace `unary-invoke-client` (24 bước file:line, 8 failure mode; đắt nhất: SendMsg unary nuốt write error thành nil), build+check pass lần đầu (76302 bytes/11 sections). Chờ user chấm → Verified. | `.agents/changes/golden-go/` |

| 2026-07-17 | claude | Executor gate MỞ ("Specs approved") — thực thi xong 8 bước bootstrap v1: marketplace+plugin manifest, CORE templates, questionnaire+profiles (lending mẫu vàng INTERNAL), SKILL.md 6 bước, command, .mcp.json, installer 4 target, README. Verify: harness pass, JSON OK, render port identical (build golden Lending md5 không đổi), dry-run 4 target OK. Còn 5.2 manual (cài marketplace trong session) chờ user. | `.agents/changes/bootstrap/evidence.md` |
| 2026-07-17 | claude | Amend plan `bootstrap`: thêm bước 2b port nguyên trạng base render md-source→HTML (`render/`: build.py/check.py/base.html/tokens.css/engine.js) từ Lending — base đã verify với golden resubmit-a2 (build+check pass). Gate vẫn đóng. | `.agents/changes/bootstrap/plans.md` |
| 2026-07-17 | claude | Lập plan `bootstrap` v1 (proposal/plans/tasks/evidence): cấu trúc plugin, playbook genesis 6 bước, thứ tự thực thi 8 bước, verification, risks. Executor gate đóng chờ approve. | `.agents/changes/bootstrap/` |
| 2026-07-17 | claude | Commit governance lean `b2dbbf5` (7 file, harness pass + negative-test). | `.agents/` |
| 2026-07-17 | claude | Scaffold governance lean (CLAUDE.md shim, AGENTS.md routing, .agents core rules, changes contract, harness grep-based). | `.agents/` |

## Active Change Registry

| Slug | Status | Mô tả | Tham chiếu |
| --- | --- | --- | --- |
| `golden-go` | Review | Genesis dogfood trên grpc-go xong bước 1-6a; cẩm nang `unary-invoke-client` + skill Draft đã cài. Chờ user chấm golden-flow gate (6b) → Verified. | `.agents/changes/golden-go/` |
| `bootstrap` | Done | v1 hoàn tất 19/19 task. Commit `163d24c` (sản phẩm) + fix 5.2 (dedup command/skill, marketplace schema). Plugin validate trên Claude Code thật: Skills (1), MCP (3). | `.agents/changes/bootstrap/` |

## Execution Queue

1. User chấm golden trace `unary-invoke-client` → đổi stamp Draft→Verified → commit khi yêu cầu.
2. Golden Dni workspace → dogfood regenerate Lending.
3. (Optional) smoke test interactive `/plugin marketplace add` trong session Claude Code.

## Current Risks

| Risk | Mitigation |
| --- | --- |
| Nội dung profile nội bộ (lending/dni/fv) lộ khi repo chuyển public | `plugins/**/profiles/` được đánh dấu sanitize-before-public trong `.agents/AGENTS.md`; tách sẵn từ đầu |
| CORE trong repo này và skill Lending gốc trôi nhau | Dogfood Phase 4: regenerate chính Lending để ép hội tụ |
| Máy đích thiếu uv/pip cho Serena/Docling | Rule degrade-gracefully bắt buộc trong playbook |

## Status Vocabulary

Dùng đúng bảng trong `.agents/AGENTS.md`.
