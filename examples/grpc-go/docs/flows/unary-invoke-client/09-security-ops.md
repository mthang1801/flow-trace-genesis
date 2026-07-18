---
id: security-ops
num: '09'
title: Security & Ops
level: inference
nav: 09 · Security & Ops
tnav: Security
---

> [!inference] Nhãn suy luận
> Toàn bộ mục này là **[AI suy luận — cần domain owner xác nhận]**.

- **Credentials**: per-call creds gắn qua CallOption vào `callHdr.Creds` (`stream.go:365-367`); transport-level creds nằm ngoài phạm vi trace này (thuộc Dial path). Không thấy creds bị log trong nhánh đã trace.
- **Dữ liệu nhạy cảm**: khi **binarylog** bật, toàn bộ header + message (materialized) được log (`stream.go:416-427,1013-1021,1038-1046`) — môi trường có PII phải kiểm soát sink của binarylog. **Stats handlers** cũng nhận nguyên payload (`stream.go:1156-1158,1211-1220`) — plugin observability tự viết là điểm rò rỉ tiềm năng.
- **Retry/timeout**: timeout per-method từ service config ép vào ctx (`stream.go:313-318`) và truyền xuống wire qua header `grpc-timeout` (`internal/transport/http2_client.go:613`) — server biết deadline của client. Retry có throttling per-ClientConn + server pushback + jitter 0.8-1.2 (`stream.go:764,772-782`) — thiết kế chống retry storm sẵn.
- **Idempotency**: transparent retry chỉ khi stream **Unprocessed** (server chưa chạy handler — `stream.go:712-719`) nên an toàn; policy retry theo `RetryableStatusCodes` do người vận hành khai trong service config — khai code không idempotent (ví dụ retry trên `UNKNOWN`) là tự chuốc double-execution, thư viện không chặn hộ.
