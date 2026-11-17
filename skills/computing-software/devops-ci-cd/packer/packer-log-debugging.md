---
id: computing-software.devops-ci-cd.packer.packer-log-debugging
name: packer-log-debugging
category: computing-software
field: devops-ci-cd
product: packer
tags: [packer-log, logging, troubleshooting, log-path, debugging]
level: practitioner
status: docs-checked
description: "Turn on verbose logs with PACKER_LOG and PACKER_LOG_PATH, and what the value rules are."
sources:
  - "https://developer.hashicorp.com/packer/docs/debugging/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`PACKER_LOG` enables detailed logging to stderr. Any value other than an empty string or `0` turns it on.

```bash
PACKER_LOG=1 packer build .
PACKER_LOG=1 PACKER_LOG_PATH=packer.log packer build .
```

`PACKER_LOG_PATH` writes the log to a file instead; it only takes effect when `PACKER_LOG` is also set.

On Windows PowerShell:

```powershell
$env:PACKER_LOG=1
packer build .
```

The debugging page lists other tools:

- `-on-error=ask` leaves a failed machine for inspection.
- `-debug` steps through builds, and writes an SSH key for cloud builders.
- The `breakpoint` provisioner pauses at a place you choose.
- Plugins run as separate processes communicating over RPC, so attaching a debugger to a plugin is hard; rely on logs.

## Checked
2026-11-03. Confirmed against the Debugging Packer Builds page: `PACKER_LOG` value rule, stderr output, `PACKER_LOG_PATH` needing `PACKER_LOG`, the PowerShell form and plugin debugging. Removed unsourced closing advice.
Method: documentation only; no commands were run.
