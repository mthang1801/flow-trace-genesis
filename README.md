# flow-trace-genesis

> Gặp một codebase lạ, sinh ra một "chuyên gia trace flow" riêng cho codebase đó.

**flow-trace-genesis** là plugin cho AI coding agent (Claude Code là đường chính; kèm
installer cho Codex, OpenCode, Cursor, Antigravity): lần đầu tiếp cận một project, nó
**khảo sát** codebase, **phỏng vấn chính codebase bằng bằng chứng `file:line`**, rồi
**sinh ra skill `flow-trace` local** — skill trace end-to-end business flow đúng
convention của project đó, xuất **cẩm nang md-source + HTML tương tác self-contained**.

## Vì sao cần nó?

Tool code-intelligence generic (LSP, index, graph) nhìn thấy *cú pháp* nhưng mù với
*convention* của từng codebase: decorator messaging tự chế, pattern constant copy tay
giữa các repo, registry `init()` thay cho DI container, chuỗi gọi frontend riêng...
Trace flow đúng đòi hỏi phải **học convention trước** — genesis tự động hoá đúng bước đó,
một lần cho mỗi project.

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

Mỗi flow là một tài liệu 12 section: tóm tắt · **knowledge graph tương tác**
(Cytoscape.js, filter/search/zoom kiểu graph view, phân tông verified/candidate) ·
sequence diagram · bảng bước có `file:line` cho từng hop · graph quan hệ · validation
rules · business spec ngược (gắn nhãn suy luận rõ ràng) · failure modes theo checklist
archetype · security & ops · ghi chú review · mục "chưa xác định" · lịch sử trace.

Nguyên tắc cứng xuyên suốt:

- **Evidence-first**: chỉ nội dung đã đọc thật với `file:line` mới được thành căn cứ;
  output từ tool index/graph chỉ là ứng viên, được đánh dấu Candidate.
- **Không đoán**: liên kết không lần ra được phải nằm trong mục "Chưa xác định".
- **Chống stale**: header ghi commit hash từng repo tại thời điểm trace.
- **HTML self-contained**: không CDN, không font ngoài — mở offline được, gate kiểm tra
  tự động chặn resource ngoại.

## Kiến trúc

- **CORE/PROFILE**: CORE là thuật toán trace + guardrails — nâng cấp plugin thì regenerate
  ghi đè được; PROFILE là tri thức convention riêng project — regenerate **bảo toàn**.
  Skill sinh ra có version stamp `generated-by`.
- **Tool tiers**: Evidence (Read/LSP/Serena/ast-grep — được làm căn cứ) · Candidate
  (GitNexus/DeepWiki/GitDiagram — chỉ gợi ý) · Ingest (MarkItDown/Docling — convert tài
  liệu PRD). Máy thiếu gì degrade nấy.
- **Render pipeline**: md-source (`_doc.yml` + mỗi section một markdown) → `build.py` →
  HTML self-contained; `check.py` là gate chặn lỗi render cơ học. Knowledge graph lấy từ
  index GitNexus qua script (`kg/extract.py`) — LLM không đọc graph data nên gần như
  không tốn token.

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

## An toàn

- Genesis đọc-only với source code project đích; chỉ ghi file skill sau khi liệt kê +
  bạn confirm; không tự cài tool bên thứ ba; không commit hộ.

## Đóng góp

Issue/PR chào đón tại [github.com/mthang1801/flow-trace-genesis](https://github.com/mthang1801/flow-trace-genesis).
Quy ước: Conventional Commits; thay đổi playbook/template cần kèm một lần chạy thật
(golden flow) làm bằng chứng.

## License

Apache-2.0.
