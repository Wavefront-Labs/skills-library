---
id: computing-software.systems-network-administration.backup-and-recovery.restic-key-and-password-management
name: restic-key-and-password-management
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic, restic-key, repository-password, key-management, password-file, backup-encryption]
level: practitioner
status: docs-checked
description: "Manage restic repository keys and passwords: key list, add, passwd and remove, per-admin keys, password files and escrow, and what to do if a password is exposed."
sources:
  - https://restic.readthedocs.io/en/stable/070_encryption.html
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic key management and repository passwords

**Goal:** control who can open a repository, rotate access, and never lose the only key.

## Model
A restic repository has one **master key** that encrypts all data. It is stored in the repository wrapped by one or more **key files**, each protected by a password. Any valid password opens the repository.

## Commands
```bash
restic key list                     # IDs, users, hosts, creation times; * marks the current key
restic key add                      # prompts for a new password (or --new-password-file)
restic key passwd                   # creates a new key, validates it and removes the old key ID
restic key remove <key-id>          # refuses to remove the key currently in use
```
Use `--user` and `--host` with `key add` to label keys per administrator or automation host.

## Practices
- One key for automation (password file readable only by the backup service account, `chmod 600`), separate keys per human administrator.
- Escrow at least one password offline (sealed envelope in a safe, or a separate vault), because losing all passwords means losing all data.
- Remove keys when staff leave (`key remove`).
- Do not put passwords on the command line or in shell history; use `RESTIC_PASSWORD_FILE` or `RESTIC_PASSWORD_COMMAND` (e.g. fetch from a vault).

## If a password is exposed
Removing the key stops that password from opening the repository in future, but an attacker with a leaked decrypted key can decrypt existing and future data: a password change does not change the master key. The master key can only be replaced by moving the data into a new repository with `restic copy`, or by making a new repository and new backups.

## Verify
`restic key list` shows only expected keys, and the escrowed password opens the repository in a test (`restic -r <repo> --password-file <escrow> snapshots`).

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: key list/add/passwd/remove behaviour, --new-password-file, --user and --host on key add, asterisk marking the current key, RESTIC_PASSWORD_FILE and RESTIC_PASSWORD_COMMAND, and that only copy or a new repository changes the master key (070_encryption, design, man pages).

Method: documentation only; no commands were run.
