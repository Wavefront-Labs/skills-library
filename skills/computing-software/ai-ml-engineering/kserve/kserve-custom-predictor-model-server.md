---
id: computing-software.ai-ml-engineering.kserve.kserve-custom-predictor-model-server
name: kserve-custom-predictor-model-server
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [custom-predictor, modelserver, kserve-model, preprocess, predict, postprocess, load, buildpacks, pack, infer-request, workers, http-port, grpc-port, enable-grpc, max-asyncio-workers, storage-uri, protocol, kserve-loglevel]
level: advanced
status: docs-checked
description: "Write a custom Python model server with the KServe Model API: handler order, ready flag, REST and gRPC, pack buildpacks build, container args and env vars."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/custom-predictor/custom-predictor.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom predictor (Python ModelServer)

Subclass `kserve.Model`. Handlers run in order `preprocess` -> `predict` -> `postprocess`; `load` loads weights (call it in `__init__`) and must set `self.ready = True`, which feeds the readiness probe. Start with `ModelServer().start([model])`; build the arg parser from `kserve.model_server.parser`. Pass `return_response_headers=True` to `super().__init__` to add response headers on V1 and V2. REST models take a dict payload (V1); for the Open (V2) Inference Protocol take `InferRequest` and return `InferResponse`.

## Build
Buildpacks, no Dockerfile: `pack build --builder=heroku/builder:24 ${DOCKER_USER}/custom-model:v1`. Needs `requirements.txt`, a `Procfile` and a `.python-version`. Test with `docker run -ePORT=8080 -p8080:8080 IMAGE`.

## Deploy
```yaml
spec:
  predictor:
    containers:
      - name: kserve-container
        image: ${DOCKER_USER}/custom-model:v1
        args: [--workers=1, --http_port=8080, --model_name=custom-model]
```
For gRPC expose one port in `ports` (only one port can be exposed; HTTP is default) and use gRPC port 8081.

## Server args
`--workers` (uvicorn processes, default 1), `--http_port` (8080), `--grpc_port` (8081), `--max_threads` (4), `--enable_grpc` (true), `--grpc_max_send_message_length` and `--grpc_max_receive_message_length` (8388608), `--model_name` (default is the service name), `--max_asyncio_workers` (`min(32, cpu.limit + 4)`), `--enable_latency_logging` (true), `--configure_logging` (true), `--log_config_file`, `--access_log_format`, `--enable_docs_url` (Swagger at `/docs`), `--event_loop` (`auto`, `asyncio`, `uvloop`).

## Env vars
`STORAGE_URI` (same as `storageUri`, data at `/mnt/models`), `PROTOCOL` (like `protocolVersion`), `KSERVE_LOGLEVEL` (default INFO).

## Checked
Confirmed against the KServe custom predictor page: handler order and load or ready behaviour, pack build command and Buildpacks file requirements, InferenceService container args, every server argument default listed, env vars, and the single gRPC port rule. The page also covers Ray Serve parallel inference and logger configuration, which this skill does not summarise.

Method: docs-only read of cited pages, 2026-11-08
