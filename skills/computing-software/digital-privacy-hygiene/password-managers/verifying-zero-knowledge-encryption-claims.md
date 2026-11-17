---
id: computing-software.digital-privacy-hygiene.password-managers.verifying-zero-knowledge-encryption-claims
name: verifying-zero-knowledge-encryption-claims
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, zero-knowledge-encryption, password-manager-selection, security-whitepaper, vault-metadata]
level: practitioner
status: draft
description: "Check a password manager's zero-knowledge claim: what fields are encrypted, what metadata the server sees, and how a malicious server could attack."
sources:
  - "https://bitwarden.com/help/bitwarden-security-white-paper/"
  - "https://1passwordstatic.com/files/security/1password-white-paper.pdf"
  - "https://www.privacyguides.org/en/passwords/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Verifying zero-knowledge encryption claims

**Goal:** know exactly what a provider (or a thief who copies its database) can read, before you trust it.

## Read the whitepaper for these answers
| Question | Good answer | Red flag |
|---|---|---|
| Which item fields are encrypted client-side? | All: names, usernames, URLs, notes, custom fields | URLs or titles stored in plaintext (the LastPass 2022 backup theft exposed site URLs) |
| How is the vault key derived? | Argon2id or PBKDF2 with high iterations, plus a Secret Key (1Password) | Low fixed PBKDF2 counts, old accounts never upgraded |
| What does the server always see? | Email, item count, revision dates, IP, device list | Browsing history, which item you used when |
| Can the provider reset your password? | No, only via an escrowed recovery you set up | "Forgot password" email restores vault access |
| Are clients open source / reproducible? | Yes, or audited with published reports | Closed, unaudited |

## Malicious-server threat
Zero-knowledge assumes the server is honest about the code and keys it gives you. Ask:
- Is the web vault served fresh from the provider on every load? (A compromised server could ship JS that leaks
  the password.) Prefer installed desktop/mobile apps and browser extensions from the store.
- How are shared keys exchanged in organisations? Check that the client shows a **fingerprint phrase** to verify
  before confirming a member (Bitwarden does).
- Read any published academic analyses of malicious-server attacks and the vendor's response.

## Verify yourself
- Bitwarden: export the encrypted JSON (`bw export --format encrypted_json`) or inspect the network tab in the web
  vault: item names arrive as `2.xxxx|yyyy|zzzz` cipher strings, not text.
- Check the KDF settings page: Bitwarden Settings > Security > Keys.

## Gotchas
- "Military-grade AES-256" says nothing; the key derivation and what is left unencrypted matter.
- Favicons/icons fetched from the provider's icon server leak which sites are in your vault; disable "Show
  website icons" if that matters to your threat model.
