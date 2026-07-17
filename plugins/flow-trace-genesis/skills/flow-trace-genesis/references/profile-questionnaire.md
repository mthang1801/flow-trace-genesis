# Profile Questionnaire — bộ câu hỏi genesis phải trả lời BẰNG BẰNG CHỨNG

Mỗi câu trả lời bắt buộc kèm ≥1 citation `file:line` đã Read trong phiên khảo sát.
Mục không xác minh được → ghi **"Chưa xác minh"** + đã thử cách gì. **Cấm đoán.**
Kết quả điền vào `profiles/<project>.md` theo khung `_TEMPLATE.md`, rồi map vào các
block `{{PROFILE_*}}` của `core-template.md`.

## Q1 — Service/module markers → `PROFILE_SERVICE_MARKERS`

- Workspace là monorepo / multi-repo / single service? Ranh giới mỗi service/module nằm đâu
  (folder nào, file manifest nào: package.json / go.mod / pom.xml / CMakeLists / rockspec)?
- Ngôn ngữ + framework chính của từng service? Layout layer bên trong (ví dụ
  presentation/application/domain/infrastructure, cmd/internal/pkg, controller/service/dao)?
- Lệnh xác định commit hash/branch từng repo (đường dẫn `.git` ở đâu)?

## Q2 — Transport edges xuyên service → `PROFILE_TRANSPORT_EDGES`

Câu hỏi quan trọng nhất — trả lời sai là trace mù:

- Các service nói chuyện với nhau bằng gì? (message broker / gRPC / REST nội bộ / GraphQL /
  shared DB / file). Liệt kê TỪNG loại tìm thấy.
- Với mỗi loại: **định danh kênh** nằm ở đâu (constant file, proto file, route table,
  topic config)? Producer phát bằng API nào, consumer nhận bằng decorator/handler nào?
- Định danh kênh có bị **copy tay giữa 2 repo** không (mỗi repo一 bản)? Nếu có → luật
  "Read cả hai đầu so từng ký tự" phải vào PROFILE.
- Phân biệt cú pháp **chờ kết quả** (request-reply/sync) vs **không chờ** (fire-and-forget/
  event) — mỗi bên viết thế nào trong code?

## Q3 — DI / indirection nội service → `PROFILE_DI_INDIRECTION`

- Interface/port khai báo ở đâu, implementation ở đâu, binding ở đâu (module providers /
  wire / factory / service locator / build tag)?
- Cách resolve nhanh nhất: grep gì, hay LSP go-to-implementation dùng được?

## Q4 — Event nội bộ → `PROFILE_INTERNAL_EVENTS`

- Có event bus trong process không (EventEmitter, channel, signal/slot, observer)?
  Emit bằng gì, listener đăng ký bằng gì, nối hai đầu bằng grep chuỗi nào?

## Q5 — Frontend chain → `PROFILE_FRONTEND_CHAIN`

- Có FE trong scope không? Nếu có: chuỗi chuẩn page → API client → constant endpoint →
  route backend viết thế nào? Nối route backend ↔ FE bằng grep gì?
- Không có FE → ghi rõ "N/A", Phase 4 của CORE bỏ qua.

## Q6 — Entrypoints & leaf nodes → `PROFILE_LEAF_NODES`

- Các loại biên của flow: HTTP route (khai báo thế nào), cron/scheduler, CLI, consumer từ
  hệ ngoài. Grep pattern cho từng loại.
- Node lá ghi nhận nhưng KHÔNG trace sâu ở v1: DB (ORM nào, entity ở đâu), cache (client
  nào, key pattern), HTTP third-party (client/base URL ở đâu), queue nội bộ (BullMQ/
  sidekiq/celery — producer→processor để v2).

## Q7 — Gotchas & archetype ngôn ngữ → `PROFILE_GOTCHAS`

- Typo/naming trap có thật trong repo (file đặt tên sai chính tả, constant sai tên...)?
- Archetype lỗi đặc thù ngôn ngữ bổ sung vào checklist CORE, ví dụ:
  - JS/TS: guard truthy rỗng ruột (`if (obj)` thay vì `obj.id`), `JSON.stringify` xóa key
    `undefined`, floating promise (gọi async không await).
  - Go: nuốt `err` (`_ =`), goroutine leak, `context.Background()` xuyên request.
  - Java: catch Exception rộng, Optional.get() trần.
  - C++/Lua: tùy codebase — chỉ ghi khi có bằng chứng pattern lặp lại.
- Incident/postmortem có sẵn trong repo để làm ground truth không?

## Q8 — Tool availability (per máy + per ngôn ngữ)

- Evidence tier có gì chạy được NGAY trên máy này: LSP server nào, Serena (uvx), ast-grep,
  ripgrep/grep? (thử chạy thật, ghi version)
- Candidate tier: GitNexus index sẵn chưa? DeepWiki/GitDiagram/Understand-Anything có được
  phép cài không (phải audit trước khi cài — xem safety `.agents/AGENTS.md`)?
- Ingest tier: markitdown MCP / docling có sẵn không?
- Thiếu gì → ghi vào PROFILE mục degrade để trace sau này không loay hoay lại.

## Q9 — Governance & output convention repo đích

- Repo đích có `.agents/` (kiểu Lending) / `.claude/skills/` / không có gì?
  → quyết định nơi đặt skill sinh ra + có cần sync 2 bản không.
- `{{OUTPUT_DIR}}`: mặc định `docs/flows/` — repo đích có chỗ khác hợp lý hơn không?
- Quy ước commit/ngôn ngữ tài liệu của repo đích?

## Q10 — Golden flow đề cử

- Đề xuất 2-3 flow ứng viên cho golden-flow gate (ưu tiên: phủ nhiều loại edge nhất,
  user thuộc nghiệp vụ, có incident/postmortem đối chiếu càng tốt). User chọn 1.
