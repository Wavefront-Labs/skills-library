---
id: computing-software.devops-ci-cd.earthly.earthly-satellites-use-manage
name: earthly-satellites-use-manage
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, satellites, earthly-sat, launch, select, no-sat, drop-cache, maintenance-window, sleep]
level: practitioner
status: docs-checked
description: "Launch, select, update and sleep Earthly Cloud satellites with earthly sat commands, use them in CI via EARTHLY_TOKEN, and size them using Init metrics."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/using.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/managing.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly Satellites: use, manage, size

Satellites are remote runners with persistent cache; the build runs remotely, logs stream back and outputs download on success.

## Daily commands
```bash
earthly org select <org-name>
earthly sat launch <satellite-name>      # auto-selected afterwards (recorded in ~/.earthly/config.yml)
earthly sat ls
earthly sat select <satellite-name>
earthly sat unselect                     # back to local builds
earthly --sat <satellite-name> +build    # one build only (or EARTHLY_SATELLITE env var)
earthly --no-sat +build                  # local build while one is selected
earthly sat inspect <satellite-name>
earthly sat rm <satellite-name>          # best while asleep
```
Launch accepts `--size` and `--platform`. For slow transfers, `--no-output` skips downloading results and can combine with `--push`. In CI: `earthly account create-token <token-name>`, set `EARTHLY_TOKEN`, then select the satellite via `earthly sat select`, `--sat` or `EARTHLY_SATELLITE`. Log in to registries first (e.g. `docker login`) to avoid DockerHub rate limits. Pull-through cache is not supported.

## Updates and state
- Cloud satellites auto-update unless pinned with `--version`; pinned ones still get patches. Default maintenance window is 2AM to 4AM in the timezone where the satellite is launched; set it with `earthly satellite launch --maintenance-window 04:00 my-satellite`. `--maintenance-weekends-only` limits updates to Saturday (UTC). Updates happen only while asleep.
- `earthly satellite update my-satellite` (satellite must be asleep). Flags: `--drop-cache` (clears cache, often faster than `earthly prune -a`), `--version v0.6.29`, `--size xlarge` (also drops cache), `--feature-flag cache-pct=30` (replaces the whole flag set; cannot be emptied, recreate instead).
- Satellites sleep after 30 min idle (no compute billed) and wake on a new build. Manual: `earthly sat sleep <name>`, `earthly sat wake <name>`.
- Source IP of Cloud satellites: `35.160.176.56`.

## Sizing and overload
Check resource use with `earthly --exec-stats`. Split work across satellites by running the same target on the same one (`earthly --satellite sat-1 +library-1`). Cancel stale PR builds (GitHub Actions `concurrency` with `cancel-in-progress: true`). Use `--ci` to avoid unneeded outputs. Init output includes lines such as `Utilization: 0 other builds, 0/12 op load` and `GC stats` (e.g.); symptoms of overload include "No space left on device", "Out of memory" and long gaps between steps.

## Checked

2026-11-07. Read in full against satellites.md, using.md, managing.md and best-practices.md (docs/cloud). Commands, launch --size/--platform, maintenance window, update flags, sleep and sizing advice match. Corrected: the default maintenance window is in the timezone where the satellite is launched (skill said local); the Init utilization line is now labelled as an example.
Method: documentation only; no commands were run.
