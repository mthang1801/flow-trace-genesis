# flow-trace-genesis

[![License](https://img.shields.io/github/license/mthang1801/flow-trace-genesis?color=blue)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-brightgreen)](plugins/flow-trace-genesis/.claude-plugin/plugin.json)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-plugin-d97757)](https://docs.anthropic.com/en/docs/claude-code/plugins)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/mthang1801/flow-trace-genesis/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/mthang1801/flow-trace-genesis)](https://github.com/mthang1801/flow-trace-genesis/commits/main)
[![Stars](https://img.shields.io/github/stars/mthang1801/flow-trace-genesis?style=social)](https://github.com/mthang1801/flow-trace-genesis/stargazers)

[🇬🇧 English](README.md) | 🇻🇳 Tiếng Việt

> Biến bất kỳ codebase nào thành cẩm nang flow mà cả team đọc được — từ kỹ sư đến người làm sản phẩm.

Codebase của bạn vốn đã chứa bản mô tả đúng nhất về cách business vận hành — từng rule, từng bước duyệt, từng edge case. **flow-trace-genesis** biến tri thức ẩn đó thành **cẩm nang flow ai cũng đọc được**: điều gì thực sự xảy ra khi khách hàng nộp hồ sơ, hệ thống đang ép những rule nào, cái gì có thể hỏng và hỏng thì mất gì — mọi khẳng định đều có bằng chứng từ chính code, nên cẩm nang không bao giờ trôi khỏi thực tế như tài liệu viết tay.

Một cẩm nang phục vụ cả team: tóm tắt quy trình bằng ngôn ngữ thường + business spec dựng ngược từ code cho BA/PO/PM, validation rules và checklist lỗi cho QA, bảng bước `file:line` cùng diagram tương tác cho kỹ sư. Bên dưới, nó là plugin cho AI coding agent (Claude Code là đường chính; kèm installer cho Codex, OpenCode, Cursor, Antigravity): lần đầu tiếp cận một project, nó **khảo sát** codebase, **phỏng vấn codebase bằng bằng chứng `file:line`**, rồi **sinh ra skill `flow-trace` local** — một "chuyên viên phân tích" riêng cho project đó, thuộc convention của project, chuyên "cook" flow kỹ thuật thành bản phân tích quy trình tổng thể từ tech đến business.

## Vì sao cần nó?

**Bài toán business**: tài liệu luôn trôi, nhưng code không nói dối. Ở hầu hết các team, code là bản mô tả duy nhất còn đúng về cách một quy trình thực sự chạy — nhưng chỉ dev đọc được. Khi BA hỏi "khách resubmit hồ sơ thì hệ thống thực sự làm gì?", câu trả lời trung thực thường nằm trong code mà không ai có thời gian dẫn họ đi xem.

**Bài toán kỹ thuật**: tool code-intelligence generic (LSP, index, graph) nhìn thấy *cú pháp* nhưng mù với *convention* của từng codebase — decorator messaging tự chế, constant copy tay giữa các repo, registry `init()` thay cho DI container, chuỗi gọi frontend riêng. Trace flow đúng đòi hỏi phải **học convention trước**.

Genesis tự động hoá cả hai: học convention một lần cho mỗi project, rồi biến code — nguồn sự thật thật sự — thành cẩm nang ai cũng đọc được.

## Dành cho ai?

| Vai trò | Bạn nhận được gì từ cẩm nang flow |
| --- | --- |
| **Kỹ sư** | Bảng bước có `file:line` cho từng hop, knowledge graph tương tác, sequence diagram — onboard và đánh giá impact không cần mò code. |
| **BA / PO / PM** | Tóm tắt flow bằng ngôn ngữ thường, business spec dựng ngược từ code, validation rule diễn đạt thành business rule — câu trả lời "hệ thống thực sự làm gì" lấy từ code, không phải từ trí nhớ. |
| **QA** | Validation rules và checklist failure mode để thiết kế test case — gồm cả edge case chỉ code mới biết. |
| **Ops / Security** | Ghi chú security & ops theo từng flow: điểm chạm bên ngoài, queue, retry, hành vi khi lỗi. |

Suy luận luôn được gắn nhãn: nội dung AI *suy ra* (thay vì *đọc thấy*) đều được đánh dấu rõ, để người không đọc code biết câu nào là bằng chứng, câu nào là diễn giải.

## Cài đặt

**Claude Code (marketplace):**

```text
/plugin marketplace add mthang1801/flow-trace-genesis
/plugin install flow-trace-genesis@flow-trace-genesis-marketplace
```

**Codex / OpenCode / Cursor / Antigravity:**

```bash
git clone https://github.com/mthang1801/flow-trace-genesis.git
cd flow-trace-genesis
./installers/install.sh --target cursor --dry-run   # xem trước, không ghi file
./installers/install.sh --target cursor             # codex|opencode|cursor|antigravity|claude
```

Mapping layout từng harness: [`installers/README.md`](installers/README.md).

## Dùng

```text
/flow-trace-genesis TARGET_DIR=/path/to/project [PRD=/path/to/doc.pdf] [ADVISOR=none]
```

Playbook 6 bước, mỗi bước có gate — genesis không bao giờ "im lặng ghi file":

1. **Intake** — phát hiện flow-trace local có sẵn; có thì chuyển chế độ regenerate (show diff, chờ confirm).
2. **Khảo sát** — detect ngôn ngữ/service marker; kiểm kê tool thật trên máy; thiếu tool thì degrade xuống grep + Read, không chặn việc.
3. **Questionnaire** — trả lời bộ câu hỏi convention (transport, DI/indirection, entrypoint, gotchas...), mỗi câu kèm bằng chứng `file:line` đã đọc thật.
4. **Sinh skill** — CORE (thuật toán trace 5 phase, dùng chung) + PROFILE (convention riêng project) + bộ render.
5. **Cài vào project** — liệt kê đầy đủ file sẽ tạo, chờ confirm mới ghi.
6. **Golden-flow gate** — trace thử một flow bạn thuộc; bạn chấm đạt thì skill mới được đóng dấu `Verified`.

Skill sinh ra dùng độc lập, không phụ thuộc genesis:

```text
/flow-trace <đường dẫn file hoặc tên flow>
→ cẩm nang tại docs/flows/<slug>/ + bản HTML tương tác
```

## Cẩm nang sinh ra có gì?

Mỗi flow là một tài liệu 12 section: tóm tắt · **knowledge graph tương tác** (Cytoscape.js, filter/search/zoom kiểu graph view, phân tông verified/candidate) · sequence diagram · bảng bước có `file:line` cho từng hop · graph quan hệ · validation rules · business spec ngược (gắn nhãn suy luận rõ ràng) · failure modes theo checklist archetype · security & ops · ghi chú review · mục "chưa xác định" · lịch sử trace.

Nguyên tắc cứng xuyên suốt:

- **Evidence-first**: chỉ nội dung đã đọc thật với `file:line` mới được thành căn cứ; output từ tool index/graph chỉ là ứng viên, được đánh dấu Candidate.
- **Không đoán**: liên kết không lần ra được phải nằm trong mục "Chưa xác định".
- **Chống stale**: header ghi commit hash từng repo tại thời điểm trace.
- **HTML self-contained**: không CDN, không font ngoài — mở offline được, gate kiểm tra tự động chặn resource ngoại.

## Kiến trúc

- **CORE/PROFILE**: CORE là thuật toán trace + guardrails — nâng cấp plugin thì regenerate ghi đè được; PROFILE là tri thức convention riêng project — regenerate **bảo toàn**. Skill sinh ra có version stamp `generated-by`.
- **Tool tiers**: Evidence (Read/LSP/Serena/ast-grep — được làm căn cứ) · Candidate (GitNexus/DeepWiki/GitDiagram — chỉ gợi ý) · Ingest (MarkItDown/Docling — convert tài liệu PRD). Máy thiếu gì degrade nấy.
- **Render pipeline**: md-source (`_doc.yml` + mỗi section một markdown) → `build.py` → HTML self-contained; `check.py` là gate chặn lỗi render cơ học. Knowledge graph lấy từ index GitNexus qua script (`kg/extract.py`) — LLM không đọc graph data nên gần như không tốn token.

## Cấu trúc repo

```text
.claude-plugin/marketplace.json      # marketplace cho Claude Code
plugins/flow-trace-genesis/
├── .claude-plugin/plugin.json
├── skills/flow-trace-genesis/       # SKILL.md + references/ (template, questionnaire) + render/
└── .mcp.json                        # serena + markitdown + docling (optional, degrade được)
installers/                          # install.sh đa harness + prompts/
```

## Yêu cầu

- AI coding agent hỗ trợ skills (Claude Code, Codex, OpenCode, Cursor, Antigravity...).
- `python3` + PyYAML (render HTML). Node/npx nếu dùng knowledge graph (GitNexus).
- MCP bundle trong `.mcp.json` là tùy chọn — thiếu vẫn chạy được toàn bộ luồng chính.

**Khai thác tối đa** — kiểm tra máy đang có gì, thiếu gì:

```bash
./installers/doctor.sh            # scan read-only: tool × tier × mất gì × lệnh fix chính xác
./installers/doctor.sh --install  # cài interactive các tool user-space (pip --user / npm -g)
```

Doctor không bao giờ tự chạy `sudo`: package hệ thống chỉ được in lệnh để bạn tự chạy; cài user-space chỉ chạy sau khi bạn y/N từng tool. Thiếu gì thì degrade nấy — không gì chặn luồng chính ngoài `python3` + PyYAML.

## An toàn

- Genesis đọc-only với source code project đích; chỉ ghi file skill sau khi liệt kê + bạn confirm; không tự cài tool bên thứ ba; không commit hộ.

## Đóng góp

Issue/PR chào đón tại [github.com/mthang1801/flow-trace-genesis](https://github.com/mthang1801/flow-trace-genesis). Quy ước: Conventional Commits; thay đổi playbook/template cần kèm một lần chạy thật (golden flow) làm bằng chứng.

## License

Apache-2.0.
