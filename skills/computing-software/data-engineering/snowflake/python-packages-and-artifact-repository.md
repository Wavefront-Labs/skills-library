---
id: computing-software.data-engineering.snowflake.python-packages-and-artifact-repository
name: python-packages-and-artifact-repository
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowpark, snowflake-packages, anaconda-channel, artifact-repository, pypi, imports, stage-imports, udf-dependencies]
level: practitioner
status: docs-checked
description: "Manage Python dependencies for Snowpark UDFs and procedures: Anaconda channel, PyPI via artifact repository, stage imports, default source, pinning."
sources:
  - https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages
  - https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udfs
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Python packages for Snowpark

**Goal:** UDFs/procedures get the libraries they need, reproducibly, with the fewest surprises at deploy time.

## Two package sources
Python UDFs and procedures take packages from the Snowflake Anaconda channel (`snowflake.snowpark.anaconda_shared_repository`) or from PyPI through an artifact repository (`snowflake.snowpark.pypi_shared_repository`), or from a customer-hosted artifact repository. Without an `ARTIFACT_REPOSITORY` clause, Snowflake uses the `DEFAULT_PYTHON_ARTIFACT_REPOSITORY` parameter set at schema, database or account level. Set or unset it with `ALTER ACCOUNT | DATABASE | SCHEMA ... SET|UNSET DEFAULT_PYTHON_ARTIFACT_REPOSITORY`.

## 1. Anaconda channel
```sql
select * from information_schema.packages where language = 'python' and package_name = 'numpy';
```
```sql
create or replace function ml.score(x float)
returns float language python runtime_version = '3.12'
packages = ('scikit-learn', 'joblib')
handler = 'score'
as $$
def score(x): return float(x)
$$;
```
- Specify only the top-level packages your code uses; Anaconda resolves dependencies. Without a version it installs the latest; the docs say pinning is generally not necessary for Anaconda packages.
- Version resolution happens once at `CREATE FUNCTION` and is then frozen for that function.
- No separate Anaconda terms apply for in-Snowflake use; local use of the Snowflake conda channel is limited to developing and testing workloads for Snowflake. Other Anaconda channels (conda-forge, defaults) are not permitted under this licence.
- Packages install on demand on a cold warehouse and the cache is dropped on suspend; the first call after resume can be slower (the docs say about 30 seconds).
- `desc function f(<arg types>)` lists the packages a Python UDF uses.

## 2. PyPI via artifact repository
```sql
create or replace function sklearn_udf() returns float language python runtime_version = 3.12
artifact_repository = snowflake.snowpark.pypi_shared_repository
packages = ('scikit-learn==1.5')
handler = 'udf'
as $$
def udf(): return 1.0
$$;
```
- The `SNOWFLAKE.PYPI_REPOSITORY_USER` database role is granted to PUBLIC by default; if revoked, ACCOUNTADMIN must grant it again to the role that creates and the roles that run the function.
- Pin or bound versions for production (`pandas<3.0.0` or exact): PyPI packages are not curated and may break on new releases.
- Packages built only for x86: use a Snowpark-optimized warehouse with an x86 resource constraint and `RESOURCE_CONSTRAINT=(architecture='x86')` on the function.
- Limitations: private repositories are not supported; not usable in anonymous stored procedures; not directly usable in legacy notebooks (call a UDF or procedure instead). Snowflake does not vet external packages; Snowflake may block packages without notice.
- If package install fails at creation, test the specification locally with `pip install <package> --only-binary=:all:` for the target Python version and platform.
- List functions by source: `select ... artifact_repository from information_schema.functions where artifact_repository is not null`.

## 3. Stage imports (your own code, native code)
Only pure-Python packages or packages with native code can be uploaded through a stage. `imports = ('@mystage/mycustompackage.zip')` then `import mycustompackage`. For native code, add `RESOURCE_CONSTRAINT=(architecture='x86')` and a Snowpark-optimized x86 warehouse.

## Snowpark Python client side
```python
session.add_packages("numpy", "pandas", "xgboost==1.5.0")
session.add_requirements("mydir/requirements.txt")
session.add_import("/<path>/my_module.py")   # uploads to an internal stage and imports it
```

## Governance
Packages policies can allowlist or blocklist Anaconda and PyPI packages at account level.

## Gotchas
- UDFs run in a restricted engine: network access and file writes are disabled, so libraries that download corpora or models on demand (NLTK, Keras, spaCy) fail. Download locally and supply the data through a stage.
- Scikit-learn and TensorFlow can be slow for single-row prediction; use vectorized UDFs for batches.
- XGBoost inside a UDF: set concurrency to 1 (`nthread` 1 / `n_jobs=1`). Keras: use `predict_on_batch`, not `predict`.

## Verify
- [ ] `describe function` shows the expected packages.
- [ ] PyPI-sourced functions have version bounds.
- [ ] CI recreates functions from code with the same specifications.

## Checked
2026-11-09. Confirmed on "Using third-party packages" and the Snowpark "Creating UDFs" page: sources and default parameter, role grant default, pinning guidance, x86 constraint, limitations, licensing statements, cold-warehouse cache and 30-second note, DESCRIBE FUNCTION, packages policies, known issues, add_packages/add_requirements/add_import. Corrected the original: the PyPI role is granted to PUBLIC by default and no per-org Anaconda terms acceptance applies. Removed: the sample ML function with stage-loaded model, the custom_package_usage_config option, the external access integration and /tmp caching advice, and the runtime deprecation remark, which the pages do not state.
Method: documentation only; no commands were run.
