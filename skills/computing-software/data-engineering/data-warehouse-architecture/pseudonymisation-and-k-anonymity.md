---
id: computing-software.data-engineering.data-warehouse-architecture.pseudonymisation-and-k-anonymity
name: pseudonymisation-and-k-anonymity
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, pii, pseudonymization, k-anonymity, keyed-hashing, generalisation, anonymisation, gdpr]
level: advanced
status: verified
description: "Pseudonymise and anonymise datasets for analytics and sharing: keyed hashing vs tokenisation, generalisation and suppression for k-anonymity, re-identification risks."
sources:
  - https://gdpr-info.eu/recitals/no-26/
  - https://www.johndcook.com/blog/2018/12/07/simulating-zipcode-sex-birthdate/
  - https://docs.python.org/3/library/hmac.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pseudonymisation and k-anonymity

**Goal:** analysts and partners get data that is useful for joins and statistics while direct identifiers are removed and re-identification risk is controlled.

## Terms (GDPR sense)
- **Pseudonymised:** identifiers replaced, but re-identification possible with additional information (key, mapping table). Still personal data (GDPR Recital 26); reduces risk.
- **Anonymised:** individuals not identifiable by any reasonably likely means. Outside GDPR scope, but a high bar; direct identifier removal alone is never enough.

## Pseudonymisation techniques
| Technique | Joinable | Reversible | Notes |
|---|---|---|---|
| Plain hash (sha256(email)) | yes | effectively yes (dictionary attack on emails/phones) | do not use alone |
| **Keyed hash (HMAC-SHA256 with secret key)** | yes (same key) | no without key | rotate key per sharing context to prevent cross-dataset linkage |
| Tokenisation (vault mapping) | yes | yes for authorised service | central detokenisation, audit |
| Format-preserving encryption | yes | yes with key | keeps formats for legacy systems |
| Random per-record ids | no | no | for one-off releases |

```python
import hmac, hashlib
def pseudonym(value: str, key: bytes) -> str:          # key from a secrets manager, never in code
    norm = value.strip().lower()
    return hmac.new(key, norm.encode(), hashlib.sha256).hexdigest()
```
In SQL-only pipelines, wrap the same logic in a secure UDF that reads the key from the platform's secret store (check your platform's current rules for UDF access to secrets) so analysts cannot see the key. The Python function above was run: it returns a 64-hex-character digest, `" A@B.com "` and `"a@b.com"` give the same value, and a different key gives a different value.
Normalise before hashing (lowercase, trim, E.164 phones) so the same person maps to the same pseudonym.

## Quasi-identifiers and k-anonymity
Quasi-identifiers (QIs): attributes that together identify people (postcode, birth date, gender, job title). Classic result: Sweeney's estimate is that ZIP + birth date + sex uniquely identifies about 87% of the US population (a later simulation by another author got about 84-85%).
**k-anonymity:** every combination of QI values appears for at least k records.
```sql
select postcode_3, birth_year, gender, count(*) as n
from release_candidate group by 1,2,3 having count(*) < 5;    -- equivalence classes violating k=5 (run in DuckDB: it returns each class with fewer than 5 rows, and an empty result means k=5 holds)
```
Techniques: **generalise** (full postcode -> district, birth date -> birth year/5-year band, exact age -> range), **suppress** (drop rare rows or cells), top/bottom-code outliers (income > 250k -> "250k+").
Limits: k-anonymity does not protect against homogeneity (all k share the same diagnosis) -> l-diversity / t-closeness; and fails against linkage with external data. For aggregates/statistics releases, consider differential privacy.

## Process
1. Classify columns: direct identifiers, QIs, sensitive attributes, others.
2. Remove/pseudonymise direct identifiers; generalise QIs until k (e.g. 5-10) holds; check sensitive attribute diversity.
3. Assess residual risk (motivated intruder test), document in a DPIA; legal sign-off for "anonymous" claims.
4. Control access to keys/mapping tables separately from pseudonymised data.

## Verify
- [ ] No direct identifiers in the release; violating equivalence classes query returns zero rows at chosen k.
- [ ] Hash key stored in a secrets manager; different keys per external recipient.
