---
id: computing-software.networking-hardware-and-wireless.arista-eos.running-config-management
name: running-config-management
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, running-config, startup-config, write-memory, config-replace]
level: practitioner
status: draft
description: "Save, back up, diff and replace EOS configuration using write memory, copy, and configure replace."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Saving, copying and replacing configuration
Goal: manage the lifecycle of configuration files.

```
switch# write memory
switch# copy running-config flash:backup-20261103.cfg
switch# copy running-config scp://backup@192.0.2.70/configs/leaf1.cfg
switch# dir flash:
switch# configure replace flash:backup-20261103.cfg
switch# show running-config diffs
```

- `show running-config diffs` shows differences against startup config.
- `configure replace <file>` computes the minimal diff against the running config and applies it; `ignore-errors` is available (confirm).
- `show startup-config` and `show running-config sanitized` hide secrets for sharing.
- `copy tftp:` / `http:` / `scp:` pull files in.

Gotcha: `configure replace` removes anything not in the file (including management access). Always test against a file that carries management, and consider a `commit timer` session for protection.

Operational tip: automate nightly `copy running-config` to a backup server and keep the last N copies on flash. Compare backups with a text diff tool off-box to spot unauthorised or forgotten changes.

## Verify
- `show running-config diffs` is empty after `write memory`.
- `dir flash:` lists the backup with a non-zero size.
