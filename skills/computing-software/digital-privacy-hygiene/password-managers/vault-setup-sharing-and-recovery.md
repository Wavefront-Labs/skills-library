---
id: computing-software.digital-privacy-hygiene.password-managers.vault-setup-sharing-and-recovery
name: vault-setup-sharing-and-recovery
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, bitwarden, 1password, keepassxc, keepass, kdbx, master-password, diceware, passphrase, argon2id, pbkdf2, kdf, password-generator, autofill, import-passwords, bitwarden-send, emergency-access, secret-key, emergency-kit, keyfile, encrypted-export, backup, passkeys, password-sharing, family-vault, vault-recovery]
level: practitioner
status: draft
description: "Set up Bitwarden, 1Password or KeePassXC properly: diceware master passphrase, KDF, import and purge browser passwords, safe autofill, sharing, emergency access, backups."
sources:
  - "https://bitwarden.com/help/kdf-algorithms/"
  - "https://bitwarden.com/help/emergency-access/"
  - "https://bitwarden.com/help/about-send/"
  - "https://support.1password.com/emergency-kit/"
  - "https://support.1password.com/secret-key-security/"
  - "https://keepassxc.org/docs/"
  - "https://www.eff.org/dice"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Password manager vault — set up, share safely, never get locked out

**Goal:** one vault holding a unique random password (or passkey) for every account,
protected by a passphrase you can actually remember, with a written recovery path so
losing a device or forgetting the passphrase is not a catastrophe.

## 1. Choose the tool
- **Bitwarden** — open source, cloud-synced, generous free tier; can be self-hosted.
- **1Password** — paid, polished; your vault key mixes the master password with a
  device-held **Secret Key**, so a stolen server copy is useless on its own.
- **KeePassXC** — free, offline, one encrypted `.kdbx` file you sync yourself (any
  file-sync service or USB). Most control, most responsibility.
- A browser's built-in manager beats nothing, but ties you to one ecosystem.

## 2. Master passphrase and KDF
- Generate **5–6 random words** with dice or the manager's generator (EFF long list:
  ~12.9 bits per word, so 6 words ≈ 77 bits). Example shape: `crane-ladle-bonus-swept-ivory-tuba`.
- Use it nowhere else; write it on the paper recovery sheet (section 6).
- **Bitwarden KDF** (web vault › Settings › Security › Keys; menu names vary by
  version): prefer **Argon2id**; the defaults offered (around 3 iterations, 64 MiB,
  4 threads) are fine. If you stay on PBKDF2, use at least 600,000 iterations — older
  accounts may still carry far lower values, so check. Changing KDF logs out all devices.
- **KeePassXC**: Database › Database Security › Encryption Settings — KDBX 4 with
  Argon2id; use the "benchmark" to target about one second of unlock time.

## 3. Import, then purge the old copies
1. Export from the browser (Chrome/Edge: Password Manager › Settings › Export;
   Firefox: about:logins › ⋯ › Export; Safari/Passwords app: File › Export). The
   export is a **plain-text CSV** — import it straight away, then securely delete it
   and empty the trash.
2. Delete the browser's saved passwords and **turn off "Offer to save passwords"**.
3. Run the manager's health report and work through reused/weak entries (see
   `computing-software.digital-privacy-hygiene.password-hygiene.account-security-audit-and-breach-response`).

## 4. Generator and autofill
- Generator: **20+ random characters** with all classes, or a 4–5 word passphrase
  where you must type it (TV, game console). Shorten only if a site rejects it.
- Save the **passkey** in the manager when a site offers one; all three tools now
  store passkeys (KeePassXC from 2.7.x via its browser extension). Moving passkeys
  between managers is still immature — the FIDO credential-exchange format is
  rolling out, so check before you rely on it.
- Autofill: keep URI matching on **base domain** (never "starts with" for shared
  hosts), and **disable autofill on page load** — fill with a click or shortcut
  (Bitwarden `Ctrl/Cmd+Shift+L`). If the manager offers no match on what looks like
  your bank, treat that as a phishing warning, not a bug. Keep the extension updated
  (2025 research showed clickjacking attacks on several managers' in-page menus).

## 5. Sharing
- **Bitwarden**: an Organisation (Families or Teams) with Collections per household or
  team; **Bitwarden Send** for one-off secrets with expiry, max access count and an
  optional password, sent via a different channel than the link.
- **1Password**: shared vaults; the item "Share" link for people without an account.
- **KeePassXC**: a separate shared `.kdbx` (KeeShare) rather than your personal file.

## 6. Recovery — set it up today
- **Bitwarden**: Emergency Access (premium) lets a trusted contact request access
  after a waiting period you set; also save the **two-step login recovery code**.
- **1Password**: print the **Emergency Kit** (account email, Secret Key, space to
  write the master password). In a family account an organiser can recover members.
- **KeePassXC**: enable "Backup database before saving"; keep copies in at least two
  places. If you add a **keyfile** or hardware key, back those up too — lose the
  keyfile and the database is unrecoverable.
- Export an **encrypted** backup periodically (Bitwarden: "encrypted JSON, password
  protected"; KeePassXC: the `.kdbx` itself is the encrypted backup). Plain CSV/1PUX
  exports are unencrypted — don't leave them lying around.
- Keep the recovery sheet somewhere safe; turn on 2FA for the manager itself
  (`computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`).

## Gotchas
- No vendor can reset a forgotten master password.
- Don't store the manager's own 2FA codes only inside the manager.
- A logged-in device with no lock timeout is an open vault: set vault timeout to lock
  (not log out) after ~15 minutes and on system lock.

## Verify
- [ ] Master passphrase is 5+ random words, used nowhere else, and on the recovery sheet.
- [ ] KDF is Argon2id (or PBKDF2 ≥ 600,000) and confirmed in settings.
- [ ] Browser-saved passwords deleted, browser saving turned off, CSV export destroyed.
- [ ] Autofill on page load is off; matching is base-domain.
- [ ] Emergency access / Emergency Kit / keyfile backup exists and someone knows where.
- [ ] You restored an encrypted backup once on a spare device or fresh profile.
