---
id: steps
num: '04'
title: Bảng bước — nguồn chân lý
subtitle: Mọi node đều đã được Read trong phiên trace, kèm `file:line` (grpc-go@7d870454)
level: deterministic
nav: 04 · Bảng bước (file:line)
tnav: Bảng bước
---

### Chặng 1 — Entry & stream setup

| # | Package | Bước | File:line | Loại edge | Ghi chú |
|---|---------|------|-----------|-----------|---------|
| S1 | grpc | Generated code gọi `cc.Invoke`; gom call options `combine(cc.dopts.callOptions, opts)` | `call.go:29-32` | call | `combine` cố ý không dùng `append` để tránh share capacity giữa các call song song `call.go:40-53` |
| S2 | grpc | Interceptor chain: nếu `dopts.unaryInt` set thì bọc `invoke` | `call.go:34-36` | call | chain dựng lúc NewClient: `chainUnaryClientInterceptors` `clientconn.go:224,519-525` — `unaryInt` luôn đứng đầu |
| S3 | grpc | `invoke` = `newClientStream` → `SendMsg` → `RecvMsg` | `call.go:65-74` | call | `unaryStreamDesc` (không client/server stream) `call.go:63` |
| S4 | grpc | `newClientStream`: channelz `incrCallsStarted`, idleness `OnCallBegin`, callopt `OnFinish` giảm đếm | `stream.go:214-231` | call | cleanup khi tạo stream fail: `endOfClientStream` defer `stream.go:217-222` |
| S5 | grpc | Validate metadata outgoing (key/pair) → `codes.Internal` nếu sai | `stream.go:233-246` | call | |
| S6 | grpc | **Chờ resolver**: `waitForResolvedAddrs` — RPC đầu tiên block tới khi có địa chỉ | `stream.go:249` → `clientconn.go:759` | call (block) | trả cờ `nameResolutionDelayed` |
| S7 | grpc | Config selector → `MethodConfig` (timeout, retry policy, max size) + interceptor per-RPC nếu có | `stream.go:263-297` | indirection | status code từ control plane bị giới hạn theo gRFC A54 `stream.go:266-273` |
| S8 | grpc | `newClientStreamWithParams`: ctx timeout từ `mc.Timeout`; callopt `before` hooks; max send/recv size; codec | `stream.go:313-334` | call | **context leak được document** `stream.go:308-312` (issue #1818) |
| S9 | grpc | Dựng `callHdr` (authority, method, content-subtype, accepted compressors) + chọn compressor (per-call `UseCompressor` ưu tiên hơn DialOption) | `stream.go:336-364` | call | compressor không đăng ký → `codes.Internal` `stream.go:356-358` |
| S10 | grpc | Nạp `retryThrottler` + binary loggers | `stream.go:385-395` | call | |

### Chặng 2 — Attempt: pick transport & mở stream HTTP/2

| # | Package | Bước | File:line | Loại edge | Ghi chú |
|---|---------|------|-----------|-----------|---------|
| S11 | grpc | Op đầu tiên `getTransport + newStream` chạy qua `withRetry`, gán `cs.attempt` | `stream.go:399-412` | call | op được buffer để replay khi retry `stream.go:412` |
| S12 | grpc | `getTransport` → `pickerWrapper.pick(ctx, failfast, PickInfo)` | `stream.go:515-535` | indirection | drop error từ picker đánh dấu `a.drop` `stream.go:522-525` |
| S13 | grpc | `pick`: loop trên `pickerGen`, **block trên `blockingCh`** tới khi có picker; ctx done → map sang `DeadlineExceeded`/`Canceled` | `picker_wrapper.go:105-174` | goroutine-sync | `ErrNoSubConnAvailable` → loop tiếp :159-161; failfast=false → block tiếp :172-174 |
| S14 | grpc | `csAttempt.newStream`: merge metadata từ PickResult → `t.NewStream` | `stream.go:537-554` | call | `PreviousAttempts` set từ `numRetries` :539 |
| S15 | transport | `http2Client.NewStream(callHdr)`: dựng header fields (`createHeaderFields`), đăng ký stream | `internal/transport/http2_client.go:756`, `:542` | transport | deadline → header `grpc-timeout` `:613` |

### Chặng 3 — Send / Recv / Retry

| # | Package | Bước | File:line | Loại edge | Ghi chú |
|---|---------|------|-----------|-----------|---------|
| S16 | grpc | `SendMsg`: `prepareMsg` (marshal + nén qua codec/compressor), guard `maxSendMessageSize` → `ResourceExhausted` | `stream.go:954-992` | call | unary set `sentLast` ngay :968-970 |
| S17 | grpc | Payload `Ref()` + `withRetry(op)` + `bufferForRetryLocked` giữ payload cho retry | `stream.go:996-1012` | call | không buffer thì free ngay :1010-1012 |
| S18 | grpc | `csAttempt.sendMsg` → `transportStream.Write(hdr, payload, Last: true)` | `stream.go:1138-1155` | transport | ⚠️ **unary: write lỗi → return `nil`** :1148-1153; client-stream: `io.EOF` :1154 |
| S19 | transport | Frame thực sự xuống socket qua goroutine nền: `loopyWriter.run` (ghi) + `t.reader` (đọc) | `internal/transport/http2_client.go:476-479`, `:420` | goroutine | loopy lỗi non-IO → close conn :478-481 |
| S20 | grpc | `RecvMsg`: `withRetry(recvMsg, commitAttemptLocked)`; kết thúc gọi `finish` | `stream.go:1025-1051` | call | commit = từ đây không retry op cũ nữa :1037 |
| S21 | grpc | `recvMsg`: dựng decompressor từ header `RecvCompress` (một lần/stream), check compressor được phép | `stream.go:1169-1187` | call | peer nén bằng thuật toán ngoài danh sách → `codes.Internal` :1179-1181 |
| S22 | grpc | `recv` decode message; `io.EOF` → lấy status từ trailer; **không nhận message nào → cardinality violation** | `stream.go:1189-1202` | call | :1195-1196 |
| S23 | grpc | Unary đọc **lần 2** — phải là EOF; nhận thêm message → cardinality violation | `stream.go:1225-1232` | call | status cuối lấy từ `transportStream.Status()` :1228 |
| S24 | grpc | Retry engine `shouldRetry`: transparent (stream unprocessed) / policy theo `RetryableStatusCodes` + throttle + server pushback `grpc-retry-pushback-ms` + backoff jitter 0.8-1.2 | `stream.go:701-789` | call | max attempts :767-768; disableRetry :721-723 |
