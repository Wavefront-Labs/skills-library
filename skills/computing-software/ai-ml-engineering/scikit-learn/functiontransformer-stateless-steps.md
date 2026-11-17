---
id: computing-software.ai-ml-engineering.scikit-learn.functiontransformer-stateless-steps
name: functiontransformer-stateless-steps
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, functiontransformer, custom-transformer, log-transform, pipeline, feature-names-out]
level: practitioner
status: verified
description: "Wrap stateless transformations in FunctionTransformer: log1p, column math, inverse_func, validate, feature_names_out and keeping it picklable."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html
  - https://scikit-learn.org/stable/modules/preprocessing.html#custom-transformers
  - https://scikit-learn.org/stable/auto_examples/preprocessing/plot_target_encoder.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FunctionTransformer for stateless steps

**Use for:** transformations that learn nothing from data (log, clipping to fixed bounds, ratios, date part extraction). Anything that learns statistics (means, quantiles, vocabularies) must be a proper transformer with `fit`.

## Examples
```python
import numpy as np, pandas as pd
from sklearn.preprocessing import FunctionTransformer

log1p = FunctionTransformer(np.log1p, inverse_func=np.expm1, feature_names_out="one-to-one")

def add_ratios(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["debt_to_income"] = df["debt"] / df["income"].clip(lower=1)
    return out

ratios = FunctionTransformer(add_ratios, feature_names_out=lambda tr, names: [*names, "debt_to_income"])

def date_parts(df):
    d = pd.to_datetime(df.iloc[:, 0])
    return pd.DataFrame({"dow": d.dt.dayofweek, "month": d.dt.month, "hour": d.dt.hour})
dates = FunctionTransformer(date_parts, feature_names_out=lambda tr, names: ["dow", "month", "hour"])
```

## Parameters
- `func` / `inverse_func`: callables; `kw_args` / `inv_kw_args` pass fixed keyword arguments (tunable as `functiontransformer__kw_args`).
- `validate=False` (default) passes DataFrames through untouched; `True` converts to a 2D array and checks it.
- `check_inverse=True` (default) emits a `UserWarning` ("not strictly inverse of each other", tested) if `inverse_func(func(X))` does not round-trip on a sample.
- `feature_names_out`: `"one-to-one"` or a callable `(transformer, input_names) -> names`; required for `get_feature_names_out` and `set_output(transform="pandas")` to work.

## Pickling
Lambdas and closures do not pickle: both `pickle.dumps` and `joblib.dump` of a pipeline holding `FunctionTransformer(lambda x: x*2)` raised `PicklingError` (tested). Define functions at module level in an importable package so the saved pipeline loads in the serving environment.

## Pitfalls
- A function that computes statistics from its input (e.g. `x / x.max()`) uses the **test batch's** max at predict time: leakage and train/serve skew. Use a fitted scaler.
- `np.log` on zeros/negatives gives -inf/NaN; use `log1p` or clip.

## Verify
- [ ] `pipe.set_output(transform="pandas").fit_transform(X_train).columns` shows expected names.
- [ ] Pipeline round-trips through `joblib.dump`/`load` in a fresh process.
