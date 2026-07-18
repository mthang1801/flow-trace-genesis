# Example — grpc-go (unary RPC, client-side Invoke path)

Real output from running **flow-trace-genesis** end-to-end on
[grpc/grpc-go](https://github.com/grpc/grpc-go) `@7d870454` — no hand-editing after the run.

## What's in here

| Path | What it is |
| --- | --- |
| `skill/SKILL.md` | The generated `flow-trace` skill: CORE (shared 5-phase trace algorithm) + PROFILE (grpc-go conventions the survey learned: `init()` registries instead of DI, HTTP/2 wire instead of a broker, gotchas G1–G5 with `file:line` citations) |
| `docs/flows/unary-invoke-client/` | The md-source handbook: `_doc.yml` menu + 12 sections (one file each) + `graph.json` (knowledge-graph data extracted from the GitNexus index by script) |
| `docs/flows/unary-invoke-client.html` | Self-contained interactive build — open it directly in a browser, works offline (no CDN; Cytoscape + MiniSearch + Mermaid vendored inline) |

## How it was produced

The 6-step playbook, on first contact with the repo:

1. **Intake** — no local flow-trace found → generate mode.
2. **Survey** — Go + gRPC detected; tool inventory on the machine (gopls yes, ast-grep no → degrade to grep).
3. **Questionnaire** — Q1–Q10 answered with `file:line` evidence actually read.
4. **Generate** — CORE + PROFILE, version stamp `generated-by: flow-trace-genesis`.
5. **Install** — file list confirmed by the user before writing.
6. **Golden flow** — the trace you see here: 24 steps with `file:line`, 12 validation rules, 8 failure modes. Most expensive finding: unary `SendMsg` returns `nil` even when the transport write fails (`stream.go:1147-1155`) — the error is deferred to `RecvMsg`.

## Rebuild it yourself

```bash
cd examples/grpc-go
python3 ../../plugins/flow-trace-genesis/skills/flow-trace-genesis/render/build.py docs/flows/unary-invoke-client
python3 ../../plugins/flow-trace-genesis/skills/flow-trace-genesis/render/check.py docs/flows/unary-invoke-client
```

Notes: the generated skill also carries its own `render/` + `references/` copies in the
target repo — they are identical to the plugin's, so they are not duplicated here. The
skill stamp is `Draft`: the golden-flow gate (step 6b, human review) intentionally stays
open until a maintainer signs it off — that is the gate working as designed, not an
omission.
