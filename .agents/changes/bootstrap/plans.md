# Plan — Bootstrap plugin flow-trace-genesis v1

Status: Open (executor gate ĐÓNG — chờ user approve)
Nguồn quyết định: 2 phiên grill-me 2026-07-16 (flow-trace Lending) + 2026-07-17 (genesis).

## Quyết định đã chốt (không bàn lại)

| # | Hạng mục | Giá trị |
| --- | --- | --- |
| 1 | Vị trí / remote | Repo này — `github.com/mthang1801/flow-trace-genesis`, private-first, Apache-2.0 |
| 2 | Bãi thử | go-core-adapter-service (Go+buf/gRPC) → Dni workspace → dogfood Lending |
| 3 | Phạm vi v1 | Plugin + marketplace + command + .mcp.json full stack + installer Codex/OpenCode/Cursor |
| 4 | MCP bundle | Serena + Docling + markitdown; playbook degrade gracefully khi máy thiếu |
| 5 | Ngôn ngữ | Tiếng Việt; dịch English gộp đợt sanitize/public |
| 6 | Output convention | Genesis dò governance repo đích (.agents→kiểu Lending / .claude→đặt đó / không có→hỏi); báo cáo mặc định `docs/flows/` |
| 7 | Kiến trúc skill sinh ra | Self-contained CORE+PROFILE, `generated-by` version stamp, regenerate ghi đè CORE bảo toàn PROFILE, header Draft→Verified |
| 8 | Tên trigger | Global `flow-trace-genesis` (chỉ trigger khi project CHƯA có flow-trace local); local giữ tên `flow-trace` |
| 9 | An toàn | Không ghi đè flow-trace local có sẵn nếu không diff+confirm; Candidate tier không bao giờ thành citation |

## Cấu trúc repo đích (v1)

```
flow-trace-genesis/
├── .claude-plugin/marketplace.json          # khai báo marketplace, list plugin
├── plugins/flow-trace-genesis/
│   ├── .claude-plugin/plugin.json           # manifest plugin (name, version, description)
│   ├── skills/flow-trace-genesis/
│   │   ├── SKILL.md                         # playbook genesis 6 bước (xem dưới)
│   │   └── references/
│   │       ├── core-template.md             # CORE flow-trace: 5 phase + guardrails
│   │       │                                #   + archetype phổ quát (#1,2,5,6,7,8 generic hóa)
│   │       ├── report-template.md           # 11 section + 6b PRD-reconciliation (port từ Lending)
│   │       ├── html-render.md               # pipeline md-source → HTML (port từ Lending)
│   │       ├── profile-questionnaire.md     # bộ câu hỏi convention: service markers,
│   │       │                                #   transport edges, DI/indirection, FE, entrypoints,
│   │       │                                #   archetype ngôn ngữ, tool per-language (LSP/Doxygen/Joern)
│   │       └── profiles/
│   │           ├── _TEMPLATE.md             # khung profile chuẩn genesis phải điền
│   │           └── lending.md               # mẫu vàng — port tri thức NestJS/RabbitMQ/Umi
│   │                                        #   (INTERNAL — sanitize-before-public)
│   ├── skills/flow-trace-genesis/render/    # base render tái sử dụng — PORT NGUYÊN TRẠNG từ
│   │   ├── build.py                         #   Lending `.agents/skills/flow-trace/render/`
│   │   ├── check.py                         #   (đã build+check pass với golden resubmit-a2
│   │   ├── templates/base.html              #   2026-07-17; gốc phỏng theo ~/mAIvt)
│   │   └── assets/{tokens.css,engine.js}
│   ├── commands/flow-trace-genesis.md       # /flow-trace-genesis TARGET_DIR= [PRD=] [ADVISOR=]
│   └── .mcp.json                            # serena (uvx) + markitdown + docling
├── installers/
│   ├── install.sh                           # --target codex|opencode|cursor (copy skills đúng layout)
│   └── README.md                            # mapping đường dẫn từng harness
└── README.md                                # cách cài, cách dùng, kiến trúc, security notes
```

## Playbook genesis (SKILL.md) — 6 bước, mỗi bước có gate

1. **Intake**: nhận TARGET_DIR; phát hiện đã có flow-trace local chưa → có thì
   chuyển chế độ regenerate (diff + confirm, bảo toàn PROFILE) hoặc dừng.
2. **Khảo sát** (đắt, 1 lần): detect service/ngôn ngữ/build markers; chạy Candidate
   advisors nếu có (GitNexus/DeepWiki-Open/GitDiagram — audit trước khi cài mới);
   Evidence bằng Read/LSP/Serena/ast-grep. Degrade gracefully + ghi rõ tool nào thiếu.
3. **Điền questionnaire**: trả lời từng mục bằng bằng chứng `file:line`;
   mục không xác minh được → "Chưa xác minh", cấm đoán.
4. **Sinh skill local**: CORE (copy từ core-template, đóng dấu
   `generated-by: flow-trace-genesis vX.Y`) + PROFILE (từ questionnaire) →
   self-contained SKILL.md + references; header `Trạng thái: Draft`.
5. **Cài vào project đích** theo governance dò được (quyết định #6); không ghi đè
   khi chưa confirm.
6. **Golden-flow gate**: yêu cầu user chọn 1 flow họ thuộc → chạy trace đầu bằng
   skill vừa sinh → user chấm → đạt mới đổi header `Verified`. Genesis KHÔNG
   tự kết thúc ở "đã sinh xong file".

## Thứ tự thực thi (trong change này)

1. `.claude-plugin/marketplace.json` + `plugin.json` — khung phân phối.
2. `references/` — port core-template, report-template, html-render từ bản Lending
   (generic hóa: bỏ tên service/chi tiết nội bộ khỏi CORE; chi tiết nội bộ dồn về
   `profiles/lending.md`). html-render theo pipeline md-source mới (2026-07-17):
   output cẩm nang = folder `_doc.yml` + section md, build/gate bằng `render/`.
2b. `render/` — copy nguyên trạng 5 file từ Lending `.agents/skills/flow-trace/render/`
   (build.py, check.py, templates/base.html, assets/tokens.css, assets/engine.js);
   KHÔNG fork chỉnh riêng — mọi sửa base phải sync ngược về Lending (chống trôi CORE).
3. `profile-questionnaire.md` + `profiles/_TEMPLATE.md`.
4. `SKILL.md` genesis (6 bước trên) + `commands/flow-trace-genesis.md`.
5. `.mcp.json` (serena/markitdown/docling) — kèm ghi chú dependency (uv, pip).
6. `installers/install.sh` (3 target) + README.
7. Root `README.md`.
8. Verification (dưới) → cập nhật progress/CHANGELOG → grill gate → commit khi user yêu cầu.

## Verification

- `bash .agents/scripts/governance-harness.sh` pass sau mọi bước chạm governance.
- Plugin validate: cài thử marketplace local vào Claude Code trên chính máy này
  (`/plugin marketplace add` đường dẫn local) → skill `flow-trace-genesis` xuất hiện
  trong danh sách available skills.
- Installer dry-run: `install.sh --target codex --dry-run` in ra đúng mapping không ghi file.
- CHƯA tính là hoàn thành sản phẩm cho đến khi golden Go pass (change record kế tiếp).

## Risks

| Risk | Mitigation |
| --- | --- |
| CORE generic hóa bị "mất chất" so với bản Lending | profiles/lending.md giữ nguyên 100% chi tiết; CORE chỉ giữ phần đã chứng minh phổ quát |
| Plugin manifest/marketplace format lệch phiên bản Claude Code | Validate bằng cài thử local ngay trong change này |
| Installer 3 harness — layout mỗi bên khác nhau và có thể đổi | v1 chỉ copy-file đơn giản + README mapping; không cố abstract hóa sớm |
| Serena/Docling kéo dependency nặng máy mới | .mcp.json kèm comment yêu cầu; playbook degrade gracefully là rule cứng |
| Genesis ghi nhầm vào repo đích | Bước 5 luôn liệt kê file sẽ tạo + hỏi confirm trước khi ghi |
