---
id: computing-software.ai-ml-engineering.scikit-learn.n-jobs-joblib-parallelism-and-oversubscription
name: n-jobs-joblib-parallelism-and-oversubscription
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, n-jobs, joblib-parallel, threadpoolctl, oversubscription, loky, parallel-config, performance]
level: practitioner
status: verified
description: "Control scikit-learn parallelism: n_jobs and joblib backends, nested parallelism, BLAS/OpenMP thread oversubscription with threadpoolctl, memmapping and containers."
sources:
  - https://scikit-learn.org/stable/computing/parallelism.html
  - https://joblib.readthedocs.io/en/stable/
  - https://github.com/joblib/threadpoolctl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# n_jobs, joblib backends and thread oversubscription

**Goal:** use all cores without making training slower through too many threads fighting over them.

## Two layers of parallelism
1. **joblib** (`n_jobs`): process- or thread-level parallelism over folds, trees, grid points. Default backend `loky` (processes).
2. **Native threads** inside NumPy/SciPy BLAS (OpenBLAS, MKL) and OpenMP code (`HistGradientBoosting`, `KMeans`): controlled by `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` or threadpoolctl.

Oversubscription = processes x threads >> cores. Symptom: 16-core box, `GridSearchCV(n_jobs=16)` over a model that also uses 16 BLAS threads -> 256 threads, slower than serial.

joblib's loky workers already limit native threads to `cpu_count // n_jobs` per worker, which helps (measured on a 12-core machine: parent OpenBLAS 12 threads, workers with `n_jobs=4` 3 threads, `n_jobs=2` 6 threads); it does not help with your own nested choices.

## Rules
- Parallelise at **one level**: the outermost (search over folds/params) is usually best. Set inner `n_jobs=1`:
```python
GridSearchCV(RandomForestClassifier(n_jobs=1), grid, n_jobs=-1)
```
- For a single big model fit, give the model the cores instead (`RandomForestClassifier(n_jobs=-1)`, HGB uses OpenMP automatically).
- Limit native threads explicitly where needed:
```python
from threadpoolctl import threadpool_limits
with threadpool_limits(limits=1, user_api="blas"):
    search.fit(X, y)
```

## Backends and config
```python
from joblib import parallel_config        # joblib >= 1.3
with parallel_config(backend="threading", n_jobs=8):   # for code that releases the GIL
    model.fit(X, y)
```
- `loky` (default): processes; data is pickled to workers - large arrays over `max_nbytes` (default 1M) are memory-mapped from a temp folder instead (`JOBLIB_TEMP_FOLDER` chooses the folder; if unset joblib tries `/dev/shm` first on Linux, so check its size in containers; default `max_nbytes='1M'` confirmed in the `Parallel` signature).
- `threading`: no copying, but only useful if the work releases the GIL.
- The `dask` backend (`parallel_config(backend="dask")`, registered by joblib 1.6.0) distributes work through a dask.distributed client. Third-party backends such as Ray register themselves; see their docs.

## Containers and shared machines
- `n_jobs=-1` means "all CPUs joblib can see". `joblib.cpu_count()` delegates to loky, which takes Linux CFS quotas and CPU affinity into account (joblib docstring), but native libraries may still see host cores; set `OMP_NUM_THREADS` to the container's CPU limit.
- Each loky worker holds a copy of non-memmapped data: memory = n_jobs x dataset size in the worst case. Reduce `n_jobs` if you hit OOM.

## Verify
- [ ] Wall time measured for at least two n_jobs/thread configurations.
- [ ] No nested `n_jobs=-1`.
- [ ] Container memory headroom checked with the chosen n_jobs.
