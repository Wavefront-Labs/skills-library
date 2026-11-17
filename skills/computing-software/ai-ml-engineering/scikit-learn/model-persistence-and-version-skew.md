---
id: computing-software.ai-ml-engineering.scikit-learn.model-persistence-and-version-skew
name: model-persistence-and-version-skew
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, joblib, pickle, model-persistence, version-skew, onnx, skops, serialization, model-deployment, backward-compatibility, security, pickle-vulnerability, untrusted-model-files]
level: practitioner
status: verified
description: "Persist and load scikit-learn models safely across environments: joblib/pickle version-skew risks, the pickle security problem, and ONNX/skops as safer alternatives."
sources:
  - https://scikit-learn.org/stable/model_persistence.html
  - https://skops.readthedocs.io/en/stable/
  - https://onnx.ai/sklearn-onnx/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Persisting scikit-learn models without a version-skew or security surprise

**Goal:** save a trained scikit-learn model and reload it later (possibly on a different machine, a different scikit-learn version, or a different Python version) and get back the exact same model — or know explicitly why you can't.

## 1. `joblib`/`pickle` are not forward- or backward-compatible across scikit-learn versions
- The scikit-learn docs say none of the persistence methods (skops.io, joblib, pickle, cloudpickle) support loading a model trained with a different scikit-learn version: such loads "might load" but are "entirely unsupported and inadvisable", and results can differ or crash the process. Estimators loaded under a different version emit `sklearn.exceptions.InconsistentVersionWarning` (reproduced on 1.9.1 by unpickling state tagged 1.3.0: `Trying to unpickle estimator LogisticRegression from version 1.3.0 when using version 1.9.1`); promote it to an error with `warnings.simplefilter("error", InconsistentVersionWarning)` and read `w.original_sklearn_version` from the caught warning. Do not rely on the warning alone: it is not raised for every change. "It loaded without an error" is not evidence it's the same model; compare predictions on a fixed test set after loading on the target version, every time you change scikit-learn version.
- **Always pin and record the exact scikit-learn (and numpy/scipy) version used to train, alongside the pickled artifact** — store it as metadata next to the model file, not just in a requirements.txt that can drift. When loading an old model, install that exact version in the loading environment rather than "whatever's current" — upgrading scikit-learn in the serving environment without re-validating every persisted model is a common source of "the model changed behavior and nobody touched the model."
- `joblib.dump`/`joblib.load` is the traditional choice for models holding large NumPy arrays, but it is not faster than plain `pickle` on current Python: a 72 MB float64 array dumped in 0.010 s with `pickle.dumps(protocol=5)` versus 0.033 s with `joblib.dump` (one run, Python 3.14). Both inherit the exact same version-skew and code-execution risks; neither fixes cross-version compatibility.

## 2. The security problem pickle doesn't warn you about
- **Unpickling is arbitrary code execution** — `pickle.load`/`joblib.load` on a file from an untrusted source can execute attacker-controlled code during deserialization, not just "load a model." Never load a pickled model from a source you don't control (a public model-sharing site without provenance, an untrusted user upload) — this is a genuine production security boundary, not a theoretical concern.
- If models must be exchanged across trust boundaries (a model-sharing platform, a third-party contributor's output), use **`skops`** (`skops.io`, a separate package recommended in the scikit-learn docs; tested here at 0.16.0) — a format that does not use pickle and only loads types and functions trusted by default or by the user: inspect `skops.io.get_untrusted_types(data=...)` (or `file=`) and pass an explicit `trusted=` list to `loads`/`load`. Its documented cons: slower than pickle, supports fewer types, and still needs the same environment as training. Prefer this over pickle whenever the loading environment doesn't fully trust the file's origin.

## 3. When you need true cross-version/cross-language portability
- **ONNX** (via `sklearn-onnx` / `skl2onnx`) converts many scikit-learn estimators into a standardized, versioned graph format that's loadable by ONNX Runtime without the Python object (the scikit-learn docs: "the ONNX runtime does not require python"). It suits serving without a Python/scikit-learn runtime. The docs add that arbitrary computation can be expressed in ONNX, so serve ONNX files from a sandboxed environment, and that the original Python object cannot be reconstructed from the ONNX file. Tested: `skl2onnx.to_onnx(LogisticRegression, X[:1])` plus `onnxruntime.InferenceSession` reproduced `predict` exactly and `predict_proba` to 6e-8 (skl2onnx 1.20.0, onnxruntime 1.31.0).
- Not every custom transformer converts cleanly to ONNX — a hand-written `BaseEstimator` with arbitrary Python logic in `transform` has no direct ONNX equivalent unless you register a custom converter (e.g. `FunctionTransformer(np.log1p)` raised `RuntimeError: FunctionTransformer is not supported unless the transform function is None`); check conversion support before committing to ONNX for a pipeline with non-trivial custom steps, and test numerically that ONNX Runtime's output matches the original scikit-learn pipeline's output within a small tolerance (floating-point operation order can differ slightly between the two runtimes).
- For a model that must be interpretable/auditable as plain parameters rather than an opaque binary blob (a simple linear/logistic model, a small decision tree), consider serializing just the learned parameters (coefficients, thresholds) as JSON and reimplementing the predict step directly — more work up front, but immune to every pickle/version-skew problem above, and trivially auditable.

## Verify
- [ ] Every persisted model file has its exact training-time scikit-learn/numpy/scipy versions recorded as metadata alongside it.
- [ ] After any scikit-learn version change in a serving environment, existing persisted models are reloaded and their predictions compared against a fixed reference output before trusting them.
- [ ] No pickled/joblib model is ever loaded from a source outside your own trust boundary.
- [ ] If cross-trust-boundary sharing is needed, `skops` (or an equivalent non-arbitrary-execution format) is used instead of raw pickle.
- [ ] If ONNX is used, conversion was tested for numerical parity against the original scikit-learn pipeline on real validation data, and any custom transformers were confirmed to have working converters.
