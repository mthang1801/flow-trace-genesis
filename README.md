# flow-trace-genesis

**English** | [Tiếng Việt](#tiếng-việt)

> Meet an unfamiliar codebase, generate a dedicated "flow-tracing expert" for that codebase.

**flow-trace-genesis** is a plugin for AI coding agents (Claude Code is the primary path; installers included for Codex, OpenCode, Cursor, Antigravity). On first contact with a project it **surveys** the codebase, **interviews the codebase itself with `file:line` evidence**, then **generates a local `flow-trace` skill** — a skill that traces end-to-end business flows following that project's own conventions, producing an **md-source handbook plus a self-contained interactive HTML report**.

## Why does this exist?

Generic code-intelligence tools (LSP, indexes, graphs) see *syntax* but are blind to each codebase's *conventions*: home-grown messaging decorators, constants hand-copied between repos, `init()` registries instead of a DI container, custom frontend call chains... Tracing a flow correctly requires **learning the conventions first** — genesis automates exactly that step, once per project.

## Installation

**Claude Code (marketplace):**

```text
/plugin marketplace add mthang1801/flow-trace-genesis
/plugin install flow-trace-genesis@flow-trace-genesis-marketplace
```

**Codex / OpenCode / Cursor / Antigravity:**

```bash
git clone https://github.com/mthang1801/flow-trace-genesis.git
cd flow-trace-genesis
./installers/install.sh --target cursor --dry-run   # preview, writes nothing
./installers/install.sh --target cursor             # codex|opencode|cursor|antigravity|claude
```

Per-harness layout mapping: [`installers/README.md`](installers/README.md).

## Usage

```text
/flow-trace-genesis TARGET_DIR=/path/to/project [PRD=/path/to/doc.pdf] [ADVISOR=none]
```

A 6-step playbook, each step gated — genesis never "silently writes files":

1. **Intake** — detect an existing local flow-trace; if found, switch to regenerate mode (show diff, wait for confirmation).
2. **Survey** — detect languages/service markers; inventory the tools actually present on the machine; missing tools degrade to grep + Read instead of blocking.
3. **Questionnaire** — answer a convention question set (transport, DI/indirection, entrypoints, gotchas...), each answer backed by `file:line` evidence that was actually read.
4. **Generate the skill** — CORE (the shared 5-phase trace algorithm) + PROFILE (project-specific conventions) + the render toolkit.
5. **Install into the project** — list every file to be created, write only after confirmation.
6. **Golden-flow gate** — trace a flow you know well; only when you approve it does the skill get stamped `Verified`.

The generated skill runs standalone, with no dependency on genesis:

```text
/flow-trace <file path or flow name>
→ handbook at docs/flows/<slug>/ + interactive HTML build
```

## What's in a generated handbook?

Each flow is a 12-section document: summary · **interactive knowledge graph** (Cytoscape.js, graph-view-style filter/search/zoom, verified/candidate tones) · sequence diagram · step table with `file:line` for every hop · relationship graph · validation rules · reverse-engineered business spec (inference clearly labeled) · failure modes per archetype checklist · security & ops · review notes · an "unresolved" section · trace history.

Hard principles throughout:

- **Evidence-first**: only content actually read with `file:line` can serve as ground truth; output from index/graph tools is candidate-only and marked as such.
- **No guessing**: links that can't be traced go into the "Unresolved" section.
- **Staleness guard**: the header records each repo's commit hash at trace time.
- **Self-contained HTML**: no CDNs, no external fonts — opens offline; an automated gate blocks external resources.

## Architecture

- **CORE/PROFILE**: CORE is the trace algorithm + guardrails — plugin upgrades may overwrite it on regenerate; PROFILE is the project's convention knowledge — regenerate **preserves** it. Generated skills carry a `generated-by` version stamp.
- **Tool tiers**: Evidence (Read/LSP/Serena/ast-grep — admissible as ground truth) · Candidate (GitNexus/DeepWiki/GitDiagram — hints only) · Ingest (MarkItDown/Docling — PRD document conversion). Whatever the machine lacks, genesis degrades gracefully.
- **Render pipeline**: md-source (`_doc.yml` + one markdown per section) → `build.py` → self-contained HTML; `check.py` gates against mechanical render errors. The knowledge graph is extracted from the GitNexus index by script (`kg/extract.py`) — the LLM never reads the graph data, so token cost is near zero.

## Repo layout

```text
.claude-plugin/marketplace.json      # Claude Code marketplace
plugins/flow-trace-genesis/
├── .claude-plugin/plugin.json
├── skills/flow-trace-genesis/       # SKILL.md + references/ (templates, questionnaire) + render/
└── .mcp.json                        # serena + markitdown + docling (optional, degradable)
installers/                          # multi-harness install.sh + prompts/
```

## Requirements

- An AI coding agent with skill support (Claude Code, Codex, OpenCode, Cursor, Antigravity...).
- `python3` + PyYAML (HTML render). Node/npx if using the knowledge graph (GitNexus).
- The MCP bundle in `.mcp.json` is optional — the entire main flow works without it.

## Safety

- Genesis is read-only toward the target project's source code; it writes skill files only after listing them and getting your confirmation; it never installs third-party tools on its own; it never commits on your behalf.

## Contributing

Issues/PRs welcome at [github.com/mthang1801/flow-trace-genesis](https://github.com/mthang1801/flow-trace-genesis). Conventions: Conventional Commits; playbook/template changes must come with one real run (a golden flow) as evidence.

## License

Apache-2.0.

---

# Tiếng Việt

[English](#flow-trace-genesis) | **Tiếng Việt**

> Gặp một codebase lạ, sinh ra một "chuyên gia trace flow" riêng cho codebase đó.

**flow-trace-genesis** là plugin cho AI coding agent (Claude Code là đường chính; kèm installer cho Codex, OpenCode, Cursor, Antigravity): lần đầu tiếp cận một project, nó **khảo sát** codebase, **phỏng vấn chính codebase bằng bằng chứng `file:line`**, rồi **sinh ra skill `flow-trace` local** — skill trace end-to-end business flow đúng convention của project đó, xuất **cẩm nang md-source + HTML tương tác self-contained**.

## Vì sao cần nó?

Tool code-intelligence generic (LSP, index, graph) nhìn thấy *cú pháp* nhưng mù với *convention* của từng codebase: decorator messaging tự chế, pattern constant copy tay giữa các repo, registry `init()` thay cho DI container, chuỗi gọi frontend riêng... Trace flow đúng đòi hỏi phải **học convention trước** — genesis tự động hoá đúng bước đó, một lần cho mỗi project.

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

## An toàn

- Genesis đọc-only với source code project đích; chỉ ghi file skill sau khi liệt kê + bạn confirm; không tự cài tool bên thứ ba; không commit hộ.

## Đóng góp

Issue/PR chào đón tại [github.com/mthang1801/flow-trace-genesis](https://github.com/mthang1801/flow-trace-genesis). Quy ước: Conventional Commits; thay đổi playbook/template cần kèm một lần chạy thật (golden flow) làm bằng chứng.

## License

Apache-2.0.
