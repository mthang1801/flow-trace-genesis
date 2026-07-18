## What changed and why

<!-- 1-3 sentences. Link an issue if there is one. -->

## Evidence

<!--
If this touches the genesis playbook, core-template.md, or render/: what did you run
this against? Link the sample/output (new or updated under examples/, or a diff of an
existing one). "Should work" is not evidence — a golden flow that actually built and
passed check.py is.
-->

## Checklist

- [ ] `python3 render/build.py <flow>` + `python3 render/check.py <flow>` pass
- [ ] `./installers/doctor.sh` still exits 0 (or the new/changed tool is correctly tiered
      as optional and degrades gracefully)
- [ ] `shellcheck` clean on any shell script touched
- [ ] No internal/company-specific data added (this repo is public)
- [ ] If `render/` changed: no second un-synced copy left in-repo
      (`scripts/check-render-sync.sh`)
