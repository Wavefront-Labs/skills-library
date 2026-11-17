---
id: computing-software.ai-ml-engineering.tensorflow-keras.litert-tflite-conversion-and-quantization
name: litert-tflite-conversion-and-quantization
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, tflite, litert, tfliteconverter, post-training-quantization, int8-quantization, representative-dataset, on-device]
level: practitioner
status: docs-checked
description: "Convert TF/Keras models to LiteRT (TFLite): dynamic-range, float16 and full-integer quantization with a representative dataset, Select TF ops, and accuracy checks."
sources:
  - https://ai.google.dev/edge/litert/models/convert_tf
  - https://ai.google.dev/edge/litert/models/post_training_quantization
  - https://ai.google.dev/edge/litert/migration
  - https://github.com/google-ai-edge/LiteRT
  - https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/python/lite.py
  - https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/python/interpreter.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LiteRT (TFLite) conversion and quantization

**Goal:** ship a compact, fast on-device model and confirm it still matches the float model's accuracy. (LiteRT continues TensorFlow Lite. The LiteRT README says the TensorFlow Lite packages and `tensorflow/lite/` are in maintenance mode and points new on-device code to the LiteRT APIs; see the migration guide at https://ai.google.dev/edge/litert/migration. The `tf.lite.TFLiteConverter` calls below are still present in TensorFlow's `tensorflow/lite/python/lite.py`.)

## Convert
```python
import tensorflow as tf
conv = tf.lite.TFLiteConverter.from_saved_model("export/saved_model")   # preferred over from_keras_model
tflite_bytes = conv.convert()
open("model.tflite", "wb").write(tflite_bytes)
```
Export Keras 3 models first with `model.export("export/saved_model")`.

## Quantization options
| Mode | Settings | Size | Notes |
|---|---|---|---|
| Dynamic range | `conv.optimizations = [tf.lite.Optimize.DEFAULT]` | smaller | no representative data needed |
| Float16 | `+ conv.target_spec.supported_types = [tf.float16]` | smaller | float16 weights |
| Full integer | DEFAULT + `representative_dataset` + int8 ops | smaller | needs calibration data |

Full integer:
```python
def rep_data():
    for x, _ in calib_ds.take(200):          # 100-500 real samples, preprocessed like inference
        yield [tf.cast(x, tf.float32)]
conv.optimizations = [tf.lite.Optimize.DEFAULT]
conv.representative_dataset = rep_data
conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
conv.inference_input_type = tf.int8          # or tf.uint8; omit to keep float I/O
conv.inference_output_type = tf.int8
```
Integer I/O means the app must quantize inputs with the model's scales and zero points (`interp.get_input_details()[0]["quantization_parameters"]`; the older `quantization` field is deprecated).

## Unsupported ops
If the converter reports operators the native runtime does not support, either rewrite with supported ops, or allow select TF ops (Flex):
```python
conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
```

## Validate
```python
from ai_edge_litert.interpreter import Interpreter   # tf.lite.Interpreter is deprecated
interp = Interpreter(model_path="model.tflite")
interp.allocate_tensors()
inp, out = interp.get_input_details()[0], interp.get_output_details()[0]
interp.set_tensor(inp["index"], x); interp.invoke(); y = interp.get_tensor(out["index"])
```
Run the full validation set through the converted model and compare metrics with the float model; if the quantized model loses too much accuracy, consider quantization-aware training. `tf.lite.Interpreter` is documented as deprecated and scheduled for deletion in TF 2.20 in favour of the `ai_edge_litert` interpreter.

## Gotchas
- Representative data must be preprocessed exactly like real inference inputs; random noise calibrates the wrong ranges.
- Dynamic shapes: set a fixed input signature on export, or resize inputs with `interp.resize_tensor_input`.
- Benchmark on the target device; desktop timings mean little.

## Verify
- [ ] Validation metric of the .tflite model within tolerance of the float model.
- [ ] Model size and on-device latency measured.
- [ ] App-side input quantization matches the model's scale/zero point.

## Checked

Checked 2026-10-25 against TensorFlow master (2026-10) and the LiteRT README. Checked against TensorFlow `lite.py`, `interpreter.py` and `convert.py` (master, last changed 2026-10-23) and the LiteRT README: `TFLiteConverter.from_saved_model`, `optimizations`, `representative_dataset`, `target_spec.supported_ops` and `supported_types`, `OpsSet.TFLITE_BUILTINS_INT8` and `SELECT_TF_OPS`, `inference_input_type` and `inference_output_type` (int8 and uint8), the conditions that select dynamic range, float16 and full-integer quantization, `resize_tensor_input`, the deprecated `quantization` field in favour of `quantization_parameters`, the `tf.lite.Interpreter` deprecation notice, and the maintenance-mode statement. The ai.google.dev conversion pages are not in a public repository and were not read. Removed size multipliers, the accuracy-loss figure, the Flex binary-size claim, the exact error string, the model-size note and the benchmark tool name.

Method: documentation only; no commands were run.
