---
id: computing-software.cybersecurity-defensive.security-architecture.data-minimisation
name: data-minimisation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-minimisation, data-minimization, privacy-by-design, gdpr-article-5, pseudonymisation, retention-limits, log-redaction]
level: practitioner
status: draft
description: "Reduce breach impact by minimising data: collection review, field-level necessity, pseudonymisation, retention deletion jobs, log and analytics redaction, and test data hygiene."
sources: ["https://gdpr-info.eu/art-5-gdpr/", "https://www.nist.gov/privacy-framework", "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/the-principles/data-minimisation/", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data minimisation

Data you do not hold cannot be breached. GDPR Art. 5(1)(c): adequate, relevant and limited to what
is necessary.

## Process
1. **Field inventory:** for each system list the personal/sensitive fields, purpose, legal basis, consumer. Fields with no named consumer are deletion candidates.
2. **Collection:** remove optional form fields nobody uses; collect year instead of date of birth, postcode district instead of full address, last 4 digits instead of full PAN where that is all that is needed.
3. **Derive and discard:** compute what you need (age band, eligibility flag) and drop the raw input.
4. **Pseudonymise** analytics: replace identifiers with keyed hashes (HMAC with a secret key, not plain SHA-256 of an email - that is reversible by dictionary).
5. **Retention:** scheduled deletion jobs per data class (and object storage lifecycle rules); verify deletion runs.
6. **Logs and telemetry:** redact tokens, passwords, PAN, national IDs at the source logger; restrict request-body logging.
7. **Non-production:** synthetic or masked data, never raw production copies.

## Gotchas
- Backups and data warehouses keep deleted data; retention must cover them.
- "We might need it later" is not a purpose.
- Free-text fields collect sensitive data you never asked for; scan them (DLP classifiers).

## Verify
- [ ] Field inventory reviewed with owners; unneeded fields scheduled for removal.
- [ ] Deletion job metrics show records purged on schedule.
- [ ] Log samples contain no secrets or full identifiers.
