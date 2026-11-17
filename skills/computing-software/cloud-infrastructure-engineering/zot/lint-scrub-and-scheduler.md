---
id: computing-software.cloud-infrastructure-engineering.zot.lint-scrub-and-scheduler
name: lint-scrub-and-scheduler
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, lint-extension, mandatory-annotations, scrub, bit-rot, scheduler-workers]
level: practitioner
status: docs-checked
description: "Configure Zot lint (required manifest annotations), scrub (periodic blob hash checks) and the background scheduler's numWorkers."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lint, `extensions.lint`:

```json
"lint": { "enable": true, "mandatoryAnnotations": ["annot1", "annot2", "annot3"] }
```

- `enable` is disabled if missing.
- `mandatoryAnnotations`: pushes whose manifest lacks any listed annotation are denied.

Scrub, `extensions.scrub`:

```json
"scrub": { "enable": true, "interval": "24h" }
```

- Periodically hashes blobs to detect errors such as bit rot.
- `interval` is the time between runs; minimum `2h`.
- The table says enabled when missing, while the extensions section says presence enables it; set `false` explicitly to disable.

Scheduler, top-level `scheduler`:

```json
"scheduler": { "numWorkers": 3 }
```

- `numWorkers`: maximum simultaneous background tasks (garbage collection, sync and so on). Default is four times the number of CPUs; most users should not change it.
- Background tasks such as garbage collection and registry synchronization are queued and executed by the scheduler.

## Checked

2026-11-08. Read in full: docs/admin-guide/admin-configuration.md and compared every claim above against it. Removed: the claims that scrub runs on the scheduler and that the scheduler protects foreground API requests (not on this page).

Method: documentation only; no commands were run.
