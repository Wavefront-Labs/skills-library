---
id: computing-software.ai-ml-engineering.scikit-learn.target-label-encoders-multilabelbinarizer
name: target-label-encoders-multilabelbinarizer
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, multilabelbinarizer, labelencoder, labelbinarizer, multilabel-classification, target-encoding-labels]
level: practitioner
status: verified
description: "Encode targets (not features) correctly: LabelEncoder, LabelBinarizer and MultiLabelBinarizer for multilabel y, inverse_transform, unseen labels and when you need none of them."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing_targets.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html
  - https://scikit-learn.org/stable/modules/multiclass.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Target encoders: LabelEncoder, LabelBinarizer, MultiLabelBinarizer

**Rule:** these transform **y**, never X. For categorical features use OneHotEncoder/OrdinalEncoder inside a ColumnTransformer.

## Do you need one at all?
Scikit-learn classifiers accept string labels directly and expose `classes_`; `predict` returns original labels (`LogisticRegression` fitted on "yes"/"no" returned `['yes' 'yes']`, `classes_` `['no' 'yes']`). You only need encoders for: multilabel targets, frameworks that require integer labels (Keras, XGBoost native API), or custom metrics.

## LabelEncoder
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder().fit(y_train)          # classes_ sorted
y_int = le.transform(y_train); labels = le.inverse_transform(pred_int)
```
Unseen labels at transform raise `ValueError: y contains previously unseen labels: np.str_('z')` (message shown with numpy 2 reprs). Fit on the union of known classes, or map unknowns explicitly.

## LabelBinarizer
One-vs-rest indicator matrix for a single-label multiclass target (binary target gives one column: shapes `(3, 1)` for two classes and `(3, 3)` for three). Mostly for custom one-vs-rest code.

## MultiLabelBinarizer (multilabel)
```python
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
Y = mlb.fit_transform([["sports", "news"], ["tech"], []])   # shape (n, n_labels), 0/1
mlb.classes_                                                 # column order
mlb.inverse_transform(Y_pred)                               # list of tuples
```
- `classes=[...]` fixes column order and includes labels absent from training (`classes=["news", "sports", "tech", "extra"]` gave 4 columns); unknown labels at transform are ignored with a warning (`unknown class(es) ['zzz'] will be ignored`). Without `classes`, `classes_` is sorted alphabetically.
- `sparse_output=True` for thousands of labels (returns a `csr_matrix`).
- Train with estimators that accept 2D y (`RandomForestClassifier`, `KNeighborsClassifier`, `MLPClassifier` fitted) or wrap: `MultiOutputClassifier(LogisticRegression())`, `ClassifierChain` to model label correlations (both fitted); a bare `LogisticRegression` raises `y should be a 1d array, got an array of shape (100, 2)`.
- Multilabel metrics: `f1_score(Y, Y_pred, average="samples"|"micro"|"macro")`, `hamming_loss`, `jaccard_score`.
- Stratify multilabel splits with iterative stratification (scikit-multilearn 0.2.0, `iterative_train_test_split(X, Y, test_size=.3)`, ran on Python 3.12 and kept label frequencies within about 0.005 of the full set) rather than `stratify=`: `train_test_split(..., stratify=Y)` on a 5-label matrix with a 2%-prevalence label raised `The least populated classes in y have only 1 member`, though it worked for three 30%-prevalence labels.

## Verify
- [ ] Persist the fitted encoder with the model and test `inverse_transform` in the serving path.
- [ ] Column order (`classes_`) logged alongside the model.
