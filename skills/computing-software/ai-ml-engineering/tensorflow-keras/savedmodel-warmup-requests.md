---
id: computing-software.ai-ml-engineering.tensorflow-keras.savedmodel-warmup-requests
name: savedmodel-warmup-requests
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, savedmodel-warmup, tensorflow-serving, cold-start, predictionlog, tf-serving]
level: practitioner
status: docs-checked
description: "Eliminate first-request latency in TF Serving with SavedModel warmup: writing assets.extra/tf_serving_warmup_requests as PredictionLog TFRecords and validating."
sources:
  - https://www.tensorflow.org/tfx/serving/saved_model_warmup
  - https://www.tensorflow.org/tfx/serving/serving_config
  - https://github.com/tensorflow/serving/blob/master/tensorflow_serving/g3doc/saved_model_warmup.md
  - https://github.com/tensorflow/serving/blob/master/tensorflow_serving/apis/prediction_log.proto
  - https://github.com/tensorflow/serving/blob/master/tensorflow_serving/servables/tensorflow/saved_model_warmup_util.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SavedModel warmup requests

**Problem:** the first requests after a model loads take seconds (lazily initialised runtime components), causing timeouts and p99 spikes on every deploy or scale-up.

## Mechanism
TF Serving replays the requests stored at `<model_version_dir>/assets.extra/tf_serving_warmup_requests` at model load time. Format: TFRecord with each record a `PredictionLog` proto. Warmup is supported for Regress, Classify, MultiInference and Predict.

## Write the warmup file
```python
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_log_pb2

export_dir = "models/my_model/3"
path = f"{export_dir}/assets.extra/tf_serving_warmup_requests"
tf.io.gfile.makedirs(f"{export_dir}/assets.extra")
with tf.io.TFRecordWriter(path) as w:
    for batch_size in (1, 8, 32):                         # cover the shapes you serve
        req = predict_pb2.PredictRequest()
        req.model_spec.name = "my_model"
        req.model_spec.signature_name = "serving_default"
        req.inputs["input_ids"].CopyFrom(tf.make_tensor_proto(tf.zeros([batch_size, 128], tf.int32)))
        log = prediction_log_pb2.PredictionLog(predict_log=prediction_log_pb2.PredictLog(request=req))
        w.write(log.SerializeToString())
```
- Input names must match the signature (`saved_model_cli show --dir ... --all`).
- The warmup data must be representative of the requests used at serving, for example one record per batch size you serve.
- At most 1000 warmup records. Warmup is on by default (`--enable_model_warmup`); `--num_request_iterations_for_warmup` sets how many times each request is replayed and is used only if greater than 0.

## Deploy
Put the file in every new version directory (part of your export step). TF Serving logs `Finished reading warmup data for model at <path>` with the number of warmup records read and the elapsed time.

## Verify
- [ ] Server logs show warmup completed for the version.
- [ ] Load test: first-request latency after a fresh deploy is close to steady-state p50.

## Checked

Checked 2026-10-25 against tensorflow/serving master (last commit 2026-10-21). Confirmed the file name and location, TFRecord of `PredictionLog` records, the 1000-record limit, the supported request types (warmup guide), `PredictLog.request` and `PredictionLog.predict_log` (proto), `enable_model_warmup` default true and `num_request_iterations_for_warmup` used only if > 0 (`server.h`, `main.cc`), and the log message text (`saved_model_warmup_util.cc`). Removed the unconfirmed default of 1 iteration, the `allowed_batch_sizes` claim and the list of lazy components.

Method: documentation only; no commands were run.
