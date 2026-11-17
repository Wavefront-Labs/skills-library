---
id: computing-software.data-engineering.polars.gpu-engine-cudf-polars
name: gpu-engine-cudf-polars
category: computing-software
field: data-engineering
product: polars
tags: [polars-gpu-engine, gpu, cudf-polars, rapids, nvidia, gpuengine, raise-on-fail, multi-gpu]
level: practitioner
status: docs-checked
description: "Run Polars lazy queries on NVIDIA GPUs with engine=gpu: requirements, install extras, GPUEngine for multi-GPU, CPU fallback detection and raise_on_fail."
sources:
  - https://docs.pola.rs/user-guide/gpu-support/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU engine (Open Beta)

GPU-accelerated execution for Python users of the Lazy API, via RAPIDS cuDF.

## Requirements
NVIDIA Volta or newer (compute capability 7.0+), CUDA 12 or 13, Linux or WSL2.

## Install
```bash
pip install polars[gpu]          # installs cudf-polars-cu12
pip install polars cudf-polars-cu13   # for CUDA 13
```
cudf-polars supports a bounded range of Polars versions; if Polars is not pinned the resolver may pick an older compatible release. Pin Polars if that is unacceptable (incompatible combinations then fail resolution).

## Use
Build a lazy query as normal, then:
```python
result = q.collect(engine="gpu")
```
Works with `.collect` and `.sink_*`. The result is a normal CPU-backed DataFrame. Eager API is not supported.

## Multi-GPU
Pass a `GPUEngine` object. As of cudf-polars 26.06 three subclasses exist: `RayEngine`, `DaskEngine`, `SPMDEngine`. Use as context managers to tear down resources:
```python
from cudf_polars.engine.ray import RayEngine
with RayEngine() as engine:
    result = q.collect(engine=engine)
```
Ray/Dask need the pip extras: `pip install cudf-polars-cu13[ray]` or `[dask]`.

## Fallback behaviour
Unsupported queries do not fail: the optimized plan is inspected and, if it cannot run on GPU, the standard CPU engine runs everything. To see why, enable verbose mode:
```python
with pl.Config() as cfg:
    cfg.set_verbose(True)
    result = q.collect(engine="gpu")
```
which issues a `PerformanceWarning` (e.g. `NotImplementedError: dtype=Binary conversion not supported`). To raise instead: `q.collect(engine=pl.GPUEngine(raise_on_fail=True))` (a `ComputeError`). Only the proximal cause is reported.

## Supported / not
Supported: LazyFrame and SQL API, CSV/Parquet/ndjson/in-memory I/O, numeric/logical/string/datetime types, grouped and rolling aggregations, joins, filters, missing data, concatenation. Not supported: eager API; Date, Categorical, Enum, Time, Array, Binary, Object dtypes; some Datetime-with-timezone and List expressions; resampling; folds; UDFs; Excel and database formats.

## When it helps
Grouped aggregations and joins; I/O-bound queries show similar CPU/GPU performance. Pass rates: 99.2% of Polars unit tests with fallback, 88.8% without.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
