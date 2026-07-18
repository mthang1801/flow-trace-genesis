# Contributing

Thanks for considering a contribution to flow-trace-genesis. This document is the
mechanical checklist; for the "why" behind the design, read the [README](README.md)
first.

## Before you open a PR

- **Evidence-first still applies to the plugin itself.** If your change touches the
  genesis playbook, `references/core-template.md`, or the `render/` pipeline, run it for
  real on a project and attach the result — a new/updated sample under `examples/`, or a
  before/after of an existing one. A description of what the change *should* do is not
  evidence; a golden flow that actually built and passed `check.py` is.
- **`render/` has one canonical copy** (`plugins/flow-trace-genesis/skills/flow-trace-genesis/render/`).
  If you're fixing a render bug found while using a *generated* skill elsewhere, port the
  fix back here — don't patch it only in the generated copy. CI's `render-sync` job will
  catch a second copy appearing in-repo and diff it against the canonical one; use
  `scripts/check-render-sync.sh <dir1> <dir2> ...` to check any two copies yourself.
- **Keep the dependency floor at `python3` + PyYAML.** Anything else (ripgrep, ast-grep,
  a language server, node/npx, uv) is optional and must degrade gracefully when absent —
  see `installers/doctor.sh` for the tier a new tool belongs in.
- **No secrets, no internal data.** This repo is public. Don't commit real company names,
  internal service maps, partner integration names, or anything from a private
  `profiles/*.md` you authored for your own project — those stay local/private.
- **Heavy samples go on Releases, not in git.** `examples/` is for one small, currently
  actively-referenced sample (README links to it, CI builds it). A new full sample
  (generated skill + handbook + built HTML, easily several MB) should ship as a
  [release asset](https://github.com/mthang1801/flow-trace-genesis/releases) instead of
  a repo commit — attach it to a release and link it from the README/PR, the way the
  `v0.1.0` grpc-go sample HTML is attached. Keeps `git clone` fast as samples accumulate.

## Running the checks locally

```bash
python3 -m pip install pyyaml
python3 plugins/flow-trace-genesis/skills/flow-trace-genesis/render/build.py examples/grpc-go/docs/flows/unary-invoke-client
python3 plugins/flow-trace-genesis/skills/flow-trace-genesis/render/check.py examples/grpc-go/docs/flows/unary-invoke-client
./installers/doctor.sh
shellcheck installers/*.sh scripts/*.sh
```

These are exactly what CI runs (`.github/workflows/ci.yml`) — green locally means green
in the PR check.

## Commit style

Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`...). Keep the subject line under
~70 chars; put the "why" in the body if it isn't obvious from the diff.

## Scope

Small, focused PRs over large ones. If you're proposing a new tool tier, a new section in
the generated handbook, or a change to the CORE/PROFILE split, open an issue first to
align on direction before investing in the implementation.
