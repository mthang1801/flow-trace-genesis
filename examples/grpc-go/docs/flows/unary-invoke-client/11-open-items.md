---
id: open-items
num: '11'
title: Chưa xác định / Nhánh chưa trace
level: basic
nav: 11 · Chưa xác định
tnav: Chưa xác định
---

> [!warn] Mục bắt buộc của template
> Mọi liên kết không lần ra được phải nằm ở đây — cấm đoán rồi trình bày như fact.

- **Server-side leg** (`server.go` `processUnaryRPC`, nối bằng full method name): ngoài phạm vi trace này (client-side only theo golden flow user chọn).
- **Resolver/balancer nội bộ** (`ccResolverWrapper`, `balancer_wrapper.go`, quá trình sinh picker): chỉ trace đến điểm nối `pickerWrapper.pick`; đường resolver→balancer→picker update là nhánh riêng.
- **Transport flow control** (controlBuf, loopyWriter internals, BDP, window update): node lá v1 — đã ghi nhận goroutine :420/:476 nhưng không mở hộp.
- **`prepareMsg`/`recv` internals** (`rpc_util.go` framing, header 5-byte): dùng như hộp đen qua call site `stream.go:973,1189`; chưa Read file.
- **Dial path** (`NewClient`, resolver build lần đầu, idle manager exit-idle): điểm chạm duy nhất đã trace là `waitForResolvedAddrs` (`stream.go:249` → `clientconn.go:759` — chưa Read thân hàm).
- **Nhánh streaming RPC** (client/server streams, `CloseSend` :1054-1067): khác semantics unary đáng kể — flow riêng.
