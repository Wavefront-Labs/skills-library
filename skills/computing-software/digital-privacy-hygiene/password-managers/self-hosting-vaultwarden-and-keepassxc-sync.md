---
id: computing-software.digital-privacy-hygiene.password-managers.self-hosting-vaultwarden-and-keepassxc-sync
name: self-hosting-vaultwarden-and-keepassxc-sync
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vaultwarden, bitwarden-self-hosted, self-hosted, keepassxc, syncthing, reverse-proxy, tls, docker, backup-strategy, server-hardening, admin-token, fail2ban]
level: advanced
status: draft
description: "Self-host a Vaultwarden server or sync a KeePassXC database yourself, with TLS, backups and server hardening, so the DIY layer doesn't become the weakest link."
sources:
  - "https://github.com/dani-garcia/vaultwarden/wiki"
  - "https://keepassxc.org/docs/"
  - "https://syncthing.net/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self-hosting Vaultwarden and syncing KeePassXC yourself

**Goal:** run your own password vault infrastructure — a Vaultwarden server or a
self-synced KeePassXC database — without the convenience of "someone else's
servers, audited" that `computing-software.digital-privacy-hygiene.password-managers.vault-setup-sharing-and-recovery`
assumes, and without turning a DIY setup into a single point of failure.

## 1. Vaultwarden — what it actually is
Vaultwarden is an unofficial, open-source, lightweight reimplementation of the
Bitwarden server API (written in Rust), **not** official Bitwarden software and
not endorsed by Bitwarden. Official Bitwarden clients (browser extension,
mobile, desktop) connect to it by pointing at your server URL instead of
bitwarden.com. It exists because the official self-hosted Bitwarden server is
heavier (requires MSSQL, more containers). Vaultwarden has not had the same
level of formal third-party security audit as Bitwarden's own cloud/official
self-host offering — weigh that against the control you gain.

## 2. Minimum viable secure deployment
- **Run it behind TLS, always** — Bitwarden clients refuse to operate fully over
  plain HTTP for anything beyond localhost testing, and a vault API over
  unencrypted HTTP is a non-starter regardless. Use a reverse proxy (Caddy
  auto-TLS via Let's Encrypt, or nginx + certbot) in front of the Vaultwarden
  container; never expose the container's raw port to the internet.
- **Set `ADMIN_TOKEN`** to a long random value (or disable the admin panel route
  entirely once configured) — the admin panel manages all users/orgs on the
  instance and is a prime target if left on a weak or default value.
- **Disable public signups** (`SIGNUPS_ALLOWED=false`) after creating the
  accounts you need, so the instance can't be used by strangers who find it.
- Put the server on a domain/subdomain you control with a firewall allowing only
  443 (and SSH from a restricted source) — not a bare IP with every port open.
- Rate-limit or fail2ban the login endpoint; credential-stuffing bots scan the
  open internet for exposed Bitwarden-compatible login endpoints.

## 3. Backups — the part people skip
- Vaultwarden's SQLite (or Postgres/MySQL, if configured) database plus its
  `rsa_key*`/attachment files directory **is the entire vault**. Back up both,
  not just the database file alone, on a schedule, to storage separate from the
  host (the whole point of self-hosting fails if a single disk failure loses
  everything with no copy elsewhere).
- Test a **restore**, not just a backup job completing — restoring to a scratch
  container and logging in is the only real proof it works.
- Encrypt the backup at rest if it leaves the server (it already contains the
  encrypted vault blobs, but the server's own TLS cert/keys and admin token
  should not travel in plaintext backups either).

## 4. KeePassXC without a managed sync service
If you don't want any server at all, KeePassXC's `.kdbx` file can sync via a
general-purpose tool instead of a vendor's infrastructure:
- **Syncthing**: peer-to-peer, no cloud intermediary, end-to-end encrypted
  transport between your own devices. Good fit philosophically with KeePassXC's
  "your file, your control" model. Watch for **sync conflicts**: editing the
  database on two unsynced devices before they reconnect creates a conflicted
  copy file — KeePassXC itself has no merge logic, so you must manually compare
  and merge, or discipline yourself to only edit on one device at a time.
- A generic cloud sync folder (Dropbox/OneDrive/a self-hosted Nextcloud) works
  too, with the same conflict risk; Nextcloud if you want to avoid a third-party
  cloud entirely.
- Either way, enable "Backup database before saving" in KeePassXC and keep that
  backup path itself included in your sync/backup plan, not excluded.

## Gotchas
- A self-hosted instance means **you** are the one who has to keep it patched;
  an unpatched Vaultwarden/Syncthing exposed to the internet is a worse outcome
  than a maintained commercial service — don't self-host and then neglect updates.
- Losing the server's encryption-at-rest key/attachment directory without a
  backup is unrecoverable, same as losing a KeePassXC keyfile.
- Uncertain: Vaultwarden's feature parity with official Bitwarden server shifts
  release to release (e.g. org SSO support); check current docs before relying
  on a specific feature.

## Verify
- [ ] Server only reachable over TLS; raw container port not exposed.
- [ ] Admin token set to a long random value or admin panel disabled after setup.
- [ ] Public signups disabled once accounts exist.
- [ ] A full restore (database + attachments) has actually been tested, not just
      a backup job running.
- [ ] If using Syncthing/cloud sync for KeePassXC, you have a plan for conflict
      files and "Backup database before saving" is on.
