---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-masking-tokenisation
name: data-masking-tokenisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, data-masking, tokenisation, pseudonymisation, dynamic-data-masking, format-preserving-encryption]
level: practitioner
status: draft
description: "Protect sensitive fields with tokenisation and masking: static masking for non-prod, dynamic masking, vault vs vaultless tokens, FPE, and scope reduction for PCI."
sources: ["https://www.pcisecuritystandards.org/documents/Tokenization_Guidelines_Info_Supplement.pdf", "https://cloud.google.com/sensitive-data-protection/docs/pseudonymization", "https://learn.microsoft.com/sql/relational-databases/security/dynamic-data-masking", "https://csrc.nist.gov/pubs/sp/800/38/g/upd1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tokenisation and data masking

## Steps
1. **Choose per use case**:
   - *Static masking*: irreversible substitution for test/dev copies (realistic but fake data).
   - *Dynamic masking*: query-time masking by role (Azure SQL/SQL Server DDM, Snowflake masking
     policies, BigQuery data masking); protects display, not determined attackers with query access.
   - *Tokenisation*: replace values with tokens; vaulted (token-to-value table in a secured
     service) or vaultless (cryptographic). Reduces PCI DSS scope when systems hold only tokens.
   - *Format-preserving encryption* (NIST SP 800-38G FF1) when formats must be kept; Google
     Sensitive Data Protection offers FPE and deterministic encryption transforms.
2. **Deterministic vs random**: deterministic tokens allow joins and lookups but leak equality;
   use random where joins are unnecessary.
3. **Key and vault protection**: detokenisation as a tightly controlled API with audit logs;
   keys in KMS/HSM.
4. **Pipelines**: mask in the copy pipeline from prod to non-prod; never copy then mask.
5. **Validate**: scan masked datasets with discovery tools to prove no residual PII.

## Gotchas
- Dynamic masking is bypassable by inference queries; do not treat it as encryption.
- Free-text fields leak PII that column masking misses.

## Verify
- [ ] Non-prod copies scanned clean of real sensitive data.
- [ ] Detokenisation access audited and least-privileged.
