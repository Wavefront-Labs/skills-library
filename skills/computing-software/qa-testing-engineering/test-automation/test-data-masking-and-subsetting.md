---
id: computing-software.qa-testing-engineering.test-automation.test-data-masking-and-subsetting
name: test-data-masking-and-subsetting
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [data-masking, data-subsetting, test-data-management, anonymization, pseudonymization, gdpr, test-data-privacy]
level: practitioner
status: docs-checked
description: "Make production-derived test data safe: subset with referential integrity, mask or pseudonymise PII, and verify nothing sensitive leaks."
sources:
  - https://www.postgresql.org/docs/current/sql-copy.html
  - https://postgresql-anonymizer.readthedocs.io/en/stable/
  - https://gdpr-info.eu/art-4-gdpr/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Masking and subsetting production data

**Goal:** representative data for testing without exposing personal or secret data. Get data-protection sign-off before any production copy.

## Subsetting
- Pick driving rows (for example a small share of customers, or customers matching test scenarios), then follow foreign keys to pull every dependent row so constraints hold.
- In PostgreSQL, `COPY (query) TO ...` exports the result of a `SELECT` (parentheses required around the query), so a subset query can be exported directly; plain `COPY table TO` exports a whole table.
- Include lookup/reference tables in full.

## Masking techniques
| Technique | Use for | Note |
|---|---|---|
| Substitution (fake value) | names, addresses | realistic, not reversible |
| Deterministic pseudonymisation (keyed) | ids, emails used as join keys | same input -> same output across tables |
| Shuffling | values whose distribution matters | breaks row linkage |
| Nulling/redaction | free text, notes | free text often hides PII |
| Date shifting | DOB, events | shift per entity to keep intervals |

GDPR Article 4 defines pseudonymisation as processing personal data so it can no longer be attributed to a specific person without additional information, provided that information is kept separately and protected by technical and organisational measures. Keep any mapping or key out of the test environment.

## PostgreSQL Anonymizer
The extension masks PII or commercially sensitive data using declarative rules written in SQL `SECURITY LABEL`s, and its masking functions include randomization, faking, partial scrambling, shuffling, noise, generalization or your own custom function. It documents six methods: anonymous dumps, static masking, dynamic masking, replica masking, masking views and masking data wrappers. Its quick start (dynamic masking):
```sql
CREATE EXTENSION anon;
ALTER DATABASE demo SET anon.transparent_dynamic_masking TO true;
CREATE ROLE skynet LOGIN;
SECURITY LABEL FOR anon ON ROLE skynet IS 'MASKED';
GRANT pg_read_all_data to skynet;
SECURITY LABEL FOR anon ON COLUMN people.lastname
  IS 'MASKED WITH FUNCTION anon.dummy_last_name()';
SECURITY LABEL FOR anon ON COLUMN people.phone
  IS 'MASKED WITH FUNCTION anon.partial(phone,2,$$******$$,2)';
```
The masked role then sees a replaced last name and a phone like `06******11`. The extension also offers detection functions that guess which columns need anonymizing. For test environments pick a method that removes the data from the copy (dump, static or replica masking) rather than only hiding it from one role; see the extension docs for the exact functions of each method.

## Process
1. Classify columns (PII, sensitive, secret, safe); keep the classification in the repo.
2. Mask in a secure zone; only masked output reaches test environments.
3. Fail the pipeline when an unclassified new column appears.

## Gotchas
- Free-text, JSON blobs, logs and file attachments carry PII that column rules miss.
- Small subsets can still re-identify people (rare combinations).
- Secrets (API keys, password hashes, tokens) must be replaced, not masked.

## Verify
Scan masked output for PII patterns (emails, phone numbers, real domains), check FK integrity, and confirm the classification covers every column.

## Checked
2026-11-09. Confirmed in the PostgreSQL COPY page (COPY (query) TO, parentheses required), the PostgreSQL Anonymizer home and quick start page (declarative security labels, six methods, masking function families, dummy_last_name, partial, transparent dynamic masking, detection functions) and GDPR Article 4 (pseudonymisation definition). Removed: Jailer/Tonic tools, information_schema FK query, anon.fake_email / anonymize_database example (not on the fetched pages), format-preserving row, the claim that pseudonymised data is personal data (Article 4 alone does not state it).
Method: documentation only; no commands were run.
