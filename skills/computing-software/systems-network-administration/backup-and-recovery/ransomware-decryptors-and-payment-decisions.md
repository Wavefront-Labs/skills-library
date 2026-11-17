---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-decryptors-and-payment-decisions
name: ransomware-decryptors-and-payment-decisions
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [decryptor, ransom-payment, ransomware-recovery, ofac-sanctions, incident-response, cyber-insurance]
level: advanced
status: draft
description: "Handle the decryptor and ransom question in a ransomware incident: free decryptors, sanctions and reporting rules, insurer and counsel roles, and testing any decryptor safely."
sources:
  - https://www.nomoreransom.org/
  - https://home.treasury.gov/policy-issues/financial-sanctions/recent-actions/20210921
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://www.ncsc.gov.uk/ransomware/home
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decryptors and ransom payment considerations

**Goal:** make the payment/decryptor decision quickly, lawfully and with evidence, while recovery from backups continues in parallel.

## First: is there a free decryptor?
- Identify the strain from the ransom note and an encrypted sample (ID Ransomware, vendor IR team).
- Check **No More Ransom** (nomoreransom.org) and security-vendor decryptor pages. Some families have flaws or seized keys.
- Run any decryptor only on **copies** of encrypted files in an isolated environment first.

## The payment question (owned by executives + legal, not IT)
- Law enforcement (FBI, CISA, NCSC) advise against paying: no guarantee of a working key or of stolen data being deleted, and it funds further attacks.
- **Sanctions**: paying a sanctioned group or jurisdiction can be illegal (US OFAC advisory; UK, EU equivalents). Counsel and the negotiator must screen the threat actor.
- **Reporting duties** may apply to payments (e.g. Australia requires ransomware payment reporting for in-scope businesses; some public sectors are barred from paying). Check current law in each jurisdiction.
- **Cyber insurance**: notify the insurer immediately; policies often dictate approved IR firms, negotiators and whether payment is covered.
- Record the decision rationale; regulators and boards will ask.

## If a decryptor is obtained (paid or otherwise)
- Have a reputable IR firm vet the binary in a sandbox; criminal decryptors can carry malware or be buggy.
- Decryption is often slow and fails on large files or partially encrypted ones; test on representative samples and back up the encrypted data before running it.
- Decrypt into clean rebuilt systems, not compromised hosts.
- Prefer backups wherever they meet RPO; use the decryptor only for data with no clean backup.

## Gotchas
- Double extortion: even with perfect backups, the actor may leak exfiltrated data; payment does not reliably prevent it.
- Contacting the actor directly without counsel can harm legal position and negotiations.

## Verify
Post-incident, the decision log shows: decryptor search done, sanctions screening, insurer and law enforcement notified, and who approved the outcome.
