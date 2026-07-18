# CORE Template — skill `flow-trace` local sinh cho project đích

> Đây là **khuôn CORE**. Genesis copy nguyên văn phần trong khối ```markdown bên dưới,
> điền các placeholder `{{...}}` và chèn PROFILE (từ questionnaire) vào đúng vị trí đánh dấu.
> **Luật regenerate**: vùng giữa `<!-- CORE:BEGIN -->` … `<!-- CORE:END -->` được ghi đè
> bởi phiên bản CORE mới; vùng giữa `<!-- PROFILE:BEGIN -->` … `<!-- PROFILE:END -->`
> phải được BẢO TOÀN nguyên trạng.

Placeholder genesis phải điền:

| Placeholder | Nguồn |
| --- | --- |
| `{{PROJECT_NAME}}` | tên project/workspace đích |
| `{{GENESIS_VERSION}}` | version trong `plugin.json` lúc sinh |
| `{{DATE}}` | ngày sinh skill (YYYY-MM-DD) |
| `{{OUTPUT_DIR}}` | nơi persist cẩm nang — mặc định `docs/flows/`, đổi theo governance repo đích |
| `{{PROFILE_*}}` | các block điền từ `profile-questionnaire.md` |
| `{{GOLDEN_FLOW}}` | flow nghiệm thu user chọn (bước 6 của genesis) |

```markdown
---
name: flow-trace
description: Trace end-to-end business flow trong {{PROJECT_NAME}} từ 1 file/hàm/tên flow được chỉ định. Dùng khi user gọi /flow-trace, hỏi "flow này đi qua đâu", "ai gọi hàm này", "vẽ diagram flow X", "quy trình này thực sự chạy thế nào", hoặc cần cẩm nang business/validation/failure-mode cho một luồng nghiệp vụ — cẩm nang viết cho cả dev lẫn BA/PO/PM/QA (tóm tắt nghiệp vụ ngôn ngữ thường + bằng chứng file:line). Output persist tại {{OUTPUT_DIR}}<slug>/ (md-source đa section + _doc.yml), render HTML bằng render/build.py.
---

<!-- generated-by: flow-trace-genesis v{{GENESIS_VERSION}} · {{DATE}} · status: Draft -->
<!-- Draft = chưa qua golden-flow gate. Đổi thành Verified CHỈ sau khi user chấm đạt một trace thật. -->

# Flow Trace — Cẩm nang trace flow ({{PROJECT_NAME}})

Input: đường dẫn 1 file (entrypoint / handler / use case / component) **hoặc** tên flow.
Output: **một cẩm nang md-source** tại `{{OUTPUT_DIR}}<slug>/` (`_doc.yml` menu + mỗi
section một file `NN-slug.md`, nội dung theo `references/report-template.md`).

Skill này **read-only với source code**. Chỉ ghi vào `{{OUTPUT_DIR}}<slug>/`
(+ `{{OUTPUT_DIR}}<slug>.html` khi build).

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
   của **từng repo/module** đã đi qua + branch đang checkout.
6. **Tool tier.** Evidence (Read/LSP/Serena/ast-grep) mới được thành citation. Candidate
   (GitNexus/DeepWiki/Understand-Anything/GitDiagram...) chỉ gợi ý ứng viên. Thiếu tool nào
   thì degrade xuống grep + Read và ghi rõ trong báo cáo — không dừng việc.
<!-- CORE:END -->

## Kiến thức nền project (PROFILE — genesis điền, regenerate bảo toàn)

<!-- PROFILE:BEGIN -->
{{PROFILE_SERVICE_MARKERS}}
{{PROFILE_TRANSPORT_EDGES}}
{{PROFILE_DI_INDIRECTION}}
{{PROFILE_INTERNAL_EVENTS}}
{{PROFILE_FRONTEND_CHAIN}}
{{PROFILE_LEAF_NODES}}
{{PROFILE_GOTCHAS}}
<!-- PROFILE:END -->

<!-- CORE:BEGIN -->
## Thuật toán trace — 5 phase

### Phase 0 — Neo (anchor)

Đọc toàn bộ file input. Xác định: đơn vị chính (class/hàm), method entry, payload/DTO,
các dependency được inject/import. Nếu input là tên flow → tìm file neo bằng grep/tool
trong phạm vi entrypoint của PROFILE, xác nhận với user nếu >1 ứng viên.

### Phase 1 — Upstream (ai kích hoạt?)

Lặp cho đến khi chạm biên (HTTP route / scheduler / message từ hệ ngoài / CLI):

1. Tìm nơi gọi đơn vị hiện tại (grep tên + LSP references nếu có).
2. Nếu caller là consumer/subscriber của transport: resolve định danh kênh (constant/topic/
   pattern) theo PROFILE_TRANSPORT_EDGES → sang phía producer tìm nơi phát → tiếp tục lần
   ngược ở đó. **Read cả hai đầu** để xác nhận định danh khớp — lệch là finding quan trọng.
3. Nếu caller là route/controller: ghi route đầy đủ, sang Phase 4 cho nhánh FE (nếu có).
4. Ghi từng hop: `(service/module, file:line, loại edge, sync|async)`.

### Phase 2 — Downstream (nó gọi gì?)

Từ entry đi xuống theo thứ tự thực thi:

1. Với mỗi dependency được gọi: resolve implementation theo PROFILE_DI_INDIRECTION →
   Read impl → phân loại tiếp (DB / cache / HTTP third-party / message producer / queue).
2. Với mỗi lần phát message xuyên service: resolve định danh kênh → sang repo/module đích
   tìm consumer → đệ quy Phase 2 (quá 3 service liên tiếp thì dừng hỏi user).
3. Với event nội bộ: theo PROFILE_INTERNAL_EVENTS.
4. Ghi rõ đoạn **song song** và **fire-and-forget** — hai thứ này quyết định failure-mode.

### Phase 3 — Phân tích 4 lớp (trên xương sống đã có)

1. **Validation & Rules** *(deterministic)*: validation khai báo (decorator/schema/tag),
   guard/middleware trên route, rule frontend, check nghiệp vụ trong code (throw/return
   error), state-machine transition nếu có.
2. **Business spec ngược** *(suy luận)*: từ route + payload + tên hàm + điều kiện rẽ nhánh,
   viết capability nghiệp vụ — flow phục vụ việc gì, trạng thái nào chuyển sang trạng thái
   nào, ngưỡng/config nào chi phối.
3. **Failure modes** *(nửa deterministic)*: đối chiếu **checklist archetype** bên dưới
   (CORE + phần bổ sung ngôn ngữ trong PROFILE_GOTCHAS) với từng edge.
4. **Security & Ops** *(suy luận)*: authz trên route, dữ liệu nhạy cảm trong log,
   retry/timeout/DLQ, idempotency.

### Chế độ đối chiếu PRD (khi user đính kèm PRD/tài liệu nghiệp vụ)

1. Tài liệu rich (PDF/DOCX/XLSX...) → convert sang Markdown trước (MarkItDown/Docling MCP
   nếu có; không có thì báo blocker, không giả vờ đã đọc).
2. Trích requirement liên quan flow đang trace (ghi rõ đã bỏ qua gì).
3. Lớp business của Phase 3 đổi chế độ: đối chiếu từng requirement với hành vi code, điền
   section "6b. Đối chiếu PRD ↔ Code" với verdict: `Khớp` / `Lệch` / `PRD có, code không
   thấy` / `Code có, PRD không nói`. Mỗi verdict kèm citation PRD (mục/trang) + `file:line`.
   **Mismatch là finding quan trọng nhất của chế độ này.**
4. Không bao giờ "sửa" mô tả PRD cho khớp code hoặc ngược lại.

### Phase 4 — Frontend leg (nếu flow có HTTP route và project có FE)

Theo PROFILE_FRONTEND_CHAIN: route path → constant/API client → hàm service → page/component.
Ghi `file:line` cho từng chặng. Không phân tích logic render — chỉ cần điểm nối.

### Phase 5 — Viết báo cáo (md-source)

Persist tại `{{OUTPUT_DIR}}<slug>/`: `_doc.yml` + mỗi section một file `NN-slug.md`
(mapping + frontmatter: xem `references/html-render.md`; nội dung theo
`references/report-template.md`). Slug đặt theo tên nghiệp vụ. Folder đã tồn tại →
cập nhật section liên quan in-place, ghi thêm dòng vào `11-history.md`.

### Phase 6 — Render HTML (tùy chọn, khi user yêu cầu)

```bash
python3 <skill-dir>/render/build.py {{OUTPUT_DIR}}<slug>   # → <slug>.html self-contained
python3 <skill-dir>/render/check.py {{OUTPUT_DIR}}<slug>   # gate bắt buộc pass
```

MD là source of truth; HTML regenerate toàn bộ, không patch tay.

## Checklist failure archetypes (CORE — phổ quát mọi ngôn ngữ)

| # | Archetype | Cách nhận diện |
| --- | --- | --- |
| 1 | **Nuốt lỗi ở tầng integration** | catch/recover trả error như response hợp lệ, flag kiểu `throwError=false`. Hỏi: caller có phân biệt được success/failure không? |
| 2 | **Fire-and-forget đứt hậu quả** | phát message không chờ rồi bước sau chạy ngay — consumer fail thì ai biết? Có alert/đối soát không? |
| 5 | **Retry vô ích / lệch TTL** | retry policy (attempts × backoff) dài hơn hạn dùng của thứ được retry (presigned URL, token, lock). |
| 6 | **Enqueue/ghi batch không atomic** | ghi một phần rồi fail trong luồng không ai chờ — vào một nửa, không ai biết nửa nào. |
| 7 | **Cache credential không invalidate** | token/config cache theo TTL nhưng không xóa khi bị từ chối (401/403) → lỗi "lúc được lúc không" đến khi TTL hết. |
| 8 | **Copy-config lệch hai đầu** | định danh kênh/queue/topic copy tay giữa 2 module — so từng ký tự cả hai đầu. |

(Archetype đặc thù ngôn ngữ/framework — ví dụ truthy guard, serialize rớt field — nằm trong
PROFILE_GOTCHAS.)

Với mỗi archetype match: ghi vào Failure modes kèm `file:line` + kịch bản cụ thể
"input/trạng thái nào → hậu quả gì". Không match thì không bịa.

## Giới hạn chi phí

- Mỗi lần trace chỉ theo **một flow** — không quét cả module.
- Quá 3 service/module liên tiếp một nhánh, hoặc >2 nhánh rẽ lớn: dừng, hỏi user chọn nhánh
  ưu tiên, phần còn lại vào "Nhánh chưa trace".
- Tool Candidate chỉ gợi ý ứng viên khi grep bí; không bao giờ làm bằng chứng thay Read.
<!-- CORE:END -->

## Nghiệm thu skill

Golden flow: `{{GOLDEN_FLOW}}` — trace đầu tiên phải được user (người thuộc flow) chấm đạt
thì header mới đổi `Draft` → `Verified`.
```
