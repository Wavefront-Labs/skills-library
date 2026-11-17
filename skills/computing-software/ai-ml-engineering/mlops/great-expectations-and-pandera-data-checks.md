---
id: computing-software.ai-ml-engineering.mlops.great-expectations-and-pandera-data-checks
name: great-expectations-and-pandera-data-checks
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, data-validation, great-expectations, pandera, schema-validation, data-contracts, data-quality]
level: practitioner
status: docs-checked
description: "Validate pipeline data with pandera schemas (lazy errors, check_types) and Great Expectations suites, validation definitions and checkpoints."
sources:
  - https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/dataframe_schemas.md
  - https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/checks.md
  - https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/lazy_validation.md
  - https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/decorators.md
  - https://raw.githubusercontent.com/great-expectations/great_expectations/develop/docs/docusaurus/docs/core/introduction/gx_overview.md
  - https://raw.githubusercontent.com/great-expectations/great_expectations/develop/docs/docusaurus/docs/core/introduction/try_gx_end_to_end.py
  - https://raw.githubusercontent.com/great-expectations/great_expectations/develop/docs/docusaurus/docs/core/define_expectations/create_an_expectation.md
  - https://raw.githubusercontent.com/great-expectations/great_expectations/develop/docs/docusaurus/docs/core/run_validations/run_validations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Great Expectations and pandera data checks

**Goal:** bad data fails loudly at pipeline boundaries instead of silently producing a bad model.

## pandera (code-first, lightweight)
```python
import pandera.pandas as pa
schema = pa.DataFrameSchema(
    {
        "customer_id": pa.Column(str, unique=True, nullable=False),
        "plan": pa.Column(str, pa.Check.isin(["free", "pro", "team"])),
        "monthly_spend": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "score": pa.Column(float, pa.Check(lambda s: s <= 10), nullable=True),
    },
    strict=True, coerce=True,
)
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as exc:
    print(exc.failure_cases)
    raise
```
- Columns accept `nullable=True` to allow nulls (otherwise nulls raise an error), `unique=True`, and `coerce=True` to cast to the declared dtype before validation. `strict=True` is used in the docs' schema example to reject unexpected columns.
- Checks: built-ins such as `Check.isin`, `Check.less_than`, `Check.greater_than_or_equal_to`, or `pa.Check(lambda s: ...)`; the function receives the whole Series by default (`element_wise=False`), `element_wise=True` runs it per element.
- `lazy=True` collects all failures; the raised `SchemaErrors` exposes `failure_cases`. Without lazy, validation stops at the first failure.
- Class syntax: `class MySchema(pa.DataFrameModel)` plus the `@pa.check_types` decorator validates function inputs and outputs annotated with `pandera.typing.DataFrame[...]`.

## Great Expectations (GX Core)
Workflow pattern from the GX overview: set up a Data Context; connect to data (Data Source, Data Asset, Batch Definition, Batch); define Expectations and Expectation Suites; run Validations. A Validation Definition ties a Batch Definition to an Expectation Suite; a Checkpoint runs a list of Validation Definitions with shared parameters and can run Actions (email, Slack/Teams, custom notifications); Data Docs are human-readable pages of suites and results.

From the docs' end-to-end example:
```python
import great_expectations as gx
context = gx.get_context()
data_source = context.data_sources.add_postgres("postgres db", connection_string=conn)
asset = data_source.add_table_asset(name="taxi data", table_name="nyc_taxi_data")
batch_definition = asset.add_batch_definition_whole_table("batch definition")
suite = context.suites.add(gx.core.expectation_suite.ExpectationSuite(name="expectations"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="fare_amount", min_value=0, severity="critical"))
vd = context.validation_definitions.add(gx.core.validation_definition.ValidationDefinition(
    name="validation definition", data=batch_definition, suite=suite))
checkpoint = context.checkpoints.add(gx.checkpoint.checkpoint.Checkpoint(
    name="checkpoint", validation_definitions=[vd]))
result = checkpoint.run()
print(result.describe())
```
- Expectations take a `severity` (the example uses `"warning"` and `"critical"`), and a `mostly` argument allows validation to pass when at least that fraction of rows pass.
- The same suite can be applied to different Batches, and several suites can cover one data set. The Expectation Gallery lists the available Expectations.
- For an `UnexpectedRowsExpectation` the failing rows are capped at 200; a doc page covers retrieving all of them.

## Where to run (design guidance, not from the docs)
At ingestion, before training, and against serving logs; fail on hard checks and only warn on soft statistical checks.

## Verify
- [ ] A deliberately corrupted batch fails validation with a readable report.
- [ ] Checks run in CI on sample data and in the pipeline on real data.

## Checked
Date: 2026-11-09.
- Confirmed in the pandera schemas, checks, lazy validation and decorators docs and in the GX overview, end-to-end example and Expectation docs: code patterns and parameters quoted above.
- Removed as unconfirmed: `Check.in_range`, `Check.ge`/`le` and quantile checks, polars and PySpark support claims, the `pandas_default.read_dataframe` and `batch.validate(suite)` flow, specific Expectation class names other than ExpectColumnValuesToBeBetween, the list of check categories (volume, freshness, distribution, label sanity), the claim that the GX API changed substantially between 0.x and 1.x, and the dead pandera and GX documentation-site URLs.
Method: documentation and example source files only; no commands were run.
