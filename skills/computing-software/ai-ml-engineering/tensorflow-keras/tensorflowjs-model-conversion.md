---
id: computing-software.ai-ml-engineering.tensorflow-keras.tensorflowjs-model-conversion
name: tensorflowjs-model-conversion
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, tensorflowjs, tfjs-converter, graph-model, layers-model, browser-inference, model-quantization]
level: practitioner
status: docs-checked
description: "Convert SavedModels and Keras models to TensorFlow.js: tensorflowjs_converter formats, weight quantization and sharding, loading graph vs layers models in the browser."
sources:
  - https://github.com/tensorflow/tfjs/tree/master/tfjs-converter
  - https://github.com/tensorflow/tfjs/blob/master/tfjs-converter/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TensorFlow.js model conversion

**Goal:** run a TensorFlow model in the browser or Node.js with acceptable download size and the same predictions.

## Convert
```bash
pip install tensorflowjs
# SavedModel -> graph model
tensorflowjs_converter --input_format=tf_saved_model --output_format=tfjs_graph_model \
  --signature_name=serving_default --saved_model_tags=serve \
  ./export/saved_model ./web_model
# Keras HDF5 -> layers model
tensorflowjs_converter --input_format=keras ./model.h5 ./web_layers_model
```
Output: `model.json` (topology + weights manifest) and `group1-shard*of*.bin` weight files.

- **Graph model** (`tfjs_graph_model`): load with `tf.loadGraphModel`.
- **Layers model** (`tfjs_layers_model`): load with `tf.loadLayersModel`.
- Run the converter in a virtual environment or Docker container: the README warns it pulls its own subset of TensorFlow, which can conflict with an existing TensorFlow or Keras install.
- The README lists TensorFlow SavedModel, TF Hub, Keras HDF5, tf.keras SavedModel and Flax/JAX inputs and does not mention Keras 3 `.keras` files; export a Keras 3 model as a SavedModel (`model.export(...)`) and convert that, and check the README for current Keras 3 support.

## Size and loading
- `--quantize_float16` and `--quantize_uint8` take an optional comma-separated list of node names (wildcards allowed) and match all nodes when given no list; `--quantize_uint16` also exists and `--quantization_bytes` is deprecated. Check accuracy after quantizing.
- `--weight_shard_size_bytes` sets the weight shard size (default 4 MB, 4194304 bytes; supported for `tfjs_layers_model` and `tfjs_graph_model` outputs).

## Run
```js
import * as tf from '@tensorflow/tfjs';
const model = await tf.loadGraphModel('https://cdn.example.com/models/v3/model.json');
const x = tf.tensor(inputArray, [1, 224, 224, 3]);
const y = model.predict(x);
const out = await y.data();
tf.dispose([x, y]);                  // free the tensors' memory
```
## Gotchas
- The converter cannot map every TensorFlow op; if conversion or loading reports an unsupported op, replace that op in the TensorFlow model before exporting.
- Preprocessing (resize, normalise) must be reimplemented in JS identically; better to put it in the exported graph.

## Verify
- [ ] JS predictions match Python predictions on the same inputs (allow a larger tolerance after quantization).
- [ ] Total model download size measured and acceptable.
- [ ] Memory stable over many predictions (`tf.memory().numTensors` not growing).

## Checked

Checked 2026-10-25 against tfjs-converter README (tensorflow/tfjs master). Confirmed `--input_format`, `--output_format`, `--signature_name`, `--saved_model_tags`, the quantization flags and their node-list semantics, `--weight_shard_size_bytes` default of 4 MB, the `tfjs_graph_model` and `tfjs_layers_model` formats with `tf.loadGraphModel` and `tf.loadLayersModel`, `model.json` with `group1-shard*of*.bin` weight files, and the virtual-environment warning (converter README, tfjs master, last commit 2026-04-06). Removed the Keras 3 conversion claim, backend ranking, dequantize-at-load, CDN, executeAsync, GPU texture leak, warm-up and tolerance statements, which the README does not cover.

Method: documentation only; no commands were run.
