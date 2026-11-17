---
id: computing-software.data-engineering.polars.polars-install-python-extras
name: polars-install-python-extras
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-installation, pip, optional-dependencies, big-index, legacy-cpu, python-install, extras]
level: practitioner
status: docs-checked
description: "Install Polars for Python with pip, pick optional extras (numpy, pyarrow, excel, database, cloud), and handle legacy CPUs or datasets over 2^32 rows."
sources:
  - https://docs.pola.rs/user-guide/installation/
  - https://docs.pola.rs/user-guide/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Polars for Python and choose extras

Goal: get a working `import polars as pl` with only the optional dependencies you need.

## Base install and import

```bash
pip install polars
```

```python
import polars as pl
```

Polars is a library; installation is just the language's package manager. The base install is the core only; extras are optional to keep the footprint small.

## Variants

- Legacy CPUs without AVX2 support: `pip install polars[rtcompat]`. The Legacy CPU section words it as "an old CPU without AVX support" and uses the same `rtcompat` extra.
- Big index: by default dataframes are limited to 2^32 rows (about 4.3 billion). Enable 2^64 with `pip install polars[rt64]`.

## Optional extras (pip tags)

Combine them in quotes: `pip install 'polars[numpy,fsspec]'`.

| Group | Tags |
| --- | --- |
| All | `all` installs every optional dependency |
| GPU | `gpu` runs queries on NVIDIA GPUs (see the GPU support page for prerequisites) |
| Interop | `pandas`, `numpy`, `pyarrow`, `pydantic` |
| Excel | `calamine`, `openpyxl`, `xlsx2csv` (read), `xlsxwriter` (write), `excel` (all engines) |
| Database | `adbc`, `connectorx` (read), `sqlalchemy` (write), `database` (all engines) |
| Cloud | `fsspec` for remote file systems |
| Other I/O | `deltalake` (read/write Delta), `iceberg` (read Iceberg) |
| Other | `async` (collect LazyFrames asynchronously), `cloudpickle` (serialize user-defined functions), `graph` (visualize LazyFrames), `plot`, `style`, `timezone` |

## Gotchas

- `timezone` is only needed on Windows.
- The user guide says it mentions when a feature needs an additional dependency, so an import error on a feature usually means a missing extra.
- Getting started shows a quick smoke test: write a dataframe with `df.write_csv(path)` and read it back with `pl.read_csv(path, try_parse_dates=True)`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/installation/; https://docs.pola.rs/user-guide/getting-started/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
