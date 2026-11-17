---
id: computing-software.cryptography-implementation.applied-cryptography.mapping-crypto-to-compliance-regimes
name: mapping-crypto-to-compliance-regimes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, compliance-crypto-mapping, pci-dss, pci-dss-4, hipaa, fedramp, fips-140-3, gdpr, soc-2, strong-cryptography, audit-evidence]
level: practitioner
status: draft
description: "Map algorithm, key length and key-management choices to PCI DSS 4.0, HIPAA, FedRAMP/FIPS, GDPR and SOC 2 expectations, and produce auditor evidence."
sources: ["https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf", "https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html", "https://www.fedramp.gov/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mapping crypto to compliance regimes

## What each regime actually asks
| Regime | Crypto expectation |
|---|---|
| PCI DSS 4.0.1 | "Strong cryptography" = industry-tested algorithms with at least 112-bit effective strength. Req 3.5 render PAN unreadable; 3.6/3.7 key management procedures; 4.2.1 strong crypto for PAN in transit with valid certificates; 12.3.3 annual review of cipher suites and protocols in use (an inventory). |
| HIPAA Security Rule | Encryption at rest/in transit is "addressable" (164.312(a)(2)(iv), (e)(2)(ii)); HHS breach guidance treats data encrypted per NIST SP 800-111 / 800-52 as "secured" (breach safe harbour). |
| FedRAMP / FISMA | FIPS 140-validated modules for all cryptographic protection (SC-13); TLS per SP 800-52 Rev 2. |
| GDPR | Art 32 names encryption as an appropriate measure; Art 34 lets you skip notifying individuals if breached data was unintelligible (encrypted, keys not compromised). |
| SOC 2 | No fixed algorithms; auditors check that your stated controls (encryption, key rotation) are implemented and evidenced. |

## Building the mapping
1. Start from your cryptographic inventory (algorithm, key length, mode, library and version, where used).
2. For each row, record which control it satisfies and the evidence location.
3. Flag rows that need FIPS-validated modules (federal workloads) separately from rows that just need strong
   algorithms.

## Evidence auditors ask for
- TLS scan output (testssl.sh/SSLyze) per external endpoint.
- KMS/HSM key policies, rotation settings and access logs.
- CMVP certificate numbers for modules claimed as FIPS-validated, plus proof they run in approved mode.
- Key management procedures signed by key custodians (PCI 3.6.1.2/3.7).

## Gotchas
- "AES-256 encrypted" disk volumes do not satisfy PCI 3.5 alone if the same OS account can read decrypted data;
  PCI 3.5.1.2 restricts disk-level encryption for this reason.
- FIPS-validated library in non-approved mode does not count.
- Hashing PANs requires keyed hashes (PCI 3.5.1.1 in 4.0).

## Verify
- [ ] Every inventory row maps to a control and evidence link.
- [ ] Cipher-suite inventory review is dated within the last 12 months.
