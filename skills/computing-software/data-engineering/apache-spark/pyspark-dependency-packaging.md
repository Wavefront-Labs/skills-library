---
id: computing-software.data-engineering.apache-spark.pyspark-dependency-packaging
name: pyspark-dependency-packaging
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, pyspark-dependency-management, venv-pack, conda-pack, pex, py-files, archives, python-environment]
level: practitioner
status: docs-checked
description: "Ship Python dependencies to PySpark executors with venv-pack/conda-pack archives, PEX or --py-files, and fix ModuleNotFoundError on workers."
sources:
  - https://spark.apache.org/docs/latest/submitting-applications.html
  - https://spark.apache.org/docs/latest/api/python/tutorial/python_packaging.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PySpark dependency packaging

**Goal:** the driver and every executor run the same Python with the same packages, reproducibly, without installing on cluster nodes by hand.

## Options
| Method | Notes |
|---|---|
| `--py-files` | Adds `.py`, `.zip` or `.egg` files to the search path; for your own package code |
| venv-pack / conda-pack archive via `--archives` (or `spark.archives`) | Ships third-party packages; unpacked automatically on executors |
| PEX file | Single-file environment; see the PySpark packaging tutorial |
| Docker image (k8s) | Bake deps into the image |
| Platform libs (Databricks cluster libraries, EMR bootstrap) | Platform-specific |

## venv-pack
```bash
python -m venv pyspark_venv && source pyspark_venv/bin/activate
pip install pyarrow pandas venv-pack
venv-pack -o pyspark_venv.tar.gz

export PYSPARK_DRIVER_PYTHON=python          # do not set in YARN/Kubernetes cluster modes
export PYSPARK_PYTHON=./environment/bin/python
spark-submit --archives pyspark_venv.tar.gz#environment app.py
```
venv-pack stores the Python interpreter as a symbolic link, so every node needs the same interpreter installed.

## conda-pack
```bash
conda create -y -n pyspark_env -c conda-forge pyarrow pandas conda-pack
conda activate pyspark_env && conda pack -f -o pyspark_env.tar.gz
spark-submit --archives pyspark_env.tar.gz#environment app.py
```

## PEX
```bash
pex pyspark pandas pyarrow -o app_env.pex
export PYSPARK_PYTHON=./app_env.pex
spark-submit --files app_env.pex app.py
```

## Your own code
Package it as a wheel and include it in the env, or zip it:
```bash
cd src && zip -r ../mycode.zip mypkg && spark-submit --py-files mycode.zip app.py
spark.sparkContext.addPyFile("s3a://artifacts/mycode.zip")   # at runtime
```

## Gotchas
- `SparkContext.addPyFile()` uploads code even after the job has started.
- Set `PYSPARK_DRIVER_PYTHON` only in client mode; it must be unset in YARN and Kubernetes cluster modes.

## Verify
- [ ] Fresh cluster runs the job without manual installs.

## Checked

2026-11-01. Confirmed against the Spark Python package management tutorial and submitting-applications page (`--py-files` file types, `--archives`/`spark.archives`, conda-pack, venv-pack symlink caveat, PEX section, `PYSPARK_PYTHON`/`PYSPARK_DRIVER_PYTHON` handling, `addPyFile`). Removed: native-wheel table claims, pinned versions, YARN appMasterEnv, worker/driver error text, `%pip`, archive-download and pyarrow notes.

Method: documentation only; no commands were run.
