---
id: computing-software.ai-ml-engineering.feature-engineering.interaction-and-ratio-features
name: interaction-and-ratio-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, interaction-features, polynomial-features, ratio-features, splinetransformer, feature-crosses]
level: practitioner
status: gated
description: "Build interaction, polynomial and ratio features (per-unit rates, differences, crosses) for linear and tree models, control feature explosion, and avoid leakage and division traps."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html#polynomial-features
  - https://developers.google.com/machine-learning/crash-course/categorical-data/feature-crosses
  - https://www.feat.engineering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interaction and ratio features

## When they help
- **Linear models** can't learn interactions or nonlinearity on their own: explicit products, splines and crosses help a lot.
- **Tree ensembles** learn interactions but approximate ratios and differences poorly with axis-aligned splits (debt/income needs many splits). Domain ratios often still give GBMs a solid boost.
- Neural nets learn them given data, but explicit features still help on small tabular data.

## Ratios and domain arithmetic
```python
eps = 1e-9
df["debt_to_income"] = df["debt"] / (df["income"] + eps)
df["price_per_sqft"] = df["price"] / df["sqft"].replace(0, np.nan)        # NaN rather than inf
df["spend_per_visit"] = df["spend_30d"] / df["visits_30d"].clip(lower=1)
df["days_since_last"] = (df["as_of"] - df["last_purchase"]).dt.days
df["delta_vs_user_mean"] = df["amount"] - df.groupby("user_id")["amount"].transform("mean")   # leakage risk: see below
```
- Choose ratios from domain knowledge (rates, per-capita, per-unit, utilisation); blind all-pairs ratios explode and overfit.
- Division by zero: decide semantics (NaN plus missing indicator, or clip denominator); infinite values break most models.
- Ratios of noisy small numbers are very noisy: smooth (add pseudo-counts) for rates like click-through: `(clicks + a) / (views + a + b)`.

## Polynomial and pairwise interactions
```python
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)   # x_i * x_j only
pipe = make_pipeline(StandardScaler(), poly, RidgeCV(alphas=np.logspace(-3, 3, 30)))
```
- p features -> p(p-1)/2 interactions; with 100 features that's 4950. Regularise (Ridge/Lasso) or select.
- Splines (`SplineTransformer`) usually beat raw polynomials for single-feature nonlinearity (no wild extrapolation).
- Categorical x categorical crosses (`country_x_device`): concatenate strings then encode (one-hot with `min_frequency`, hashing or target encoding).
- `get_feature_names_out()` gives readable names like `age income` (checked: interaction_only gives `age`, `income`, `z`, `age income`, ...; 100 features give 4,950 pairs).

## Finding useful interactions
- GBM interaction statistics (Friedman H via 2-way partial dependence), SHAP interaction values, or EBM (`interpret` package) pairwise detection (gated: unconfirmed, source is paywalled or blocked).
- Error analysis: segments where residuals are large suggest which crosses to add.

## Leakage traps
Group aggregates (user mean, category mean of target-related fields) computed over the whole dataset leak future and test information. Compute them out-of-fold or point-in-time (only data before the row's timestamp).

## Verify
CV score with vs without each feature family, using the same folds; drop families that don't help. Check no inf/NaN appear: `np.isfinite(X).all()` on numeric columns.
