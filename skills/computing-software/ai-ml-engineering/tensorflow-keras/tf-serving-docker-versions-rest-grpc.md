---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-serving-docker-versions-rest-grpc
name: tf-serving-docker-versions-rest-grpc
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, tensorflow-serving, tf-serving-docker, savedmodel, model-versioning, rest-api, grpc, model-config-file]
level: practitioner
status: docs-checked
description: "Serve SavedModels with the TF Serving Docker image: version directories, model_config_file with version labels, REST and gRPC requests, batching and GPU image."
sources:
  - https://www.tensorflow.org/tfx/serving/docker
  - https://www.tensorflow.org/tfx/serving/serving_config
  - https://www.tensorflow.org/tfx/serving/api_rest
  - https://github.com/tensorflow/serving/blob/master/tensorflow_serving/g3doc/docker.md
  - https://github.com/tensorflow/serving/blob/master/tensorflow_serving/model_servers/main.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TF Serving with Docker: versions, REST and gRPC

**Goal:** run a production TF Serving container that hot-loads new model versions and serves REST and gRPC.

## Directory layout
```
/models/churn/
  1/saved_model.pb  variables/
  2/saved_model.pb  variables/
```
Each version is a numbered subdirectory. By default TF Serving serves the version with the largest number and polls the filesystem for new versions (`--file_system_poll_wait_seconds`).

Inspect signatures before serving:
```bash
saved_model_cli show --dir /models/churn/2 --tag_set serve --signature_def serving_default
```

## Run
```bash
docker run -d --name tfs -p 8500:8500 -p 8501:8501 \
  --mount type=bind,source=/srv/models/churn,target=/models/churn \
  -e MODEL_NAME=churn tensorflow/serving
# GPU: tensorflow/serving:latest-gpu with --gpus all
```
8500 = gRPC, 8501 = REST. The image reads the model from `${MODEL_BASE_PATH}/${MODEL_NAME}` (default base path `/models`).

## REST
```bash
curl -s localhost:8501/v1/models/churn                                  # status of versions
curl -s -X POST localhost:8501/v1/models/churn:predict \
  -d '{"signature_name":"serving_default","instances":[{"age":42,"plan":"pro"}]}'
curl -s -X POST localhost:8501/v1/models/churn/versions/1:predict -d '{"instances":[...]}'
curl -s localhost:8501/v1/models/churn/metadata                         # signatures
```
`instances` is row format; `inputs` is columnar, for named inputs whose 0-th dimensions differ.

## Multiple models, pinned versions, labels
`models.config`:
```
model_config_list {
  config {
    name: "churn"  base_path: "/models/churn"  model_platform: "tensorflow"
    model_version_policy { specific { versions: 1 versions: 2 } }
    version_labels { key: "stable" value: 1 }
    version_labels { key: "canary" value: 2 }
  }
}
```
Run with `--model_config_file=/models/models.config --model_config_file_poll_wait_seconds=60`. Call `/v1/models/churn/labels/canary:predict`. Labels can only be assigned to versions that are already loaded; `--allow_version_labels_for_unavailable_models` allows new labels on versions not yet loaded.

## Batching and performance
`--enable_batching --batching_parameters_file=/models/batching.config` with `max_batch_size`, `batch_timeout_micros` and `num_batch_threads` (for example `max_batch_size { value: 128 }`). Tune `batch_timeout_micros` against your latency budget.

## Gotchas
- A preprocessing step not in the SavedModel must be duplicated by clients; prefer exporting preprocessing in the graph.
- Health checks: `GET /v1/models/<name>` returning `AVAILABLE` for the expected version.

## Verify
- [ ] Both versions show `AVAILABLE` and labels route correctly.
- [ ] REST and gRPC return identical predictions for the same input.
- [ ] Load test with batching on shows target p99 latency.

## Checked

Checked 2026-10-25 against tensorflow/serving master (last commit 2026-10-21). Confirmed ports 8500 (gRPC) and 8501 (REST), `MODEL_NAME` and the default model base path, the `latest-gpu` image with `--gpus all` (Docker guide), `model_version_policy { specific { versions: ... } }` with `version_labels`, the loaded-versions rule for labels and `--allow_version_labels_for_unavailable_models`, `--model_config_file` and `--model_config_file_poll_wait_seconds` (serving config guide and `main.cc`), `--enable_batching`, `--batching_parameters_file` and the three batching parameter names, the `:predict`, `/versions/N`, `/labels/L` and `/metadata` REST paths, row (`instances`) versus columnar (`inputs`) formats and the `AVAILABLE` state (REST API guide). Removed the pinned image version, the non-atomic copy advice and the unconfirmed performance claims.

Method: documentation only; no commands were run.
