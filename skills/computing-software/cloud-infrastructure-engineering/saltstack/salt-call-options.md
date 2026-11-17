---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-call-options
name: salt-call-options
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-call, local, masterless, file-root, pillar-root, retcode-passthrough]
level: practitioner
status: docs-checked
description: "Run functions on a minion with salt-call: --local masterless mode, --file-root, --pillar-root, --retcode-passthrough, --id, --master and grain options."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/cli/salt-call.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt-call options

- `--local`: run as if no master were running.
- `--file-root=DIR` and `--pillar-root=DIR`: set base file or pillar roots; repeatable.
- `--retcode-passthrough`: exit with the function's return code rather than salt-call's.
- `-g`, `--grains`: return the grains information.
- `-m DIR`, `--module-dirs=DIR`: extra module directory; repeatable.
- `--master=MASTER`: master to use (default: from the minion config).
- `--id=ID`: minion ID (default: `id` in the minion config).
- `--skip-grains`: do not load grains.
- `--refresh-grains-cache`: force a grains cache refresh.

## Checked

2026-11-09. Read against the salt-call reference source (doc/ref/cli/salt-call.rst); every option and default left was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
