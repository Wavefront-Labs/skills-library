---
id: computing-software.ai-ml-engineering.scikit-learn.global-config-set-config-and-config-context
name: global-config-set-config-and-config-context
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, sklearn-config-context, set-config, transform-output, assume-finite, working-memory, display]
level: practitioner
status: gated
description: "Control scikit-learn globally with set_config and config_context: pandas/polars output, assume_finite, working_memory, display, metadata routing and thread-safety."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.set_config.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.config_context.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.get_config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global options with set_config / config_context

```python
import sklearn
sklearn.get_config()                                  # current settings
sklearn.set_config(transform_output="pandas")         # process-wide
with sklearn.config_context(assume_finite=True):      # scoped; restored on exit
    model.predict(X_big)
```

## Options worth knowing
| Option | Effect | Use |
|---|---|---|
| `transform_output="pandas"` / `"polars"` / `"default"` | transformers return DataFrames with feature names | debugging, feature names downstream; per-estimator `set_output(transform=...)` overrides |
| `assume_finite=True` | skip NaN/inf validation | small speedup on large inputs you have already validated; dangerous otherwise |
| `working_memory=` (MiB, default 1024) | chunk size for pairwise distance computations | lower to avoid memory spikes in `pairwise_distances_chunked`, KNN, silhouette |
| `display="text"` / `"diagram"` | estimator repr in notebooks | text for logs |
| `print_changed_only=True` | repr shows only non-default params | default; keep |
| `enable_metadata_routing=True` | route `sample_weight`, `groups` etc. to sub-estimators explicitly | required for advanced routing APIs |
| `array_api_dispatch=True` | accept Array API (torch/CuPy) inputs | GPU computation for supported estimators |
| `skip_parameter_validation=True` | skip constructor param validation | micro-optimisation for many tiny fits |
| `pairwise_dist_chunk_size` | internal chunking for pairwise reductions | rarely needed |
| `enable_cython_pairwise_dist`, `sparse_interface` | other keys returned by `get_config()` in 1.9.1 | check `get_config()` for your version |

## Scope and threads
- `config_context` is thread-local: settings apply in the thread that set them. A bare `threading.Thread` saw the default `assume_finite=False` inside a `config_context(assume_finite=True)` (tested). To propagate the config to joblib workers use `sklearn.utils.parallel.Parallel` together with `sklearn.utils.parallel.delayed`; `joblib.Parallel` with sklearn's `delayed` warns and the workers saw the defaults (tested).
- Libraries and notebooks: prefer `config_context` over `set_config` so you do not change behaviour for other code in the process.

## Environment variables
- `SKLEARN_ASSUME_FINITE`, `SKLEARN_WORKING_MEMORY` set defaults at import.
- `SKLEARN_SEED` affects only the scikit-learn test suite, not estimators: set `random_state` explicitly (gated: unconfirmed, source is paywalled or blocked).
- `SKLEARN_ASSUME_FINITE=1` and `SKLEARN_WORKING_MEMORY=64` were picked up by a fresh process (tested).

## Gotchas
- `transform_output="pandas"` fails with sparse `OneHotEncoder` output ("Pandas output does not support sparse data. Set sparse_output=False", tested); set `sparse_output=False` or keep default output for that step. `TfidfVectorizer.fit_transform` still returned a SciPy CSR matrix under the pandas setting (tested), so it is not converted.
- A global setting changed in one test leaks into others; reset with `set_config(**defaults)` in fixtures or use contexts.
