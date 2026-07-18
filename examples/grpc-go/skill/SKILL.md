---
name: flow-trace
description: Trace end-to-end business flow trong grpc-go (google.golang.org/grpc) từ 1 file/hàm/tên flow được chỉ định. Dùng khi user gọi /flow-trace, hỏi "flow này đi qua đâu", "ai gọi hàm này", "vẽ diagram flow X", hoặc cần cẩm nang business/validation/failure-mode cho một luồng trong thư viện. Output persist tại docs/flows/<slug>/ (md-source đa section + _doc.yml), render HTML bằng render/build.py.
---

<!-- generated-by: flow-trace-genesis v0.1.0 · 2026-07-18 · status: Draft -->
<!-- Draft = chưa qua golden-flow gate. Đổi thành Verified CHỈ sau khi user chấm đạt một trace thật. -->

# Flow Trace — Cẩm nang trace flow (grpc-go)

Input: đường dẫn 1 file (public API / handler / internal component) **hoặc** tên flow.
Output: **một cẩm nang md-source** tại `docs/flows/<slug>/` (`_doc.yml` menu + mỗi
section một file `NN-slug.md`, nội dung theo `references/report-template.md`).

Skill này **read-only với source code**. Chỉ ghi vào `docs/flows/<slug>/`
(+ `docs/flows/<slug>.html` khi build).

<!-- CORE:BEGIN -->
## Nguyên tắc bất biến (đọc trước khi làm gì khác)

1. **Không có node nào thiếu bằng chứng.** Một node/edge chỉ được ghi vào báo cáo khi bạn đã
   `Read` file chứa nó trong phiên này và ghi được `file:line`. Kết quả grep/tool index chưa
   phải bằng chứng — chúng chỉ để tìm ứng viên, Read để xác nhận.
2. **Không resolve được thì nói thẳng.** Mọi liên kết không lần ra được phải vào mục
   **"Chưa xác định"** của báo cáo. Cấm đoán rồi trình bày như fact.
3. **Phân định 2 loại nội dung.** Phần flow/validation là *deterministic* (đọc code ra).
   Phần business/security/ops là *suy luận* — bắt buộc gắn nhãn `[AI suy luận — cần domain
   owner xác nhận]` và vẫn phải kèm citation `file:line` cho căn cứ.
4. **Nhánh chính trước.** Trace hết happy path end-to-end trước, rồi mới mở nhánh lỗi/nhánh
   phụ. Nhánh chưa mở rộng → liệt kê ở mục "Nhánh chưa trace" thay vì trace nửa vời.
5. **Header chống stale.** Báo cáo ghi ngày trace + commit hash (`git rev-parse --short HEAD`)
   + branch đang checkout.
6. **Tool tier.** Evidence (Read/gopls/Serena/grep) mới được thành citation. Candidate
   (GitNexus/DeepWiki/GitDiagram...) chỉ gợi ý ứng viên. Thiếu tool nào thì degrade xuống
   grep + Read và ghi rõ trong báo cáo — không dừng việc.
<!-- CORE:END -->

## Kiến thức nền project (PROFILE — genesis điền, regenerate bảo toàn)

<!-- PROFILE:BEGIN -->
### Cấu trúc repo (Q1)

- Single-repo Go **library** (không phải app dịch vụ): `module google.golang.org/grpc`
  (`go.mod:1`), go 1.25.0. Root package = public API (`call.go`, `stream.go`,
  `clientconn.go`, `server.go`); `internal/` = private impl (nặng nhất là
  `internal/transport/`); sub-package theo domain: `resolver/`, `balancer/`, `encoding/`,
  `credentials/`, `metadata/`, `status/`, `codes/`.
- "Service boundary" của một flow = ranh giới client ↔ server **qua HTTP/2 wire**, không
  phải qua message broker.

### Transport edges (Q2)

- Wire = HTTP/2 trong `internal/transport/`: client tạo stream `http2Client.NewStream`
  (`internal/transport/http2_client.go:756`), ghi frame qua `write` (:1106) → loopyWriter
  goroutine (:476-479) → framer; đọc bằng reader goroutine (:420).
- **Correlation key nối client ↔ server = full method name string** (`callHdr.Method`,
  dạng `/package.Service/Method`) — muốn sang phía server, grep method name trong generated
  code + `server.go` (`processUnaryRPC`).
- Trong process, "edge" chủ yếu là **goroutine + channel** (loopy/controlBuf, blockingCh
  của picker) — khi trace phải ghi rõ cái gì chạy trên goroutine nào.

### Indirection / registry (Q3) — thay cho DI container

- **Global registry + `init()`**: `resolver.Register/Get` (`resolver/resolver.go:54/61`,
  key = scheme), `balancer.Register/Get` (`balancer/balancer.go:58/84`, key = name),
  `encoding.RegisterCodec/GetCodec` (`encoding/encoding.go:132/147`, key = content-subtype;
  proto codec đăng ký tại `encoding/proto/proto.go:35 init()`).
  → Resolve impl: grep `Register(` trong package tương ứng, hoặc gopls references.
- **Functional options**: `DialOption` mutate `dialOptions` (`dialoptions.go:70,589`).
- **Interceptor chain**: `chainUnaryClientInterceptors` (`clientconn.go:224,519-525`) —
  `dopts.unaryInt` luôn đứng đầu chuỗi.

### Event nội bộ (Q4)

- Connectivity state machine: `cc.GetState` (`clientconn.go:336`), `WaitForStateChange`
  (:710). Picker update lan truyền qua `blockingCh` (`picker_wrapper.go:111-140`) — pick
  block cho tới khi có picker mới.

### Frontend (Q5)

- N/A — library. Phase 4 của thuật toán bỏ qua.

### Entrypoints & node lá (Q6)

- Entrypoint: public API được generated code gọi (`ClientConn.Invoke` `call.go:29`,
  `NewStream`), `grpc.NewClient/Dial`, phía server `Server.Serve`.
- Node lá v1 (ghi nhận, không trace sâu): `net.Conn`/framer trong transport, channelz,
  binarylog, stats handlers, os/env config (`GRPC_GO_*`).

### Gotchas Go của repo (Q7) — archetype bổ sung vào checklist CORE

| # | Archetype | Bằng chứng trong repo |
| --- | --- | --- |
| G1 | **Lỗi bị hoãn sang chỗ khác** — SendMsg nuốt transport error thành `io.EOF`, lỗi thật chỉ lộ ở RecvMsg | `stream.go:955-963` |
| G2 | **Nuốt lỗi chủ đích** — `CloseSend` luôn trả nil, bỏ lỗi write | `stream.go:1060-1067` |
| G3 | **Context leak được document** — cancel của child context chỉ chạy khi RecvMsg lỗi/SendMsg lỗi/conn đóng (issue #1818) | `stream.go:308-312` |
| G4 | **Slice capacity sharing race** — `combine()` cố ý không dùng `append` | `call.go:40-53` |
| G5 | **Retry giữ payload trong RAM** — `bufferForRetryLocked` + throttle | `stream.go:1007`, `stream.go:764` |

- Khi trace goroutine: reader (:420) và loopy (:476) chết thế nào, ai nhận biết — luôn hỏi.

### Tool availability (Q8 — máy khảo sát, 2026-07-18)

| Tier | Tool | Trạng thái |
| --- | --- | --- |
| Evidence | gopls (`~/go/bin/gopls` + plugin gopls-lsp), GNU grep 3.12, Read | OK |
| Evidence | Serena (qua `uvx`) | khả dụng, chưa bật mặc định |
| Candidate | GitNexus | CHƯA index repo này — chỉ dùng nếu index |
| Ingest | markitdown MCP | có ở máy này |
| — | ast-grep, ripgrep | KHÔNG có — dùng grep |

### Governance & output (Q9)

- Skill tại `.claude/skills/flow-trace/` (repo không có hệ `.agents`). OUTPUT_DIR:
  `docs/flows/`. Không commit tự động — user tự commit.
<!-- PROFILE:END -->

<!-- CORE:BEGIN -->
## Thuật toán trace — 5 phase

### Phase 0 — Neo (anchor)

Đọc toàn bộ file input. Xác định: đơn vị chính (hàm/struct), entry, payload, các dependency
(registry/option/interface). Nếu input là tên flow → grep trong public API để tìm file neo,
xác nhận với user nếu >1 ứng viên.

### Phase 1 — Upstream (ai kích hoạt?)

Lặp cho đến khi chạm biên (public API / generated code / goroutine nền / test):

1. Tìm caller (grep tên + gopls references).
2. Caller là handler của transport/channel: resolve định danh (method name, channel) →
   sang phía phát → tiếp tục lần ngược.
3. Ghi từng hop: `(package, file:line, loại edge, sync|goroutine)`.

### Phase 2 — Downstream (nó gọi gì?)

1. Với mỗi indirection (registry/option/interface): resolve impl theo PROFILE → Read impl
   → phân loại (transport / registry / goroutine / syscall lá).
2. Qua wire HTTP/2: dùng method name sang phía server nếu flow yêu cầu (quá 3 tầng thì
   dừng hỏi user).
3. Ghi rõ đoạn **song song/goroutine** và **fire-and-forget** — quyết định failure-mode.

### Phase 3 — Phân tích 4 lớp

1. **Validation & Rules** *(deterministic)*: validate metadata/message size/config,
   state check, error code mapping.
2. **Business spec ngược** *(suy luận)*: capability, state transition, config chi phối.
3. **Failure modes**: đối chiếu 6 archetype CORE + G1-G5 của PROFILE với từng edge.
4. **Security & Ops** *(suy luận)*: creds/authz, dữ liệu nhạy cảm trong log, retry/
   timeout/throttle, idempotency.

### Chế độ đối chiếu PRD (khi user đính kèm tài liệu/gRFC)

Convert rich doc trước (markitdown), trích requirement liên quan, điền section "6b" với
verdict `Khớp / Lệch / Doc có-code không thấy / Code có-doc không nói` + citation cả hai
phía. Với grpc-go, "PRD" thường là gRFC (A-series) hoặc Documentation/.

### Phase 4 — Frontend leg

N/A cho repo này (xem PROFILE Q5).

### Phase 5 — Viết báo cáo (md-source)

Persist tại `docs/flows/<slug>/`: `_doc.yml` + mỗi section một file `NN-slug.md`
(mapping + frontmatter: `references/html-render.md`; nội dung: `references/report-template.md`).
Folder tồn tại → cập nhật in-place, ghi thêm `11-history.md`.

### Phase 6 — Render HTML (tùy chọn)

```bash
python3 .claude/skills/flow-trace/render/build.py docs/flows/<slug>
python3 .claude/skills/flow-trace/render/check.py docs/flows/<slug>   # gate bắt buộc pass
```

## Checklist failure archetypes (CORE — phổ quát)

| # | Archetype | Cách nhận diện |
| --- | --- | --- |
| 1 | Nuốt lỗi ở tầng integration | catch/recover trả error như response hợp lệ |
| 2 | Fire-and-forget đứt hậu quả | phát không chờ, consumer fail ai biết? |
| 5 | Retry vô ích / lệch TTL | retry dài hơn hạn của thứ được retry |
| 6 | Ghi batch không atomic | vào một nửa trong luồng không ai chờ |
| 7 | Cache credential không invalidate | 401/403 không xóa cache |
| 8 | Copy-config lệch hai đầu | định danh copy tay 2 nơi |

(+ G1-G5 trong PROFILE cho Go/grpc-go.)

## Giới hạn chi phí

- Mỗi lần trace một flow; quá 3 tầng liên tiếp hoặc >2 nhánh lớn → dừng hỏi user.
- Tool Candidate không bao giờ làm bằng chứng thay Read.
<!-- CORE:END -->

## Nghiệm thu skill

Golden flow: **unary RPC client-side (Invoke path)** — anchor `call.go:29`
(`ClientConn.Invoke`) → `invoke` → `newClientStream` → pick → `http2Client.NewStream/write`.
Trace đầu tiên phải được user chấm đạt thì header mới đổi `Draft` → `Verified`.
