---
id: code-review
num: '10'
title: Ghi chú code review
subtitle: Quan sát dọc đường trace — không phải review toàn diện
level: basic
nav: 10 · Code review
tnav: Code review
---

- `combine()` kèm comment giải thích race — mẫu tốt về "comment nói lý do, không nói cái gì" (`call.go:40-53`).
- TODO còn treo: check size theo `len(data)` thay vì payload (`stream.go:989`); API merge metadata.MD vào outgoing context chưa có (`stream.go:546-553`).
- Top-level `Invoke` deprecated vẫn export cho tương thích (`call.go:55-61`).
- Semantics `SendMsg` unary (trả nil khi write lỗi) chỉ được giải thích bằng comment nội bộ (`stream.go:1148-1151`) — đáng được nêu trong doc comment public của `SendMsg`.
- Cardinality violation checks (`stream.go:1195-1197,1225-1232`) là hardening tương đối mới — message lỗi rõ ràng, dễ grep.
- `newClientStreamWithParams` dài (~120 dòng setup) nhưng tuyến tính, mỗi block có comment — đọc được; phần retry (`withRetry`/`shouldRetry`/buffer replay) là vùng phức tạp nhất, xứng đáng có diagram riêng nếu trace sâu (v2).
