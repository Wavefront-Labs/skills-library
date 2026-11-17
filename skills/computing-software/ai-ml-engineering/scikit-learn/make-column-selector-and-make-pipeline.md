---
id: computing-software.ai-ml-engineering.scikit-learn.make-column-selector-and-make-pipeline
name: make-column-selector-and-make-pipeline
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, make-column-selector, make-column-transformer, make-pipeline, columntransformer, pipeline]
level: practitioner
status: verified
description: "Build preprocessing with make_pipeline, make_column_transformer and make_column_selector (dtype/regex selection), remainder handling and auto-generated step names."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_selector.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_transformer.html
  - https://scikit-learn.org/stable/modules/compose.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# make_pipeline, make_column_transformer and make_column_selector

**Goal:** declare column-wise preprocessing that adapts to the DataFrame's dtypes instead of hard-coded column lists.

## Pattern
```python
from sklearn.compose import make_column_transformer, make_column_selector as selector
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier

num = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
cat = make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=20))
pre = make_column_transformer(
    (num, selector(dtype_include="number")),
    (cat, selector(dtype_include=["object", "category"])),
    ("drop", selector(pattern=r"^id_|_raw$")),   # WARNING: see Overlap below, this does not remove numeric id_/_raw columns
    remainder="drop", verbose_feature_names_out=False)
clf = make_pipeline(pre, HistGradientBoostingClassifier())
```

## Selector options
- `dtype_include` / `dtype_exclude`: numpy/pandas dtypes or strings (`"number"`, `"category"`, `"bool"`, `"datetime"`).
- `pattern`: regex on column names (combined with dtype filters via AND).
- Selection happens at `fit` time and the chosen columns are stored; at `transform` the same names are required.

## Step names
`make_pipeline`/`make_column_transformer` name steps after lowercased class names (`standardscaler`, `pipeline-1`, `pipeline-2`). Inspect with `clf.get_params().keys()` before writing a grid; use explicit `Pipeline([...])` / `ColumnTransformer([...])` when you want stable readable names for tuning and logging.

## remainder
`remainder="drop"` (default) silently discards unlisted columns; `"passthrough"` keeps them unchanged; you can also pass an estimator. Overlapping selections process a column twice, and a `"drop"` entry does NOT cancel a column another transformer also selects: in the pattern above, numeric `id_x` and `c_raw` matched both the number selector and the drop selector, were scaled, and appeared in the output (checked on 1.9.1). Make selectors mutually exclusive, e.g. `selector(dtype_include="number", pattern=r"^(?!id_)(?!.*_raw$)")` for the numeric branch (dtype and pattern combine with AND).

## Gotchas
- A pandas `bool` column is not selected by `dtype_include="number"` (pandas 2.3.3, scikit-learn 1.9.1) and falls into the remainder; select it with `dtype_include="bool"`. Check `pre.transformers_` after fit.
- Object columns holding numbers (read from CSV) are selected as categorical; fix dtypes at load time.
- `verbose_feature_names_out=False` with two transformers emitting the same name does not fail at `fit`; `get_feature_names_out()` raises `ValueError: Output feature names: ['a'] are not unique`.

## Verify
- [ ] After fit: `for name, trans, cols in pre.transformers_: print(name, cols)` shows each column in exactly one group.
- [ ] `pre.get_feature_names_out()` length equals transformed column count.
