---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-k6-load-tests
name: performance-k6-load-tests
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, k6, load-testing, benchmarking, make-targets, k6-sa-key, tests-k6]
level: practitioner
status: docs-checked
description: "Run k6 load tests against Seldon Core 2 from inside the cluster: make targets for envoy, agent, server, pipeline and model gateways, results, k6 args and env variables."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tests.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# k6 performance tests for Seldon Core 2

The repo ships k6 scenarios under `tests/k6` to find the limits of a deployment. k6 drives load, unload and infer workloads. Run it inside the same cluster as Core 2: it needs internal access to services not exposed outside, and being in-cluster keeps link latency low so inference latencies reflect system overhead.

## Tests and make targets
- Envoy, synchronous inference via envoy: `make deploy-envoy-test`
- Agent, requests direct to a specific agent (default triton-0 or mlserver-0): `make deploy-rproxy-test` or `make deploy-rproxy-mlserver-test`
- Server, direct to a server and bypassing the agent: `make deploy-server-test` or `make deploy-server-mlserver-test`
- Pipeline gateway (HTTP-Kafka), HTTP and gRPC to a one-node pipeline: `make deploy-kpipeline-test`
- Model gateway (Kafka-HTTP), requests to a model via Kafka: `make deploy-kmodel-test`

## Results
Read the log of the pod that ran the Kubernetes job. Results can also go to a gs bucket if a service account secret `k6-sa-key` exists in the same namespace. Prometheus metrics are visible while the test runs.

## Changing the scenario
Edit `tests/k6/configs/k8s/base/k6.yaml`; it applies to all later deployed tests. To change the scenario code, `export DOCKERHUB_USERNAME=<account>`, run `make build-push`, and deploy jobs from the same shell so they use your image.

Settings:
- k6 `args`, for example `-u 5 -i 100000 -d 120m` with `scenarios/infer_constant_vu.js`; alternatives include `infer_constant_rate.js`, `k8s-test-script.js` and `core2_qa_control_plane_ops.js`.
- Environment variables such as `INFER_HTTP_ITERATIONS`, `INFER_GRPC_ITERATIONS`, `MODELNAME_PREFIX`, `MODEL_TYPE`, `MODEL_MEMORY_BYTES`, `MAX_NUM_MODELS`, `INFER_BATCH_SIZE` and `WARMUP`.
- Give `MODEL_MEMORY_BYTES` with unit suffixes (k, M, G, T). Bare numbers make the operator take field ownership, so the next model create or update fails.
- `MODEL_TYPE` values include tfsimple, tfsimple_string, iris, pytorch_cifar10, tfmnist, tfresnet152, onnx_gpt2, mlflow_wine, add10 and sentiment.

## Checked

2026-11-04. Confirmed against performance-tests.md (Seldon Core 2 docs, v2 branch): make targets, k6-sa-key, build-push, k6 args, environment variables, MODEL_TYPE list, MODEL_MEMORY_BYTES unit note. Removed or corrected: nothing.

Method: documentation only; no commands were run.
