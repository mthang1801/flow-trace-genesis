# Proposal — golden-go

**Ngày**: 2026-07-18 · **Yêu cầu**: user chốt bãi thử `~/Repositories/Go/grpc-go` và golden
flow "unary RPC client-side (Invoke path)".

Nghiệm thu sản phẩm v0.1.0 bằng lần chạy genesis end-to-end đầu tiên trên project Go thật:
khảo sát → questionnaire bằng chứng → sinh skill local → cài có confirm → golden trace →
user chấm. Thành công = skill grpc-go đổi được stamp Draft→Verified và cẩm nang
`unary-invoke-client` đạt chuẩn chất lượng golden `resubmit-a2` bên Lending.

Out of scope: server-side leg, streaming RPC, dial path — flow riêng sau này.
