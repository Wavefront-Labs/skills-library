---
id: computing-software.digital-privacy-hygiene.password-managers.bitwarden-cli-unlock-and-item-retrieval
name: bitwarden-cli-unlock-and-item-retrieval
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, bitwarden-cli, password-manager-cli, bw, bw-session, jq, scripting, api-key-login]
level: practitioner
status: docs-checked
description: "Use the Bitwarden CLI (bw) to log in, unlock to a session key, fetch passwords/TOTP/fields in scripts, and lock again without leaving secrets in shell history."
sources:
  - "https://bitwarden.com/help/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bitwarden CLI

**Goal:** pull secrets from your vault into scripts and terminals without
copy-pasting or hard-coding.

## Install and log in
```bash
npm install -g @bitwarden/cli     # or the native binary / snap / choco
bw config server https://your.bw.domain.com   # only for self-hosted
bw login                          # interactive: email, master password, 2FA
# non-interactive login with a personal API key (still needs unlock afterwards):
#   export BW_CLIENTID=<client_id> BW_CLIENTSECRET=<client_secret>; bw login --apikey
```

## Unlock to a session
```bash
export BW_SESSION="$(bw unlock --raw)"   # prompts for master password
bw sync                                   # pull latest vault
```
`BW_SESSION` holds the key that decrypts the local vault cache; anyone with it and
the cache reads the vault. Keep it in the current shell only.

## Retrieve
```bash
bw list items --search github | jq '.[] | {id, name}'
bw get password <id-or-search-term>
bw get username <id>
bw get totp <id>
bw get item <id> | jq -r '.fields[] | select(.name=="Phone PIN").value'
bw get attachment backup.pdf --itemid <id> --output ./
bw generate -uln --length 24            # or: bw generate --passphrase --words 6
```
Prefer the item id over a search term so the right item is returned.

## Finish
```bash
bw lock; unset BW_SESSION
```

## Gotchas
- Never `echo` secrets into files or command lines visible in `ps`; pipe directly
  (`bw get password x | some-tool --password-stdin`).
- Keep sensitive values out of shell history; `bw unlock --passwordenv <VAR>` reads the master password from an
  environment variable instead of typing it (a `--passwordfile` must be readable only by you).
- The CLI keeps its configuration in a `data.json`; `BITWARDENCLI_APPDATA_DIR` points to another location. Use
  `bw logout` on shared machines.

## Verify
- [ ] `bw status` shows `"status":"unlocked"` only while working, `locked` after.

## Checked
2026-11-01: install, `config server`, `login --apikey` and BW_CLIENTID/BW_CLIENTSECRET, unlock and BW_SESSION, session
invalidation by `bw lock`/`bw logout`, `get` subcommands, `--itemid`/`--output` for attachments, `generate` options,
`sync` and `status` confirmed against the Bitwarden CLI help page. Removed: HISTCONTROL tip, default data path, and the
unverified multi-match error behaviour.
Method: documentation only; no commands were run.
