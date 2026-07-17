# PROFILE — {{PROJECT_NAME}}

> Sinh bởi flow-trace-genesis v{{GENESIS_VERSION}} · {{DATE}} · từ questionnaire Q1-Q10.
> Mọi claim trong file này có citation `file:line` đã Read lúc khảo sát.
> File này được chèn vào vùng `<!-- PROFILE:BEGIN/END -->` của SKILL.md sinh ra —
> **regenerate CORE không được đụng nội dung này.**

## PROFILE_SERVICE_MARKERS (Q1)

### Cấu trúc workspace

- <monorepo/multi-repo, ranh giới service, manifest> (`file:line`)
- <ngôn ngữ + framework + layout layer từng service>

## PROFILE_TRANSPORT_EDGES (Q2)

### <Loại transport 1 — ví dụ: message broker X>

- Định danh kênh: <ở đâu> (`file:line`)
- Producer: <API/cú pháp> · Consumer: <decorator/handler>
- Chờ kết quả vs fire-and-forget: <phân biệt thế nào>
- <Có/không copy tay hai đầu — luật so khớp>

## PROFILE_DI_INDIRECTION (Q3)

- <port ở đâu, impl ở đâu, binding ở đâu, resolve bằng gì> (`file:line`)

## PROFILE_INTERNAL_EVENTS (Q4)

- <event bus nội bộ, emit/listen, cách nối> hoặc "N/A — không tìm thấy (đã thử ...)"

## PROFILE_FRONTEND_CHAIN (Q5)

- <chuỗi page → client → constant → route + grep pattern> hoặc "N/A"

## PROFILE_LEAF_NODES (Q6)

- Entrypoints: <route/cron/CLI/consumer — grep pattern từng loại>
- Node lá v1 (ghi nhận, không trace sâu): DB <ORM/entity>, cache <client/key>,
  HTTP third-party <client>, queue <tên — để v2>

## PROFILE_GOTCHAS (Q7)

- <typo/naming trap có thật> (`file:line`)
- Archetype bổ sung cho ngôn ngữ <X>:
  | # | Archetype | Cách nhận diện |
  | --- | --- | --- |
- Ground truth đối chiếu: <postmortem/incident doc nếu có>

## Tool availability trên máy khảo sát (Q8)

| Tier | Tool | Trạng thái (version / thiếu) |
| --- | --- | --- |
| Evidence | ... | |
| Candidate | ... | |
| Ingest | ... | |

## Governance & output (Q9)

- Skill đặt tại: <đường dẫn> · Sync: <có/không, đi đâu>
- OUTPUT_DIR: <giá trị>
- Quy ước khác: <commit/ngôn ngữ>

## Golden flow (Q10)

- Ứng viên: <2-3 flow + lý do> · User chọn: <flow> → điền `{{GOLDEN_FLOW}}`
