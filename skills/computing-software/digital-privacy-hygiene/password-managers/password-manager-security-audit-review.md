---
id: computing-software.digital-privacy-hygiene.password-managers.password-manager-security-audit-review
name: password-manager-security-audit-review
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, pm-security-audit, password-manager-selection, choosing-a-password-manager, security-audit, open-source, zero-knowledge, bug-bounty, whitepaper, bitwarden, 1password, keepassxc]
level: practitioner
status: draft
description: "Judge a password manager's security claims before trusting it: read its audit reports, whitepaper, bug bounty and incident history instead of its marketing page."
sources:
  - "https://ssd.eff.org/module/choosing-password-manager"
  - "https://www.privacyguides.org/en/passwords/"
  - "https://bitwarden.com/help/is-bitwarden-audited/"
  - "https://1password.com/security"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing a password manager's security evidence

**Goal:** decide whether a password manager deserves your whole credential set,
based on evidence a third party produced, not on "military-grade encryption".

## 1. Collect the evidence (30 minutes per product)
| Evidence | Where to look | What good looks like |
|---|---|---|
| Third-party audit reports | Vendor "security"/"compliance" page (Bitwarden: help article "Is Bitwarden audited?", 1Password: security page) | Named firm (Cure53, Trail of Bits, NCC, ISE etc.), date in the last ~2 years, full report or detailed summary, findings and fix status listed |
| Security design whitepaper | 1Password Security Design white paper; Bitwarden Security Whitepaper | Explains key derivation, what is encrypted client-side, what metadata the server sees |
| Source availability | GitHub org | Clients open source (Bitwarden, KeePassXC, Proton Pass) lets others verify; closed source is not disqualifying if audits are strong |
| Bug bounty | HackerOne/Bugcrowd page | Public programme with paid payouts and visible resolved reports |
| Incident history | Vendor blog, news, CVE search | Prompt, specific disclosure; not "no customer data affected" followed by months of corrections |

## 2. Read an audit report properly
- Check **scope**: an audit of the marketing website or one browser extension says
  nothing about the server or mobile apps. Note which components were in scope.
- Check **severity and status**: High/Critical findings are normal; what matters is
  that they were fixed and retested, with the retest dated.
- Check **independence**: the vendor commissioning the audit is normal; a report
  that is only a one-paragraph "attestation letter" with no findings is weak.
- SOC 2 Type II reports cover operational controls, not cryptographic design;
  treat them as complementary, not as a crypto audit.

## 3. Questions to answer in the whitepaper
- Is the vault encrypted with a key derived **only on your device** from your master
  password (plus 1Password's Secret Key)? The server must never receive it.
- Which fields are **not** encrypted? (Vault item URLs were plaintext in the LastPass
  2022 backup theft; see
  `computing-software.digital-privacy-hygiene.password-managers.lastpass-breach-lessons-for-vault-users`.)
- What is the KDF and its default cost (PBKDF2-SHA256 600,000 iterations or Argon2id
  is the current baseline per OWASP guidance)?
- How is sharing done (public-key encryption between users) and how is account
  recovery done (does an admin or the vendor hold a key that can decrypt you)?

## 4. Decision rule
Accept a product when: recent audit covering clients and server, published
whitepaper answering the questions above, active bug bounty, clean or well-handled
incident history, and an export path (see
`computing-software.digital-privacy-hygiene.password-managers.vault-portability-check-before-committing`).
Any password manager that clears this bar is far safer than reused passwords;
do not let perfect block good.

## Gotchas
- "Zero-knowledge" is a marketing term; verify it against the whitepaper.
- Old audits of a codebase that has since been rewritten (new extension
  architecture, new sync server) have little value.
- Uncertain: audit cadence changes; check the vendor's current page rather than
  relying on any date written here.

## Verify
- [ ] You can name the audit firm, date and scope for the product you chose.
- [ ] You know which vault fields are unencrypted server-side.
- [ ] You know the default KDF and that your account uses it.
