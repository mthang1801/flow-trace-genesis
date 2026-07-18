---
id: failure-modes
num: '08'
title: Failure modes
subtitle: Đối chiếu 6 archetype CORE + G1-G5 của PROFILE grpc-go
level: advanced
badge: ARCHETYPE
nav: 08 · Failure modes
tnav: Failure modes
---

| # | Vị trí | Archetype | Kịch bản: input/trạng thái → hậu quả | File:line |
|---|--------|-----------|--------------------------------------|-----------|
| F1 | `csAttempt.sendMsg` | **G1 lỗi hoãn sang chỗ khác** | Conn đứt giữa lúc write: unary `SendMsg` trả **`nil`** (không phải lỗi!) — caller tưởng đã gửi xong; lỗi thật chỉ xuất hiện ở `RecvMsg` qua status của stream. Code đọc `if err := cs.SendMsg(req); err != nil` để "xử lý lỗi gửi" là vô nghĩa với unary | `stream.go:1147-1155` |
| F2 | `newClientStreamWithParams` | **G3 context leak (documented)** | App gọi Invoke nhưng bỏ ngang không đọc kết quả: cancel của child ctx chỉ chạy khi RecvMsg lỗi / SendMsg lỗi / conn đóng — ctx (và timer nếu có timeout) sống lâu hơn cần thiết (issue #1818, comment ngay trong code) | `stream.go:308-323` |
| F3 | `SendMsg` + retry | **G5 / #5 retry giữ payload trong RAM** | Message lớn + retry policy bật: mỗi op được buffer kèm payload (`bufferForRetryLocked`) tới khi commit — nhiều RPC lớn đồng thời retry → memory phình; throttler chỉ hạn chế tần suất retry, không hạn chế size | `stream.go:1006-1012`, `stream.go:764` |
| F4 | `pickerWrapper.pick` | **biến thể #2 — block vô hạn** | Không set deadline + wait-for-ready (failfast=false) + balancer không bao giờ READY: pick block mãi trên `blockingCh`, RPC treo không lỗi — chỉ thoát khi ctx bị cancel từ ngoài | `picker_wrapper.go:111-140,172-174` |
| F5 | `shouldRetry` pushback | **dữ liệu đối tác điều khiển luồng** | Server trả `grpc-retry-pushback-ms` sai định dạng hoặc nhiều giá trị → client abort retry và **đếm như failure cho throttle** — server cấu hình sai làm giảm retry của toàn client | `stream.go:734-747` |
| F6 | transport goroutines | **#2 fire-and-forget (ĐƯỢC XỬ LÝ)** | Frame thực sự ghi bởi loopyWriter goroutine, không phải RPC goroutine; loopy chết vì lỗi non-IO → close conn ngay (:478-481), reader chết → readerErrCh (:420). Ghi nhận: cơ chế lành mạnh, không phải bug — nhưng khi debug "RPC treo" phải nhìn 2 goroutine này | `internal/transport/http2_client.go:420,476-481` |
| F7 | `recvMsg` cardinality | **guard chống server sai** | Server stream trả 0 hoặc >1 message cho unary → client chặn bằng `codes.Internal` cardinality violation thay vì im lặng nhận sai — fail loud, đúng hướng | `stream.go:1195-1197,1225-1232` |
| F8 | `combine` | **G4 slice sharing (ĐÃ PHÒNG)** | Comment giải thích rõ: dùng `append` trên slice còn capacity sẽ share phần tử giữa các call đồng thời → race; code cấp phát mới. Pattern đáng học cho code Go khác | `call.go:40-53` |
