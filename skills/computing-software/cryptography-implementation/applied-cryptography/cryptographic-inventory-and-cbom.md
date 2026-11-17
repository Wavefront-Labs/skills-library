---
id: computing-software.cryptography-implementation.applied-cryptography.cryptographic-inventory-and-cbom
name: cryptographic-inventory-and-cbom
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, post-quantum-migration, cryptographic-inventory, cbom, cyclonedx, crypto-agility, discovery, pq-migration]
level: practitioner
status: draft
description: "Build a cryptographic inventory for PQ migration: what to record, discovery across code, endpoints, certs and keys, and CycloneDX CBOM output."
sources: ["https://cyclonedx.org/capabilities/cbom/", "https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms", "https://www.whitehouse.gov/wp-content/uploads/2022/11/M-23-02-M-Memo-on-Migrating-to-Post-Quantum-Cryptography.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cryptographic inventory and CBOM

You cannot migrate what you have not found. A cryptographic inventory
lists every algorithm, key and protocol in use, who owns it, and how long
the protected data must stay secret. US OMB M-23-02 requires federal
agencies to submit one annually; it is the first step of every PQ plan.

## What to record per asset

- Algorithm, parameters, key size (RSA-2048, P-256, AES-128-GCM).
- Use: key exchange, signature, encryption at rest, hashing.
- Where: system, repository, endpoint, HSM/KMS key id, library and version.
- Data sensitivity and **secrecy lifetime** (how long confidentiality matters).
- Owner, vendor dependency, and whether it is configurable (crypto agility).

## Discovery sources

| Source | Tooling |
|---|---|
| Source code | Semgrep/CodeQL crypto rules, IBM `sonar-cryptography`, CBOMkit |
| Dependencies | SBOM (Syft) to find crypto libraries and versions |
| TLS/SSH endpoints | `sslyze`, `testssl.sh`, `nmap --script ssl-enum-ciphers,ssh2-enum-algos` |
| Certificates | CT logs for your domains, internal CA databases, cert stores |
| Keys | KMS/HSM key listings (key spec, creation date) |
| Network | Passive TLS metadata (Zeek `ssl.log`) |
| Vendors | Questionnaires for appliances and SaaS |

## Output: CycloneDX CBOM

CycloneDX 1.6 adds `cryptographic-asset` components (algorithm,
certificate, protocol, related-crypto-material) with properties such as
`primitive`, `parameterSetIdentifier`, `nistQuantumSecurityLevel`.
Generate per repo in CI and aggregate.

## Keep it alive

- Regenerate from CI and scanners, not a one-off spreadsheet.
- Diff each release; new quantum-vulnerable usage needs an exception.
- Feed into the prioritisation (harvest-now-decrypt-later) skill.

## Verify

- [ ] Every production system has an owner and an inventory entry.
- [ ] CBOM generated in CI for each service.
- [ ] Each quantum-vulnerable asset has a target date.
