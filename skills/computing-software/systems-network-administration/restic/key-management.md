---
id: computing-software.systems-network-administration.restic.key-management
name: key-management
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, key, key-add, key-passwd, key-list, key-remove, encryption]
level: practitioner
status: docs-checked
description: "Manage restic repository keys: list, add, remove and change passwords with the key subcommands, and understand what a password change does not do."
sources:
  - https://restic.readthedocs.io/en/stable/070_encryption.html
  - https://restic.readthedocs.io/en/stable/100_references.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing repository keys

A repository can have several keys, each protected by its own password. All of them unlock the same master key.

```
restic -r /srv/restic-repo key list
restic -r /srv/restic-repo key add
restic -r /srv/restic-repo key remove <ID>
restic -r /srv/restic-repo key passwd
```

## What each does

- `key list` prompts for a valid password and prints ID, User, Host and Created. The key you used is marked with an asterisk.
- `key add` asks for the current password, then the new password twice, and saves a new key file.
- `key passwd` changes a password.
- `key remove` deletes a key.

## Important limit

A repository can have several passwords, each with its own key file, so a password can change without re-encrypting all data. The design document says a leaked key gives access to the master key, so a password change does not help: the master key can only be changed with `copy` into a new repository, or by making a completely new repository.

`--key-hint` and `RESTIC_KEY_HINT` give the ID of the key to try decrypting first.

## Checked

2026-11-03. Confirmed in the restic docs pages Encryption (key list/add output, asterisk marks the current key, list/add/remove/passwd sub-commands), Design (key files, leaked-key limits, `copy` for a new master key) and the command reference (`--key-hint`). Removed: the advice not to remove the current key and the per-user key recommendation (not in the docs).

Method: documentation only; no commands were run.
