# Evidence — golden-go (đang chạy)

## Bước 1-2 (2026-07-18)

- `git -C ~/Repositories/Go/grpc-go rev-parse --short HEAD` → `7d870454`, branch `master`,
  status sạch. `go.mod`: `module google.golang.org/grpc`, `go 1.25.0`.
- Không có `.agents/`, `.claude/`, không SKILL.md nào trong repo → chế độ sinh mới.
- Tool: gopls `~/go/bin/gopls` (+ plugin gopls-lsp cache Claude), uvx `~/.local/bin/uvx`,
  `/usr/bin/grep` = GNU grep 3.12 (⚠️ khác ghi nhận cũ "ugrep 7.5.0" trong profile Lending —
  môi trường đã đổi), không ast-grep/rg. PyYAML OK.

## Bước 3 — Questionnaire (bằng chứng đã Read, grpc-go @ 7d870454)

- Q1: single-repo Go library; root = public API (`call.go`, `stream.go`, `clientconn.go`),
  `internal/` = private impl (transport...), sub-package theo domain (resolver/ balancer/
  encoding/ credentials/).
- Q2 (transport): không có message broker — "xuyên service" = HTTP/2 wire.
  `internal/transport/http2_client.go`: `NewStream` :756, `write` :1106, reader goroutine
  :420, loopyWriter :476-479. Correlation key = full method name (`callHdr.Method`).
- Q3 (indirection): registry pattern qua global map + `init()`:
  `resolver.Register/Get` resolver/resolver.go:54/61 · `balancer.Register/Get`
  balancer/balancer.go:58/84 · `encoding.RegisterCodec/GetCodec` encoding/encoding.go:132/147
  (đăng ký từ `encoding/proto/proto.go:35 init()`). Functional options: `dialoptions.go:70,589`;
  interceptor chain `clientconn.go:224,519-525`.
- Q4 (event nội bộ): connectivity state (`GetState` clientconn.go:336, `WaitForStateChange`
  :710); picker update qua `blockingCh` picker_wrapper.go:111-140.
- Q5: FE N/A (library).
- Q6: entrypoint = public API (`ClientConn.Invoke` call.go:29 — generated code gọi);
  leaf = net.Conn/framer (transport), channelz, binarylog, stats handler.
- Q7 (gotchas Go, có bằng chứng):
  - Context leak ĐƯỢC DOCUMENT trong code: stream.go:308-312 (issue #1818).
  - `combine()` tránh append-capacity sharing race: call.go:40-53.
  - SendMsg nuốt transport error thành `io.EOF`, lỗi thật chỉ lộ ở RecvMsg: stream.go:955-963.
  - `CloseSend` chủ đích nuốt lỗi write: stream.go:1060-1067.
  - Retry buffer giữ payload trong RAM (`bufferForRetryLocked` stream.go:1007) +
    retryThrottler stream.go:764.
- Q8: xem bước 2.
- Q9: không governance → hỏi user (gate 5).
- Q10: user chốt golden flow = **unary RPC client-side (Invoke path)**. Xương sống đã xác
  nhận: `Invoke` call.go:29-38 (interceptor) → `invoke` :65-74 (newClientStream → SendMsg →
  RecvMsg) → `newClientStream` stream.go:213-300 (idleness, metadata validate,
  waitForResolvedAddrs :249, configSelector :264) → `newClientStreamWithParams` :302 →
  `withRetry`/`newAttemptLocked` :831/:454 → `getTransport` :515-535 → `pickerWrapper.pick`
  picker_wrapper.go:105-174 → `csAttempt.sendMsg` stream.go:1138 / `recvMsg` :1162 →
  `http2Client.NewStream/write` :756/:1106.

## Bước 4-6 (2026-07-18)

- Gate 5: user chốt `.claude/skills/flow-trace/` + `docs/flows/` (AskUserQuestion).
- Skill sinh tại `grpc-go/.claude/skills/flow-trace/`: SKILL.md (stamp
  `generated-by: flow-trace-genesis v0.1.0 · 2026-07-18 · status: Draft`, vùng CORE/PROFILE,
  PROFILE 9 mục + bảng gotchas G1-G5), references (report-template + html-render đã điền
  OUTPUT_DIR/skill-dir), render/ copy nguyên trạng. `grep '{{'` = 0 placeholder sống.
- Golden trace: `docs/flows/unary-invoke-client/` (12 file md-source) — 24 bước bảng
  file:line toàn bộ đã Read, 12 rule validation, 8 failure mode (đắt nhất: SendMsg unary
  trả nil khi write lỗi `stream.go:1147-1155`; context leak #1818 `stream.go:308-323`;
  retry buffer RAM `stream.go:1006-1012`; pick block vô hạn `picker_wrapper.go:111-140`).
- Build + check bằng render của chính skill sinh ra:
  `✓ built docs/flows/unary-invoke-client.html (76302 bytes, 11 sections)` ·
  `✓ check OK (11 sections)` — pass ngay lần đầu.

## Còn lại

- User chấm golden trace → đạt thì đổi stamp SKILL.md + header report `Draft` → `Verified`.
- Không commit trong grpc-go (rule skill) — user tự commit nếu muốn giữ.
