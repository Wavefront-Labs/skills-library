---
id: computing-software.data-engineering.etl-pipeline-design.inferred-members-for-late-dimensions
name: inferred-members-for-late-dimensions
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, inferred-members, late-arriving-dimensions, surrogate-keys, dimensional-modelling]
level: advanced
status: docs-checked
description: "Load facts whose dimension rows have not arrived using inferred (placeholder) members, then overwrite them in place when the real dimension data lands."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/late-arriving-dimension/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Inferred members for late-arriving dimensions

**Goal:** never drop or delay facts because their customer/product row is not in the dimension yet, and still end with correct attributes.

## Pattern
1. While loading facts, look up the dimension by natural key.
2. If missing, **insert an inferred member**: new surrogate key, natural key, attributes set to placeholders (`'Unknown'`), `is_inferred = true`.
3. Fact rows get that surrogate key.
4. When the real dimension record arrives, **update the inferred row in place** (type 1 overwrite of all attributes, `is_inferred = false`), even for attributes that are SCD2 elsewhere. The first real version replaces the placeholder rather than creating a new version.

```sql
-- step 2 (before fact load)
insert into dim_customer (customer_sk, customer_id, name, segment, is_inferred, valid_from, valid_to)
select dim_customer_seq.nextval, s.customer_id, 'Unknown', 'Unknown', true, '1900-01-01', '9999-12-31'
from (select distinct customer_id from stg_orders) s
left join dim_customer d on d.customer_id = s.customer_id
where d.customer_id is null;

-- step 4 (dimension load)
merge into dim_customer d using stg_customers s on d.customer_id = s.customer_id and d.is_inferred
when matched then update set name = s.name, segment = s.segment, is_inferred = false;
```

## With hash/natural keys
If facts carry `customer_key = hash(customer_id)` and the dimension is built from the union of all known customer ids (from facts and source), the "inferred" row arises naturally with null attributes; coalesce to 'Unknown' and flag it. No in-place update needed because the dimension is rebuilt.

## Monitoring
Count of inferred members older than N days = source integration problem (customer never arrives). Alert on it.

## vs unknown member (-1)
A single `-1 Unknown` row loses the natural key; you cannot fix facts later without reloading. Inferred members keep the key, so they heal automatically.

## Related case: retroactive type 2 change
Kimball's late-arriving dimension technique also covers a retroactive change to a type 2 attribute: insert a new dimension row for the corrected period, then restate the associated fact rows. That is a different fix from the inferred-member overwrite above.

## Verify
Load a fact with a new customer id, then the customer: the fact's surrogate key is unchanged and now shows real attributes.

## Checked
Checked 2026-11-08 against the Kimball Group "Late Arriving Dimensions" technique page, read in full (a single paragraph). Confirmed: facts can arrive before dimension context; placeholder rows carry the unresolved natural key with generic unknown values; placeholders are later updated with type 1 overwrites; retroactive type 2 changes need a new row and restated facts. The SQL, hash-key variant, monitoring and -1 comparison are design advice, not documentation claims; the SQL was not run.
Method: documentation only; no commands were run.
