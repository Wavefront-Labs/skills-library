---
id: computing-software.data-engineering.data-quality.dataframe-validation-with-pandera
name: dataframe-validation-with-pandera
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-testing, pandera, pydantic, dataframe-validation, schema-validation, polars, pyspark, python-pipelines]
level: practitioner
status: verified
description: "Validate DataFrames in Python pipelines with pandera (pandas, polars, PySpark) and records with pydantic: schema models, checks, coercion, lazy error reports and type-checked functions."
sources:
  - https://pandera.readthedocs.io/en/stable/
  - https://pandera.readthedocs.io/en/stable/dataframe_models.html
  - https://pandera.readthedocs.io/en/stable/lazy_validation.html
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DataFrame validation with pandera (and pydantic)

**Goal:** Python transformations fail fast with a readable report when input or output data violates expectations, using schemas that double as documentation.

## 1. Define a schema model
```python
import pandera.pandas as pa            # older versions: import pandera as pa
from pandera.typing import Series

class Orders(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(unique=True, ge=1)
    customer_id: Series[int] = pa.Field(nullable=False)
    amount: Series[float] = pa.Field(ge=0, le=1_000_000)
    currency: Series[str] = pa.Field(isin=["EUR", "USD", "GBP"])
    created_at: Series[pa.DateTime] = pa.Field(nullable=False)
    shipped_at: Series[pa.DateTime] = pa.Field(nullable=True)

    @pa.dataframe_check
    def shipped_after_created(cls, df):          # cross-column rule
        return df["shipped_at"].isna() | (df["shipped_at"] >= df["created_at"])

    class Config:
        strict = "filter"     # drop unexpected columns (True = error on them)
        coerce = True         # cast to declared types before checks
```

## 2. Validate
```python
validated = Orders.validate(raw_df, lazy=True)   # lazy: collect ALL failures, not just the first
```
```python
from pandera.errors import SchemaErrors
try:
    Orders.validate(raw_df, lazy=True)
except SchemaErrors as e:
    report = e.failure_cases          # DataFrame: schema_context, column, check, check_number, failure_case, index (pandera 0.34, pandas)
    report.to_csv("orders_failures.csv", index=False)
    raise
```
Quarantine pattern: split invalid rows using `failure_cases["index"]`, write them to a quarantine table, continue with valid rows only if the error rate is below a threshold.

## 3. Type-checked functions
```python
from pandera.typing import DataFrame
@pa.check_types
def enrich(orders: DataFrame[Orders]) -> DataFrame[EnrichedOrders]:
    ...
```
Inputs and outputs are validated on every call — good at module boundaries, expensive in tight loops (set `PANDERA_VALIDATION_ENABLED=False` to disable in hot paths only if you validate elsewhere).

## 4. Other backends
- Polars: `import pandera.polars as pa` with `pl.DataFrame`/`LazyFrame` (lazy frames validate schema-level checks without collecting).
- PySpark: `import pandera.pyspark as pa` — returns the DataFrame with an `errors` attribute instead of raising; check `df.pandera.errors`.
- Statistical hypothesis checks and custom checks (`pa.Check(lambda s: s.str.len() < 255)`).
- Generate schemas from data as a starting point: `pa.infer_schema(df).to_script()` — then tighten by hand. `to_script()` needs `black` installed (ImportError otherwise; pandera's `io` extra).
- Polars `LazyFrame`: with the default settings `Model.validate(lf)` returns a LazyFrame and a data-level check such as `ge=1` is NOT run (tested: a 0 passed); validate a collected `DataFrame` to run value checks.

## 5. Row-level records: pydantic
For API payloads and event messages (dicts, not DataFrames):
```python
from pydantic import BaseModel, Field, ValidationError
class OrderEvent(BaseModel):
    order_id: int = Field(ge=1)
    currency: str = Field(pattern="^[A-Z]{3}$")
    amount: float = Field(ge=0)
good, bad = [], []
for rec in records:
    try: good.append(OrderEvent.model_validate(rec))
    except ValidationError as e: bad.append({"record": rec, "errors": e.errors()})
```

## Verify
- [ ] Schema models are unit-tested with one valid and one invalid fixture each.
- [ ] Validation runs with `lazy=True` and failure cases are persisted.
- [ ] Pipeline behaviour on failure (abort vs quarantine) is explicit per dataset.
