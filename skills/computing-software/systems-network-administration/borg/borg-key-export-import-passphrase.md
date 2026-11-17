---
id: computing-software.systems-network-administration.borg.borg-key-export-import-passphrase
name: borg-key-export-import-passphrase
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-key, key-export, key-import, change-passphrase, paper-key, qr-html, recovery]
level: practitioner
status: docs-checked
description: "Back up and restore a Borg key with borg key export and import (including paper and QR formats) and change the passphrase without changing the key."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/key.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg key export, import and passphrase change

Without the key an encrypted repository cannot be opened. Keyfile repositories keep the key locally, so it must be backed up independently of the data. Repokey and authenticated repositories keep it inside the repository; an export still guards against loss or corruption.

```
borg key export /path/to/repo /path/to/key-backup.txt
borg key export --paper /path/to/repo           # printable, line-checked text
borg key export --qr-html /path/to/repo key.html # printable HTML with QR code
borg key import /path/to/repo /path/to/key-backup.txt
borg key import --paper /path/to/repo            # interactive; do not pass PATH
```

The exported key is still encrypted by the passphrase and the export does not contain the passphrase: recovery needs both, so store them in separate safe places. `--paper` import checks each line for plausibility before accepting the next.

For keyfile repositories, `key import` writes to the file named by `BORG_KEY_FILE` if set, otherwise to the repository's file in `BORG_KEYS_DIR` (overwriting if present, creating if not).

`borg key change-passphrase [REPOSITORY]` changes only the passphrase, not the secrets it protects. Changing it after a compromise does not protect past or future backups. To automate, set `BORG_PASSPHRASE` (old) and `BORG_NEW_PASSPHRASE` (new).

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/key): export formats, import behaviour and BORG_KEY_FILE/BORG_KEYS_DIR rules, change-passphrase scope and automation. Removed: nothing.

Method: documentation only; no commands were run.
