---
id: computing-software.digital-privacy-hygiene.two-factor-auth.recovery-code-inventory
name: recovery-code-inventory
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, recovery-code-inventory, backup-codes, offline-recovery-sheet]
level: practitioner
status: draft
description: "Build an inventory of every account's recovery codes and keys, track when each was generated and used, and keep it current after changes."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://ssd.eff.org/module/how-enable-two-factor-authentication"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Recovery code inventory

**Goal:** for every account with 2FA you know where its recovery codes are, whether any were used, and when
they were last regenerated.

## Inventory columns
| Account | Code type | Count left | Generated | Stored in | Paper copy? |
|---|---|---|---|---|---|
| Google | 10 backup codes | 9 | 2026-03 | Vault + safe | yes |
| GitHub | 16 recovery codes | 16 | 2025-11 | Vault | yes |
| Apple | Recovery key (28 chars) | 1 | 2025-06 | Safe | yes |
| Microsoft | Recovery code | 1 | 2026-01 | Vault | yes |
| Password manager | Bitwarden recovery code / 1Password Emergency Kit | 1 | 2026-02 | Safe only | yes |

Keep it in the vault as a secure note (without the codes themselves if codes are in each item).

## Rules
- Codes for the vault account itself live **outside** the vault (paper).
- Strike through or delete used codes; regenerate when fewer than half remain.
- Regenerate after any suspected exposure (codes photographed, emailed, printed on a shared printer).
- After changing 2FA methods, check whether the site regenerated codes (some do automatically).

## Review cadence
Twice a year with the paper backup review.

## Gotchas
- Some services show codes only once; if you skipped saving them, regenerate now.
- Codes saved as screenshots in the photo library sync to the cloud; delete and regenerate.
