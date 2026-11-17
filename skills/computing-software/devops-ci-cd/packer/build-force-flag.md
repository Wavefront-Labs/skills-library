---
id: computing-software.devops-ci-cd.packer.build-force-flag
name: build-force-flag
category: computing-software
field: devops-ci-cd
product: packer
tags: [force, artifacts, rebuild, cmd-build]
level: intro
status: docs-checked
description: "Use packer build -force to let a builder replace artifacts left by an earlier run."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/build/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`-force` tells a builder to run even when artifacts from a previous build would normally stop it. The docs leave the precise meaning to each builder; in general a builder that supports it removes the previous artifacts so you can repeat the build without cleaning up by hand.

```bash
packer build -force .
```

Interactions worth remembering:

- `-on-error=abort` leaves instances and files behind, and the next run may require `-force`.
- With `-force`, the `manifest` post-processor truncates its file at the start of each run. Without it, new builds are appended to the manifest and you use the timestamps to find the latest.
- A builder that does not implement forced builds simply ignores the flag, so read the builder page before relying on it.

## Checked
2026-11-03. Confirmed against the packer build command page (`-force`, `-on-error=abort`) and the manifest post-processor page (truncation with `-force`). Removed the unsourced typical triggers and the CI advice.
Method: documentation only; no commands were run.
