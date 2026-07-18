---
id: validation
num: '06'
title: Validation & Rules
level: deterministic
nav: 06 · Validation & Rules
tnav: Validation
---

| Tầng | Vị trí | Rule | File:line |
|------|--------|------|-----------|
| Metadata | `newClientStream` | Key/value outgoing metadata phải hợp lệ → `codes.Internal` | `stream.go:233-246` |
| Control plane | config selector | Status code từ control plane bị giới hạn danh sách gRFC A54, code lạ → `codes.Internal` | `stream.go:266-273` |
| Deadline | `newClientStreamWithParams` | `mc.Timeout` (service config) ép `context.WithTimeout` cho toàn RPC | `stream.go:313-318` |
| Size | `SendMsg` | payload sau nén > `maxSendMessageSize` → `codes.ResourceExhausted` | `stream.go:990-992` |
| Size | `recvMsg` → `recv` | decode bị chặn bởi `maxReceiveMessageSize` | `stream.go:1189` |
| Compression | `newClientStreamWithParams` | `UseCompressor` chỉ định compressor chưa đăng ký → `codes.Internal` | `stream.go:353-360` |
| Compression | `recvMsg` | Peer nén response bằng thuật toán ngoài `AcceptCompressors` → `codes.Internal` | `stream.go:1179-1181` |
| Cardinality | `recvMsg` | Unary không nhận được message nào (EOF + status OK) → `codes.Internal` "cardinality violation" | `stream.go:1195-1197` |
| Cardinality | `recvMsg` | Unary nhận >1 message (recv lần 2 không phải EOF) → `codes.Internal` | `stream.go:1225-1232` |
| Pick | `pickerWrapper.pick` | ctx hết hạn khi chờ picker → map đúng `DeadlineExceeded`/`Canceled` kèm lỗi balancer gần nhất | `picker_wrapper.go:123-136` |
| Retry | `shouldRetry` | Chỉ retry code thuộc `RetryableStatusCodes`; throttle đếm fail; `MaxAttempts` chặn trần; pushback sai định dạng → abort | `stream.go:757-768,734-747` |
| Lifecycle | `SendMsg` | Gọi sau `CloseSend` → `codes.Internal` "SendMsg called after CloseSend" | `stream.go:965-967` |
