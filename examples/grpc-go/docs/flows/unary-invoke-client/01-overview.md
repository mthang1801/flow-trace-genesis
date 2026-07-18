---
id: overview
num: '01'
title: Tóm tắt
subtitle: Vòng đời một unary RPC phía client — Invoke → newClientStream → pick → HTTP/2 wire
level: draft
nav: 01 · Tóm tắt
tnav: Tóm tắt
---

| Meta | Giá trị |
| --- | --- |
| Trace | 2026-07-18 · flow-trace (grpc-go) — golden-flow run đầu tiên của skill sinh bởi flow-trace-genesis v0.1.0 |
| Repo & commit | `grpc-go@7d870454 (master)` — `module google.golang.org/grpc`, go 1.25.0 |
| Anchor | `call.go:29` — `ClientConn.Invoke` |
| Trạng thái | Draft — chờ user chấm golden-flow gate |

Generated code (stub `.pb.go`) gọi `cc.Invoke` cho mọi unary RPC. `Invoke` gom call options
rồi đi qua **interceptor chain** (nếu có) trước khi vào `invoke` — hàm này chỉ làm đúng 3
việc: `newClientStream` → `SendMsg(req)` → `RecvMsg(reply)`.

`newClientStream` là nơi nặng nhất: đếm call cho channelz/idleness, validate metadata, **chờ
resolver trả địa chỉ đầu tiên**, hỏi config selector lấy method config (timeout, retry
policy, max size), chọn codec/compressor, rồi tạo **attempt đầu tiên**: qua
`pickerWrapper.pick` (block tới khi balancer có picker sẵn sàng) lấy transport, mở stream
HTTP/2 (`http2Client.NewStream` — header `grpc-timeout` sinh từ deadline).

`SendMsg` marshal + nén + kiểm tra size, **buffer payload cho retry**, rồi ghi frame qua
transport. `RecvMsg` dựng decompressor theo header trả về, decode message, và **đọc thêm một
lần nữa để bắt EOF** (cardinality check). Retry engine bọc mọi op: transparent retry khi
stream chưa được server xử lý, policy retry theo service config (throttling + server
pushback + backoff jitter).

> [!warning] Đặc điểm đáng chú ý nhất
> Với unary RPC, **lỗi ghi xuống transport bị nuốt tại `SendMsg` (trả `nil`)** — lỗi thật chỉ lộ ra ở `RecvMsg` qua status của stream (`stream.go:1147-1153`, comment ghi rõ "because the generated code requires it"). Ai đọc code caller mà tưởng `SendMsg == nil` nghĩa là đã gửi thành công sẽ hiểu sai hoàn toàn semantics.
