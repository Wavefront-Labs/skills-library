---
id: computing-software.digital-privacy-hygiene.password-managers.keepassxc-cli-scripted-lookups
name: keepassxc-cli-scripted-lookups
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, keepassxc-cli, password-manager-cli, keepassxc, kdbx, diceware, keepassxc-analyze]
level: practitioner
status: docs-checked
description: "Query, add and audit a KeePassXC database from the terminal with keepassxc-cli: show, clip, generate, diceware, analyze."
sources:
  - "https://raw.githubusercontent.com/keepassxreboot/keepassxc/develop/docs/man/keepassxc-cli.1.adoc"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keepassxc-cli

**Goal:** script against a local vault (backups, health checks, password retrieval on headless machines) without
the GUI.

## Common commands
```bash
keepassxc-cli ls vault.kdbx                       # list root group
keepassxc-cli search vault.kdbx github
keepassxc-cli show vault.kdbx "Web/GitHub"        # entry fields, protected ones hidden
keepassxc-cli show -s -a Password vault.kdbx "Web/GitHub"   # print one attribute
keepassxc-cli show -t vault.kdbx "Web/GitHub"     # current TOTP
keepassxc-cli clip vault.kdbx "Web/GitHub" 15     # copy to clipboard, optional timeout in seconds
keepassxc-cli add -u alice -g -L 24 vault.kdbx "Web/NewSite"
keepassxc-cli generate -L 24 -l -U -n -s          # random password
keepassxc-cli diceware -W 6                       # passphrase of 6 words
keepassxc-cli db-info vault.kdbx                  # database information
```
Key file: `-k vault.keyx`; YubiKey: `-y <slot[:serial]>`. Add `--no-password` for key-file-only databases. The
`clip` timeout defaults to 10 seconds, and 0 disables the automatic clear.

## Breach audit
`keepassxc-cli analyze -H <filename> vault.kdbx` (`--hibp`) takes a filename for a Have I Been Pwned password
list. Read the man page for the list format it expects before relying on the result.

## Scripting safely
- Never put the database password on the command line as an argument; let the CLI prompt for it.
- `open` starts an interactive session so several commands share one unlock.

## Verify
- [ ] `show -s -a Password` returns the right value for a test entry.
- [ ] Flagged entries from `analyze` rotated.

## Checked
2026-11-01. Confirmed against the keepassxc-cli man page source (docs/man/keepassxc-cli.1.adoc): commands ls,
search, show, clip [timeout], add, generate, diceware, db-info, analyze, open; options -u, -g, -L, -l, -U, -n, -s,
-W, -H/--hibp, -k, -y, --no-password, -s/-a/-t on show; clip default 10 seconds and 0 disables clearing.
Removed as unconfirmed: KDF and cipher output of db-info, the HIBP downloader instructions, offline-only
behaviour, GUI report description, and prompt-on-TTY wording.
Method: documentation only; no commands were run.
