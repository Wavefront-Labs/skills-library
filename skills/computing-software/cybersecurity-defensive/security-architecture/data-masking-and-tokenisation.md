---
id: computing-software.cybersecurity-defensive.security-architecture.data-masking-and-tokenisation
name: data-masking-and-tokenisation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-protection, data-masking, tokenization, tokenisation, pseudonymisation, dynamic-data-masking, test-data-management, format-preserving-encryption, pci-scope-reduction]
level: practitioner
status: draft
description: "Apply masking, tokenisation and pseudonymisation correctly: static masking for test data, dynamic masking for views, vault tokenisation to shrink PCI scope."
sources: ["CompTIA Security+ SY0-701 objective 3.3 (masking, tokenization, obfuscation)", "PCI SSC Tokenization Product Security Guidelines", "NIST SP 800-38G (format-preserving encryption)", "GDPR Article 4(5) pseudonymisation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data masking and tokenisation

**Goal:** people and systems that do not need real sensitive values never see them, while
processes that need realistic data keep working.

## Techniques
| Technique | Reversible | Use |
|---|---|---|
| Static masking | No | Copies of production for test/dev/analytics |
| Dynamic masking | Original intact; view masked | Support staff see `****1234` in queries/UI |
| Tokenisation (vault) | Yes, via vault | Payment data, national IDs; shrinks PCI scope |
| Vaultless / format-preserving encryption (FF1) | Yes, with key | Keeps format for legacy systems |
| Pseudonymisation (keyed hash, HMAC) | Not without the key / mapping | Analytics linking records without identity |
| Anonymisation (aggregation, generalisation, noise) | No | Publishing statistics |

## Static masking for non-production
- Never copy production data to test without masking; test environments have weaker access controls.
- Preserve referential integrity: the same input maps to the same masked value across tables (deterministic masking).
- Keep format and distributions (valid-looking emails, Luhn-valid test card numbers) so tests still work.
- Watch free-text fields (notes, comments): they contain PII that column rules miss.

## Dynamic masking
SQL Server `ALTER TABLE Customers ALTER COLUMN Email ADD MASKED WITH (FUNCTION = 'email()')`;
grant `UNMASK` only to roles that need it. Snowflake masking policies and BigQuery column-level
policies do the same. It is not a security boundary against users who can run arbitrary
queries (inference attacks); use it for convenience-level protection.

## Tokenisation for PCI
Replace PAN at the point of capture with a token from the provider vault; downstream systems
store tokens only and fall out of PCI scope. Confirm with your QSA which systems leave scope.

## Gotchas
- Plain hashing of low-entropy values (phone numbers, IDs) is reversible by brute force; use HMAC with a secret key.
- Pseudonymised data is still personal data under GDPR.
- Masked datasets combined with others can re-identify people (quasi-identifiers: postcode, birth date, gender).

## Verify
- [ ] A scan of non-production databases finds no real PII/PAN (DLP or data discovery scan).
- [ ] Token vault access logged and restricted to named services.
