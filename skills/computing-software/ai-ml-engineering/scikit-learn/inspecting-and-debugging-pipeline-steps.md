---
id: computing-software.ai-ml-engineering.scikit-learn.inspecting-and-debugging-pipeline-steps
name: inspecting-and-debugging-pipeline-steps
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, pipeline-debugging, pipeline, get-feature-names-out, set-output, named-steps, column-transformer]
level: practitioner
status: verified
description: "Debug scikit-learn Pipelines: slice and index steps, see intermediate outputs with set_output(transform='pandas'), trace feature names and find which step breaks."
sources:
  - https://scikit-learn.org/stable/modules/compose.html#pipeline
  - https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspecting and debugging pipeline steps

## Access steps
```python
pipe = Pipeline([("prep", preprocessor), ("select", SelectKBest(k=20)), ("clf", LogisticRegression())])
pipe.named_steps["clf"].coef_          # or pipe["clf"], pipe[-1]
pipe[:-1]                              # sub-pipeline of all but the last step (shares fitted steps)
Xt = pipe[:-1].transform(X_valid)      # what the classifier actually receives
```
For a fitted `GridSearchCV`: `search.best_estimator_[:-1]`.

## See intermediate data as DataFrames
```python
pipe.set_output(transform="pandas")    # every transformer returns a DataFrame with column names
pipe[:-1].fit_transform(X_train).head()
```
`sklearn.set_config(transform_output="pandas")` does it globally. Sparse outputs (OneHotEncoder default) cannot be pandas: `pipe.set_output(transform="pandas")` then raises `ValueError: Pandas output does not support sparse data. Set sparse_output=False` at fit time (tested); set `sparse_output=False` while debugging. `GridSearchCV(..., error_score="raise").best_estimator_[:-1]` returned the fitted sub-pipeline (tested).

## Feature names through the pipeline
```python
names = pipe[:-1].get_feature_names_out()     # e.g. 'num__age', 'cat__city_Paris'
coef = pd.Series(pipe[-1].coef_.ravel(), index=names).sort_values()
```
Fails if some step lacks `get_feature_names_out` (custom transformers: implement it, or use `FunctionTransformer(feature_names_out="one-to-one")`).

## ColumnTransformer specifics
- `ct.transformers_` (fitted) lists `(name, fitted_transformer, columns)` including the auto-added `remainder`.
- `ct.named_transformers_["num"]` gives the fitted sub-transformer (e.g. scaler means).
- `ct.output_indices_` maps each transformer to output column slices.
- Dropped columns: `remainder="drop"` is default; check you did not lose columns silently.

## Finding the failing step
- `Pipeline(..., verbose=True)` prints each step's fit time.
- Run step by step:
```python
Xt = X_train
for name, step in pipe.steps[:-1]:
    Xt = step.fit_transform(Xt, y_train)
    print(name, getattr(Xt, "shape", None), np.isnan(np.asarray(Xt, dtype=float)).sum())
```
- Errors inside cross-validation are hidden behind "fit failed" warnings: use `error_score="raise"` in `cross_validate`/`GridSearchCV` to get the traceback.
- Caching (`memory=`) can hide code changes in custom transformers; clear the cache directory when editing them.

## Visualise
In Jupyter the estimator HTML repr shows the step tree with parameters (non-default highlighted). `sklearn.utils.estimator_html_repr(pipe)` returns the HTML as a string (117 KB for a 3-step pipeline in a test); write it to a file yourself for reports.
