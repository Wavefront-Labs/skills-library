---
id: computing-software.cloud-infrastructure-engineering.zot.retention-dry-run-verify
name: retention-dry-run-verify
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, verify-feature, retention-dry-run, gc-interval-override, preview-deletions]
level: advanced
status: docs-checked
description: "Preview Zot retention decisions safely with zot verify-feature retention or dryRun: options, requirements, and the orphan-blob deletion caveat."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Command:

```
zot verify-feature retention <config-file>
```

It forces dry-run mode for all retention policies, logs tag and orphan-manifest decisions without deleting them, and does not need the server running. It runs until SIGINT or SIGTERM unless a timeout is set.

Options:
- `-l, --log-file`: write logs to a file instead of stdout.
- `-i, --gc-interval`: override the GC interval for all storage paths including subpaths.
- `-t, --timeout`: how long to wait for tasks; indefinite if omitted.

Requirements:
- `"gc": true` in the config.
- For local storage, stop the Zot server first to avoid database lock conflicts.
- A valid, readable config.

Warning: garbage collection still runs and permanently deletes unreferenced orphan blobs during verification.

Alternative: set `"dryRun": true` in the `retention` block to log removals while a live server runs.

## Checked

2026-11-04. Read against the zot retention article (Testing retention policies). Removed: a worked-expectations sentence about the v2.* example that oversimplified the docs example.

Method: documentation only; no commands were run.
