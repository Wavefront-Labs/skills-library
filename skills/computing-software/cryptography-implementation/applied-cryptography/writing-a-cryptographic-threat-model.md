---
id: computing-software.cryptography-implementation.applied-cryptography.writing-a-cryptographic-threat-model
name: writing-a-cryptographic-threat-model
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, algorithm-selection, crypto-threat-model, threat-modeling, adversary-model, security-requirements, design-review]
level: advanced
status: draft
description: "Write the threat model a crypto design needs: assets, adversary capabilities, trust boundaries, required properties per data flow, and the assumptions that would break it."
sources: ["https://www.schneier.com/books/cryptography-engineering/", "https://owasp.org/www-community/Threat_Modeling", "https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a cryptographic threat model

Cryptography Engineering ch 1-2: you cannot evaluate a cryptographic design
without knowing what it must withstand. "Encrypt the data" is not a
requirement; "an attacker with read access to the database and backups must
not learn customers' national ID numbers" is.

## One page, five sections

1. **Assets**: what must be protected and for how long (session tokens:
   hours; health records: decades; signing keys: their certificate's life).
2. **Adversaries and capabilities**, concretely:
   - Network: passive observer, active MITM, can replay/reorder/drop.
   - Storage: reads DB, reads backups, writes DB (tampering, swapping rows).
   - Insider: DBA, cloud admin, support staff, CI system.
   - Endpoint: malware on a client, stolen laptop (powered off vs on).
   - Future: quantum computer for long-lived data; key compromise later.
3. **Trust boundaries and keys**: where each key lives, who can use it, what
   happens if it leaks.
4. **Required properties per flow**: for each data flow, mark confidentiality,
   integrity, authenticity (of whom), replay protection, forward secrecy,
   non-repudiation, unlinkability/metadata privacy. Many designs fail because
   they deliver confidentiality where integrity was the real need.
5. **Assumptions and out of scope**: "we trust the KMS", "client devices are
   not compromised", "clocks are within 5 minutes". Each assumption is a test
   for reviewers.

## Example row

| Flow | Adversary | Needs | Mechanism |
|---|---|---|---|
| Card data at rest | DB reader, backup thief | Confidentiality, integrity bound to row | FLE AES-GCM, AAD=row id, DEK per tenant via KMS |
| Webhook to partner | Network MITM, replay | Authenticity, freshness | HMAC-SHA256 over timestamp+body, 5-min window, TLS |
| Audit log | Insider with DB write | Tamper evidence | Hash chain + daily signed checkpoint to external store |

## Use it

- Pick primitives from the properties (see choosing primitives skill).
- Review: for each adversary, walk through what they see and can modify.
- Revisit when the architecture changes (new replica, new region, new
  third party) - most crypto breaks come from changed assumptions, not broken
  algorithms.

## Verify

- [ ] Every crypto mechanism maps to a property and adversary in the model.
- [ ] Assumptions listed and owned; reviewers signed off.
- [ ] Model updated in the last architecture change.
