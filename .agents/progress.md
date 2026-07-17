# flow-trace-genesis — Progress Dashboard

> Newest first. Giữ compact — chi tiết bền vững nằm trong change records.

## Activity Log

| 2026-07-17 | claude | Executor gate MỞ ("Specs approved") — thực thi xong 8 bước bootstrap v1: marketplace+plugin manifest, CORE templates, questionnaire+profiles (lending mẫu vàng INTERNAL), SKILL.md 6 bước, command, .mcp.json, installer 4 target, README. Verify: harness pass, JSON OK, render port identical (build golden Lending md5 không đổi), dry-run 4 target OK. Còn 5.2 manual (cài marketplace trong session) chờ user. | `.agents/changes/bootstrap/evidence.md` |
| 2026-07-17 | claude | Amend plan `bootstrap`: thêm bước 2b port nguyên trạng base render md-source→HTML (`render/`: build.py/check.py/base.html/tokens.css/engine.js) từ Lending — base đã verify với golden resubmit-a2 (build+check pass). Gate vẫn đóng. | `.agents/changes/bootstrap/plans.md` |
| 2026-07-17 | claude | Lập plan `bootstrap` v1 (proposal/plans/tasks/evidence): cấu trúc plugin, playbook genesis 6 bước, thứ tự thực thi 8 bước, verification, risks. Executor gate đóng chờ approve. | `.agents/changes/bootstrap/` |
| 2026-07-17 | claude | Commit governance lean `b2dbbf5` (7 file, harness pass + negative-test). | `.agents/` |
| 2026-07-17 | claude | Scaffold governance lean (CLAUDE.md shim, AGENTS.md routing, .agents core rules, changes contract, harness grep-based). | `.agents/` |

## Active Change Registry

| Slug | Status | Mô tả | Tham chiếu |
| --- | --- | --- | --- |
| `bootstrap` | Done | v1 hoàn tất 19/19 task. Commit `163d24c` (sản phẩm) + fix 5.2 (dedup command/skill, marketplace schema). Plugin validate trên Claude Code thật: Skills (1), MCP (3). | `.agents/changes/bootstrap/` |

## Execution Queue

1. Golden Go — bãi thử user CHỐT 2026-07-17: `~/Repositories/Go/grpc-go` (đổi từ
   go-core-adapter-service). User chọn 1 flow gRPC họ thuộc → change record mới.
2. Golden Dni → dogfood regenerate Lending.
3. (Optional) smoke test interactive `/plugin marketplace add` trong session Claude Code.

## Current Risks

| Risk | Mitigation |
| --- | --- |
| Nội dung profile nội bộ (lending/dni/fv) lộ khi repo chuyển public | `plugins/**/profiles/` được đánh dấu sanitize-before-public trong `.agents/AGENTS.md`; tách sẵn từ đầu |
| CORE trong repo này và skill Lending gốc trôi nhau | Dogfood Phase 4: regenerate chính Lending để ép hội tụ |
| Máy đích thiếu uv/pip cho Serena/Docling | Rule degrade-gracefully bắt buộc trong playbook |

## Status Vocabulary

Dùng đúng bảng trong `.agents/AGENTS.md`.
