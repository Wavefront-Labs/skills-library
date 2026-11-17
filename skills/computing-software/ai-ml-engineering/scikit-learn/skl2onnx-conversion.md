---
id: computing-software.ai-ml-engineering.scikit-learn.skl2onnx-conversion
name: skl2onnx-conversion
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, skl2onnx, onnx-export, onnx-runtime, model-persistence, inference-deployment]
level: practitioner
status: verified
description: "Convert scikit-learn pipelines to ONNX with skl2onnx: initial_types, ColumnTransformer inputs, options like zipmap, unsupported estimators, and numeric parity checks in ORT."
sources:
  - https://onnx.ai/sklearn-onnx/
  - https://onnx.ai/sklearn-onnx/supported.html
  - https://onnxruntime.ai/docs/get-started/with-python.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# skl2onnx conversion

**Why:** serve sklearn models without Python/sklearn version lock-in via ONNX Runtime (the scikit-learn persistence guide says the ONNX serving environment can be minimal and does not need Python); versions tested: skl2onnx 1.20.0, onnx 1.23.2, onnxruntime 1.31.0, Python 3.14.

## Basic conversion
```python
from skl2onnx import to_onnx
from skl2onnx.common.data_types import FloatTensorType
onx = to_onnx(pipe, initial_types=[("input", FloatTensorType([None, X.shape[1]]))],
              target_opset=17, options={id(pipe[-1]): {"zipmap": False}})   # output names: label, probabilities
open("model.onnx", "wb").write(onx.SerializeToString())
```
- `zipmap=False` returns probabilities as a plain tensor instead of a list of dicts (default output was a list of `{0: p0, 1: p1}` dicts; much easier to consume as a tensor).
- Convert numeric inputs to float32: a float32 model fed float64 data raises `INVALID_ARGUMENT: Unexpected input data type. Actual: (tensor(double)), expected: (tensor(float))`. In tests, float32 parity was within 1.4e-7 (random forest) and 1.1e-7 (mixed-type pipeline); labels matched on 2,000 rows. A `DoubleTensorType` model gave 2.2e-16 on a scaler + logistic regression pipeline, and also converted for a random forest. Tree thresholds near a boundary can flip in float32; none did in these tests.

## DataFrames with mixed types
Declare one input per column (or per dtype group) and make the ColumnTransformer select by those names:
```python
from skl2onnx.common.data_types import StringTensorType
initial_types = [("age", FloatTensorType([None, 1])), ("country", StringTensorType([None, 1]))]
```
Feed `{"age": df[["age"]].values.astype(np.float32), "country": df[["country"]].values}` at inference.

## Coverage
Linear models, `RandomForestClassifier`, `GradientBoostingClassifier`, `KNeighborsClassifier` and `SVC(probability=True)` converted in tests; `HistGradientBoostingClassifier` did NOT convert on this stack (`Unable to create node 'TreeEnsembleClassifier'`), so test your estimator. XGBoost needs a registered converter: `XGBClassifier` alone raised `MissingShapeCalculator`; after `update_registered_converter(xgb.XGBClassifier, "XGBoostXGBClassifier", calculate_linear_classifier_output_shapes, convert_xgboost, options={...})` (with `onnxmltools` installed) parity was 1.2e-7 with `target_opset={"": 15, "ai.onnx.ml": 3}`.  `FunctionTransformer(np.log1p)` raised `FunctionTransformer is not supported unless the transform function is None`; rewrite as supported ops or write a custom converter.

## Parity check
```python
import onnxruntime as ort
sess = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
onnx_proba = sess.run(None, {"input": X_test.astype(np.float32)})[1]
np.testing.assert_allclose(pipe.predict_proba(X_test.astype(np.float32)), onnx_proba, rtol=1e-4, atol=1e-5)
```
Also compare predicted labels and count mismatches; for trees, a handful of borderline flips is possible in float32 (none in the 2,000-row test) unless you use double precision (`DoubleTensorType` where supported). An `options={"cast": True}` entry is not valid for `RandomForestClassifier` (the error lists `decision_leaf, decision_path, nocl, output_class_labels, raw_scores, zipmap`).

## Verify
- [ ] Mismatch rate on a full validation set below an agreed threshold; ORT latency benchmarked.
