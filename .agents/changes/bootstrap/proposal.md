# Proposal — Bootstrap plugin flow-trace-genesis v1

Status: Open (executor gate ĐÓNG — chờ user approve plans.md)
Date: 2026-07-17

## Problem

Skill `flow-trace` hiện chỉ tồn tại dưới dạng bản viết tay cho workspace Lending
(NestJS/RabbitMQ). Muốn nhân rộng sang project khác (Go/gRPC, Java, C++, Lua...,
monorepo hoặc workspace đa service) phải lặp lại toàn bộ công khảo sát + viết skill
thủ công — không scale, không phân phối được sang máy khác/harness khác.

## Solution

Plugin `flow-trace-genesis` (repo này): lần đầu gặp project lạ, agent chạy playbook
genesis — khảo sát bằng bộ tool phân tier (Evidence: Read/LSP/Serena/ast-grep ·
Candidate: GitNexus/DeepWiki-Open/Understand-Anything/GitDiagram · Ingest:
MarkItDown/Docling) — rồi SINH `flow-trace` local self-contained cho project đó
(CORE + PROFILE, version stamp, regenerate bảo toàn PROFILE, golden-flow gate
Draft→Verified). Phân phối: Claude Code plugin marketplace + installer
Codex/OpenCode/Cursor.

## Impact

- Tạo mới toàn bộ nội dung sản phẩm trong repo này: `.claude-plugin/`,
  `plugins/flow-trace-genesis/` (skill, references, command, .mcp.json),
  `installers/`, `README.md`.
- KHÔNG chạm repo ngoài (Lending, Go, Dni) trong change này — golden runs là các
  change record kế tiếp.

## Out of scope (v1 bootstrap)

- Phase 2-4: golden Go (`go-core-adapter-service`), golden Dni, dogfood regenerate
  Lending — mỗi phase một change record riêng sau khi v1 xong.
- Sanitize + dịch English + chuyển public.
- Engine CLI deterministic (spec sống là SKILL.md, chỉ build khi có nhu cầu CI).
- BullMQ edge coverage (v2 của core, kế thừa từ quyết định Lending).
