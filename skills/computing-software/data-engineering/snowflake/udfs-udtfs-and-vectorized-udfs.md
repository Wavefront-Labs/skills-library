---
id: computing-software.data-engineering.snowflake.udfs-udtfs-and-vectorized-udfs
name: udfs-udtfs-and-vectorized-udfs
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-udf, udtf, vectorized-udf, python-udf, sql-udf, secure-udf, anaconda-packages, imports-stage, memoizable]
level: advanced
status: docs-checked
description: "Extend Snowflake SQL with functions: SQL vs Python UDFs, UDTFs that return rows, vectorized (batch pandas) Python UDFs, packages and imports, secure UDFs, and performance traps."
sources:
  - https://docs.snowflake.com/en/developer-guide/udf/udf-overview
  - https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-batch
  - https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-tabular-functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UDFs, UDTFs and vectorized UDFs

**Goal:** encapsulate logic SQL can't express cleanly, with the cheapest execution model that works.

## Prefer SQL UDFs for SQL logic
```sql
create or replace function util.fiscal_quarter(d date)
returns varchar
as $$ 'FY' || year(dateadd(month, 6, d)) || '-Q' || quarter(dateadd(month, 6, d)) $$;
```

## Python scalar UDF
```sql
create or replace function util.normalize_phone(p string)
returns string
language python runtime_version = '3.11'
packages = ('phonenumbers')
handler = 'normalize'
as $$
import phonenumbers
def normalize(p):
    if p is None: return None
    try: return phonenumbers.format_number(phonenumbers.parse(p, "AU"), phonenumbers.PhoneNumberFormat.E164)
    except Exception: return None
$$;
```
List available packages with `select * from information_schema.packages where language = 'python'`; other code can be added with `IMPORTS = ('<imports>')`.

## Vectorized (batch) Python UDF
```python
import pandas as pd
from _snowflake import vectorized
@vectorized(input=pd.DataFrame)
def score(df):                        # df columns are positional: df[0], df[1], ...
    return model.predict(df)          # model loaded at module level, once per process
```
Processes batches as pandas; `max_batch_size` (set on the decorator or as a function attribute) limits the rows per batch.

## UDTF: return rows
```python
class SplitItems:
    def process(self, payload: str):
        for item in json.loads(payload)["items"]:
            yield (item["sku"], item["qty"])
    def end_partition(self): pass
```
`select t.* from orders, table(util.split_items(orders.payload)) t;` or partitioned: `table(f(x) over (partition by key order by ts))` to process groups with state.

## Security and performance
- Network access from UDF code needs an external access integration.
- Load heavy resources at module level (once per process), not inside the handler.

## Verify
- [ ] Unit test the handler function in plain Python before deploying.
- [ ] Query profile shows the UDF's share of time; compare against a SQL/built-in alternative.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: vectorized decorator with pandas DataFrame input and positional columns, max_batch_size, UDTF end_partition, IMPORTS and PACKAGES parameters, INFORMATION_SCHEMA.PACKAGES query, external access integration for network (udf-overview, udf-python-batch, udf-python-tabular-functions pages).

Removed or corrected: optimizer-inlining, secure-function, memoizable/immutable and 'much faster' claims (not on the pages read).

Method: documentation only; no commands were run.
