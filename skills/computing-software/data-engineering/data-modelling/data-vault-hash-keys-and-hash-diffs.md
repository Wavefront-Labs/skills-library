---
id: computing-software.data-engineering.data-modelling.data-vault-hash-keys-and-hash-diffs
name: data-vault-hash-keys-and-hash-diffs
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, data-vault, hash-diff, hash-keys, md5, sha1, business-key-normalisation, satellite-loading]
level: advanced
status: gated
description: "Compute Data Vault 2.0 hash keys and hash diffs consistently: business key normalisation, delimiters and null handling, algorithm choice, and change detection in satellites."
sources:
  - https://datavaultalliance.com/news/dv/understanding-data-vault-2-0/
  - https://automate-dv.readthedocs.io/en/latest/best_practises/hashing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Vault hash keys and hash diffs

**Goal:** the same business key produces the same hash on every platform and load, and satellites insert a row only when attributes really changed.

## Hash keys (hubs and links)
Standardise before hashing, always in the same order:
1. Cast to string.
2. Trim whitespace; upper-case (for case-insensitive keys).
3. Replace null/empty with a fixed token (e.g. `-1` or `^^`). This is not optional: `concat_ws` silently skips NULL arguments (DuckDB: `concat_ws('||','A',NULL,'C')` = `A||C`), so un-coalesced NULLs make different rows hash alike.
4. Concatenate multiple key parts with a delimiter that cannot appear in data (`||`).
5. Hash (MD5 or SHA-1/SHA-256) and store as BINARY (or fixed-length hex) consistently.

```sql
-- hub_customer hash key (md5 returns hex VARCHAR in DuckDB; unhex() gives the 16-byte BLOB; md5('A||B') matched Python hashlib)
md5(upper(trim(coalesce(cast(customer_id as varchar), '^^')))) as hk_customer
-- link_customer_order: parent keys in a fixed documented order
md5(concat_ws('||',
  upper(trim(coalesce(cast(customer_id as varchar), '^^'))),
  upper(trim(coalesce(cast(order_id as varchar), '^^'))))) as hk_customer_order
```
Multi-source hubs: include a business key collision code (BKCC) when the same key value means different entities in different systems (`'SAP' || '||' || customer_id`).

## Hash diff (satellites)
Hash of all descriptive attributes of the satellite, in a fixed column order:
```sql
md5(concat_ws('||',
  coalesce(upper(trim(name)), '^^'),
  coalesce(upper(trim(email)), '^^'),
  coalesce(cast(segment as varchar), '^^'))) as hd_customer_details
```
Load rule (ran on DuckDB: second identical load inserted 0 rows, a changed hash diff inserted 1): insert a satellite row when the latest row for that hash key has a different hash diff (or none exists):
```sql
insert into sat_customer_details
select s.* from stg s
left join (select hk_customer, hd_customer_details from sat_customer_details
           qualify row_number() over (partition by hk_customer order by load_dts desc) = 1) cur
  on cur.hk_customer = s.hk_customer
where cur.hk_customer is null or cur.hd_customer_details <> s.hd_customer_details;
```

## Choices and pitfalls
- **Algorithm:** MD5 is fine for keys (collision risk negligible at warehouse scales, not a security use). SHA-1/256 if policy requires. Never mix within one vault.
- **Case for hash diff:** upper-casing attributes in the diff means case-only changes are ignored; decide deliberately.
- **Column additions:** adding a column to the hash diff changes every hash -> every key looks changed on the next load and gets a new satellite row. Options: put new attributes in a new satellite (cleanest), or append the column last and strip trailing null placeholders before hashing so rows where it is null keep their old hash.
- **Types:** dates/timestamps/decimals must be formatted identically everywhere (`to_char(ts, 'YYYY-MM-DD HH24:MI:SS.FF6')`), or different platforms produce different hashes.
- Store hashes as BINARY(16) for MD5 to halve storage vs hex strings.

## Tooling
automate_dv macros (`hash_columns` with `is_hashdiff: true`) implement these standards; its docs list `concat_string` (default `||`) and `null_placeholder_string` (default `^^`) as the settings to configure once in `dbt_project.yml` vars. The `hash: MD5` var and the datavault4dbt macro names were not re-checked (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Same key hashed in two systems/platforms yields identical value (test vectors in CI).
- [ ] Re-running a load with unchanged source inserts zero satellite rows.
