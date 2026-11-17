---
id: computing-software.ai-ml-engineering.scikit-learn.array-api-gpu-dispatch
name: array-api-gpu-dispatch
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, array-api, gpu, cupy, pytorch-tensors, array-api-dispatch, acceleration]
level: practitioner
status: gated
description: "Run supported scikit-learn estimators on GPU arrays via Array API dispatch with PyTorch or CuPy inputs: enabling it, supported estimators, dtype/device rules and limits."
sources:
  - https://scikit-learn.org/stable/modules/array_api.html
  - https://data-apis.org/array-api/latest/
  - https://scikit-learn.org/stable/modules/generated/sklearn.config_context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Array API dispatch for GPU arrays

scikit-learn can run some estimators directly on non-NumPy arrays (PyTorch tensors, CuPy arrays) that follow the Python Array API standard, keeping computation on the GPU.

## Enable
```python
import sklearn, torch
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
X = torch.as_tensor(X_np, device="cuda", dtype=torch.float32); y = torch.as_tensor(y_np, device="cuda")
with sklearn.config_context(array_api_dispatch=True):
    lda = LinearDiscriminantAnalysis().fit(X, y)
    Xt = lda.transform(X)          # torch tensor on cuda
```
Requirements: `pip install array-api-compat` (and `array-api-strict` for CPU-only testing); set `SCIPY_ARRAY_API=1` in the environment **before importing SciPy or scikit-learn**. It is mandatory: without it, enabling dispatch raises `RuntimeError: Scikit-learn array API support was enabled but scipy's own support is not enabled` (tested on scikit-learn 1.9.1). The docs call the feature experimental and say backwards compatibility is not guaranteed.

No GPU is needed to try the code path: `array_api_strict` arrays under `config_context(array_api_dispatch=True)` fit `LinearDiscriminantAnalysis` and `PCA(svd_solver="full")`, return `array_api_strict` arrays, and `_convert_to_numpy(t, array_api_strict)` matches the NumPy result (tested). CUDA and CuPy behaviour below is from the docs, not run here no GPU available (gated: unconfirmed, source is paywalled or blocked).

## Supported (grows each release)
In scikit-learn 1.9 the docs list `PCA` (`svd_solver` "full", "covariance_eigh" or "randomized" with `power_iteration_normalizer="QR"`), `LinearDiscriminantAnalysis` (solver="svd"), `LogisticRegression` (solver="lbfgs"), `Ridge`/`RidgeClassifier` (solver="svd") and their CV variants, `GaussianMixture` (`init_params` "random"/"random_from_data"), `Nystroem`, `GaussianNB`, preprocessing (`StandardScaler`, `MinMaxScaler`, `MaxAbsScaler`, `Normalizer`, `Binarizer`, `PolynomialFeatures`, `LabelEncoder`, `KernelCenterer`), meta-estimators (`GridSearchCV`, `RandomizedSearchCV`, `FeatureUnion`) when the base estimator qualifies, and many metrics and pairwise kernels. Check the "Estimators and other tools in scikit-learn that support array API compatible inputs" section for your version. An unsupported estimator fails: `RandomForestClassifier().fit()` on an `array_api_strict` array raised `TypeError: 'dtype' must be a dtype` (tested).

## Rules
- Fitted attributes live on the same namespace/device as the input (e.g. `pca.components_` is a CUDA tensor). Convert before pickling or mixing with NumPy: `sklearn.utils._array_api._convert_to_numpy` or `t.cpu().numpy()`.
- `predict`/`transform` expect inputs from the same array library and device as `fit`.
- Some devices lack float64 (PyTorch on MPS, some Intel GPUs); scikit-learn then falls back to float32, which can make results less numerically stable, so use float32 deliberately there.
- Estimators follow X: `y`, `sample_weight` and constructor arguments are converted to X's library and device; scoring functions follow `y_pred`. A pipeline can therefore move X to the GPU mid-way (for example `FunctionTransformer(partial(torch.asarray, device="cuda"))`) after CPU-only steps; the steps that run on the GPU must support the Array API.

## When it helps
Large dense matrices with linear algebra heavy steps (PCA on 1M x 1000, pairwise kernels, LDA). Tree models, gradient boosting, and most iterative solvers are CPU-only in scikit-learn; for those use XGBoost/LightGBM GPU or cuML.

## Alternative: cuML
NVIDIA cuML offers GPU versions of many estimators and `python -m cuml.accel` (zero-code-change acceleration intercepting scikit-learn calls). Broader coverage; separate dependency (gated: unconfirmed, source is paywalled or blocked).

## Verify
Compare outputs to the NumPy path (`np.allclose(Xt.cpu().numpy(), Xt_np, atol=1e-4)`) and time with `torch.cuda.synchronize()` around calls; small data is often faster on CPU due to transfer and launch overhead.
