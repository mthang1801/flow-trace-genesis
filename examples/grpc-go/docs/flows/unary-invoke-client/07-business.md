---
id: business
num: '07'
title: Business spec ngược
level: inference
nav: 07 · Business spec ngược
tnav: Business
---

> [!inference] Nhãn suy luận
> Toàn bộ mục này là **[AI suy luận — cần domain owner xác nhận]** — với grpc-go, "domain owner" là gRFC/spec chính thức; chế độ đối chiếu PRD của skill có thể chạy trực tiếp với gRFC A6 (retry), A54 (control plane codes), A31 (config selector).

- **Capability**: cho phép application code thực hiện một unary RPC đồng bộ với semantics đầy đủ: per-method config từ service config (timeout/retry/size — `stream.go:263-297`), interceptor chain (`call.go:34-36`), nén tùy chọn (`stream.go:347-364`), retry an toàn (chỉ khi stream chưa được server xử lý hoặc code retryable — `stream.go:708-719,757-759`).
- **Semantics chờ**: RPC đầu tiên chờ resolver (`stream.go:249`), pick block khi chưa có subchannel READY trừ khi failfast (`picker_wrapper.go:100-104`) — nghĩa là "gọi RPC" ngầm bao gồm "chờ hạ tầng sẵn sàng", không fail ngay.
- **Chuyển trạng thái attempt**: tạo attempt → committed (khi RecvMsg bắt đầu — `stream.go:1037`) hoặc retry (transparent/policy) → finished; `onCommit` báo cho config selector (`stream.go:281`).
- **Ngưỡng/config chi phối**: service config per-method (`MethodConfig`), `disableRetry` DialOption (`stream.go:721`), retry throttler per-ClientConn (`stream.go:386`), env/DialOption về compressor và message size mặc định (`stream.go:330-331`).
- **Điểm cần xác nhận với spec**: (1) hành vi trả `nil` của `SendMsg` unary khi write lỗi có được document ở API contract không (comment nói "generated code requires it" — `stream.go:1148-1151`); (2) cardinality violation trả `codes.Internal` — gRFC nào quy định code này thay vì `Unimplemented`?
