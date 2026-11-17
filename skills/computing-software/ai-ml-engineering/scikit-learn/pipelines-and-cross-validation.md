---
id: computing-software.ai-ml-engineering.scikit-learn.pipelines-and-cross-validation
name: pipelines-and-cross-validation
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, sklearn, pipeline, columntransformer, cross-validation, cross-validate, stratifiedkfold, groupkfold, timeseriessplit, gridsearchcv, randomizedsearchcv, hyperparameter-tuning, data-leakage, onehotencoder, standardscaler, simpleimputer, joblib, model-persistence, nested-cross-validation, machine-learning, python]
level: practitioner
status: verified
description: "Build leakage-free scikit-learn Pipelines with ColumnTransformer, pick the right CV splitter, tune with GridSearchCV using step__param names, and persist with joblib safely."
sources:
  - https://scikit-learn.org/stable/modules/compose.html
  - https://scikit-learn.org/stable/modules/cross_validation.html
  - https://scikit-learn.org/stable/modules/grid_search.html
  - https://scikit-learn.org/stable/model_persistence.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scikit-learn Pipelines and Cross-Validation — honest scores, one object to ship

**Goal:** wrap all preprocessing and the model in a single Pipeline so cross-validation scores are honest and the exact same transformations run in production.

## 1. Build the pipeline
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

num = ["age", "income"]; cat = ["region", "plan"]
pre = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num),
    ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=20), cat),
])
pipe = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))])
```
- `handle_unknown="ignore"` prevents crashes when production sees a category absent from training.
- `ColumnTransformer` drops unlisted columns by default (`remainder="drop"`); IDs and timestamps silently disappear, which is usually what you want — but be deliberate.
- Get output feature names with `pipe[:-1].get_feature_names_out()` (fit first; gave `num__age ... cat__plan_y` on a test frame). The whole example, including `cross_validate(..., groups=groups)` with `StratifiedGroupKFold`, `RandomizedSearchCV.fit(X, y, groups=groups)`, swapping `clf` for `HistGradientBoostingClassifier()`, `HalvingRandomSearchCV` and prediction on an unseen region value, ran on scikit-learn 1.9.1.

## 2. Why the pipeline prevents leakage
Fitting a scaler, imputer, target encoder or feature selector on the full dataset before splitting lets validation rows influence training — scores look better than reality. Inside a Pipeline passed to CV, every transformer is re-fit on each training fold only. The most damaging case is feature selection (e.g. `SelectKBest`) outside CV: with many noise features it can produce high "accuracy" on pure noise (100 rows, 2000 random features, random labels, `SelectKBest(k=20)` before CV: accuracy 0.85; inside a Pipeline: 0.49). Broader leakage patterns: computing-software.ai-ml-engineering.feature-engineering.leakage-safe-feature-construction.

## 3. Choose the splitter to match deployment
| Situation | Splitter |
|---|---|
| Classification, i.i.d. rows | `StratifiedKFold(5, shuffle=True, random_state=0)` |
| Several rows per user/patient/device | `GroupKFold` / `StratifiedGroupKFold`, pass `groups=` |
| Predicting the future | `TimeSeriesSplit(n_splits=5, gap=...)` |

For classifiers, passing an integer `cv=5` already stratifies but does not shuffle (`check_cv(5, y, classifier=True)` gives `StratifiedKFold` with `shuffle=False`; for regressors it gives `KFold`). Groups split wrong is the most common inflated-score bug: the same customer in train and validation lets the model memorise identity.

```python
from sklearn.model_selection import cross_validate
res = cross_validate(pipe, X, y, cv=cv, groups=groups,
                     scoring=["roc_auc", "average_precision"],
                     return_train_score=True, n_jobs=-1)
```
Report mean and standard deviation across folds; a large train/validation gap means overfitting. Design of splits and metrics in general: computing-software.ai-ml-engineering.model-training.data-splits-and-evaluation.

## 4. Tune with step__param names
```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import loguniform
search = RandomizedSearchCV(pipe,
    {"clf__C": loguniform(1e-3, 1e2),
     "pre__cat__min_frequency": [5, 20, 50]},
    n_iter=40, cv=cv, scoring="roc_auc", n_jobs=-1, random_state=0)
search.fit(X, y, groups=groups)
```
- Names chain step names with double underscores; `pipe.get_params().keys()` lists every valid key.
- You can swap whole steps: `{"clf": [LogisticRegression(), HistGradientBoostingClassifier()]}`.
- Prefer `RandomizedSearchCV` or `HalvingRandomSearchCV` (experimental import `sklearn.experimental.enable_halving_search_cv`) when there are more than ~3 parameters.
- `best_score_` is optimistically biased because it selected the max. Report on an untouched test set or use nested CV (search inside `cross_validate`).
- `refit=True` (default) retrains the best config on all data; with multiple scorers you must name which one to refit on.

## 5. Persist and reload
```python
import joblib, sklearn
joblib.dump(search.best_estimator_, "model.joblib")
```
- Pickle/joblib files are only guaranteed to load in the **same scikit-learn version** (and compatible NumPy/SciPy). Record versions next to the file (requirements lock, or MLflow — see computing-software.ai-ml-engineering.mlflow.experiment-tracking-and-model-registry) and pin them in the serving image.
- Loading a pickle executes code: never load model files from untrusted sources. The `skops` library offers a safer format; ONNX (`skl2onnx`) suits non-Python serving.
- Custom functions in `FunctionTransformer` must be importable at load time — define them in a module, not a notebook cell.

## Verify
- [ ] No `fit` or `fit_transform` is called on data outside the Pipeline before CV.
- [ ] The splitter matches deployment (groups or time) and `groups=` is passed where relevant.
- [ ] Every search key is in `pipe.get_params()`; the final score comes from data not used in the search.
- [ ] The loaded joblib model gives identical predictions to the in-memory one in a fresh environment with pinned versions.
- [ ] Inference on a row with an unseen category returns a prediction, not an error.
