---
id: computing-software.digital-privacy-hygiene.password-managers.offline-vault-access-during-an-outage
name: offline-vault-access-during-an-outage
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, offline-vault-access, vault-recovery, cloud-vs-local-vault]
level: practitioner
status: draft
description: "Make sure you can still read your vault when the provider is down or you have no internet: cached apps, staying logged in, and offline exports."
sources:
  - "https://bitwarden.com/help/vault-timeout/"
  - "https://support.1password.com/"
  - "https://status.bitwarden.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Offline vault access during an outage

**Goal:** a provider outage, travel without data, or an ISP failure doesn't lock you out of every password.

## How cloud managers behave offline
- **Bitwarden apps** keep an encrypted local copy; if you are logged in (vault timeout action **Lock**, not
  **Log out**), you can unlock offline with master password, PIN or biometrics. The web vault needs the server.
- **1Password apps** keep a local encrypted cache and unlock offline once signed in.
- **KeePassXC** is always offline; sync is your own.

## Prepare
1. Set vault timeout action to **Lock** on at least one desktop and your phone. "Log out" wipes the cache.
2. Test: airplane mode > unlock > open a login.
3. Keep an encrypted export (Bitwarden password-protected JSON, or a KeePassXC copy) on an offline drive,
   refreshed monthly; you can open it with the CLI/another client if all apps fail.
4. Know where the status page is (`status.bitwarden.com`, 1Password status) to distinguish outage from local issue.

## During an outage
- Don't log out to "fix" it: you'll lose the cache.
- Edits made offline may not sync (Bitwarden apps are read-mostly offline); note changes and re-apply.

## Gotchas
- New devices can't log in during an outage; that's why you keep two already-logged-in devices.
- Self-hosted Vaultwarden down = same issue; monitor it.
