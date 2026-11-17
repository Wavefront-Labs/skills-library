---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf2onnx-conversion
name: tf2onnx-conversion
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tf2onnx, onnx-export, onnx-runtime, savedmodel, model-conversion]
level: practitioner
status: docs-checked
description: "Convert TensorFlow/Keras models to ONNX with tf2onnx: CLI and Python API, opset choice, input signatures and dynamic axes, unsupported ops, and ONNX Runtime parity checks."
sources:
  - https://github.com/onnx/tensorflow-onnx
  - https://github.com/onnx/tensorflow-onnx/blob/main/README.md
  - https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/python/onnxruntime_inference_collection.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tf2onnx conversion

**Use when:** serving a TF/Keras model in ONNX Runtime, TensorRT or a non-TF stack.

## From a SavedModel (most robust)
```bash
python -m tf2onnx.convert --saved-model export/1 --signature_def serving_default \
  --opset 17 --output model.onnx
```

## From Keras in Python
```python
import tf2onnx, tensorflow as tf
spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="image"),)
model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=17, output_path="model.onnx")
```
The tf2onnx README documents `from_keras` for tf.keras models and tests with TensorFlow 2.13 or newer and Python 3.10-3.12; it does not mention Keras 3, so for a Keras 3 model export a SavedModel first (`model.export("export/1")`) and convert that. The README also says the project is looking for a new maintainer.

## Options that matter
- `--opset`: tf2onnx tests opsets 14 to 18 and defaults to 15; choose the highest opset your runtime supports.
- `--inputs-as-nchw image:0` transposes NHWC inputs to NCHW for runtimes that prefer it.
- `--large_model` (TF2 SavedModel only) writes a zip containing the ONNX protobuf and externally stored large tensors so models over 2 GB can convert.

## Failures
- TensorFlow has many more ops than ONNX, so some models fail to map; check the supported-op list (`support_status.md` in the repository). Ops that onnxruntime does not recognise can be tagged with a custom op domain (`--custom-ops`).

## Parity check
```python
import onnxruntime as ort, numpy as np
sess = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
x = np.random.rand(4, 224, 224, 3).astype(np.float32)
np.testing.assert_allclose(model(x).numpy(), sess.run(None, {"image": x})[0], rtol=1e-4, atol=1e-5)
```

## Verify
- [ ] Outputs match TF on a validation batch; latency measured in ORT with the target execution provider.

## Checked

Checked 2026-10-25 against tensorflow-onnx README (onnx/tensorflow-onnx main, 2026-10-07). Confirmed the `python -m tf2onnx.convert` options `--saved-model`, `--signature_def`, `--opset`, `--output`, `--inputs-as-nchw`, `--large_model` (TF2 SavedModel only, zip output) and custom-op tagging, `tf2onnx.convert.from_keras(model, input_signature, opset, output_path)` returning `(model_proto, external_tensor_storage)`, the tested opset range 14-18 with default 15, TensorFlow 2.13+ and Python 3.10-3.12 support, the maintainer-wanted notice (tf2onnx README, last commit 2026-10-07), and `onnxruntime.InferenceSession(path, providers=[...])` and `run` (ONNX Runtime source). Removed the dynamic-axes claim, `--rename-inputs`, `--rename-outputs`, onnxruntime-extensions, ONNX Loop performance and `onnxsim` statements.

Method: documentation only; no commands were run.
