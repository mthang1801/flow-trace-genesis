# Plan — golden-go: dogfood genesis trên grpc-go

Status: Open — đang thực thi theo playbook 6 bước của plugin (user chốt bãi thử
`~/Repositories/Go/grpc-go` và golden flow "unary RPC client-side (Invoke path)" 2026-07-17).

## Mục tiêu

Chạy genesis end-to-end lần đầu trên project Go thật → sinh `flow-trace` local cho grpc-go
→ trace golden flow → user chấm → Verified. Đây là nghiệm thu sản phẩm v0.1.0.

## Các bước (theo playbook)

1. [x] Intake: `grpc-go @ 7d870454 (master)`, working tree sạch, KHÔNG có flow-trace local
   (không `.agents/`, không `.claude/`).
2. [x] Khảo sát + tool inventory (chạy thật): gopls có (`~/go/bin/gopls` + plugin gopls-lsp),
   uvx có (serena khả dụng), GNU grep 3.12 tại /usr/bin/grep, KHÔNG có ast-grep/rg,
   python3 + PyYAML OK.
3. [x] Questionnaire Q1-Q10 với bằng chứng file:line (xem evidence.md).
4. [x] Sinh skill: CORE (core-template điền placeholder) + PROFILE grpc-go + render/ copy.
5. [x] Cài vào grpc-go — user chọn `.claude/skills/flow-trace/` + OUTPUT_DIR `docs/flows/`
   qua AskUserQuestion (gate confirm 2026-07-18); không còn placeholder sống.
6. [~] Golden-flow gate: trace `unary-invoke-client` XONG (11 section, build 76302 bytes +
   check pass) — CHỜ USER CHẤM để Draft→Verified.

## Điểm cần user quyết ở gate 5

- Vị trí skill trong grpc-go (không có governance sẵn): đề xuất `.claude/skills/flow-trace/`.
- OUTPUT_DIR cẩm nang: đề xuất `docs/flows/` (grpc-go có `Documentation/` nhưng đó là docs
  upstream — không trộn).
