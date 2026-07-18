---
id: knowledge-graph
num: '02'
title: Knowledge graph (máy sinh)
subtitle: Subgraph flow-scoped từ GitNexus — seeds là các symbol trong bảng bước
level: basic
badge: CANDIDATE
nav: 02 · Knowledge graph
tnav: KG
---

> [!warn] Candidate tier — máy sinh, không phải bằng chứng
> Graph này do `render/kg/extract.py` sinh từ index GitNexus của grpc-go (k-hop ≤2 quanh seeds), KHÔNG qua Read từng edge. Node/cạnh **sáng + nét liền** = trùng seeds lấy từ bảng bước (đã Read, có `file:line` ở section 04); phần **mờ + nét đứt** = ứng viên máy gợi ý — muốn dùng làm căn cứ phải Read xác nhận trước.

```kg
```

Ghi chú phạm vi: single-repo (`grpc-go`); seeds là xương sống unary Invoke path (`Invoke`, `newClientStream`, `clientStream`, `csAttempt`, `pickerWrapper`, `http2Client`). Edge sang server-side/wire không có trong graph — xem sequence diagram (section 03) cho ranh giới HTTP/2.
