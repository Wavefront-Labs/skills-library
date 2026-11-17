---
id: computing-software.ai-ml-engineering.seldon-core-2.inference-endpoints-and-sync-requests
name: inference-endpoints-and-sync-requests
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, inference, rest, grpc, curl, grpcurl, tritonclient, seldon-mesh-service, port-forward, envoy-data-port]
level: practitioner
status: docs-checked
description: "Send synchronous inference to Seldon Core 2: find the seldon-mesh Service or Compose port 9000, then call a model with the seldon CLI, curl, grpcurl or Python tritonclient."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/inference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Synchronous inference requests

Requests can be synchronous over REST or gRPC, or asynchronous through Kafka. REST payloads are JSON v2 protocol, while gRPC and Kafka payloads must be Protobuf v2 protocol.

## Find the endpoint
- Docker Compose: ports are on the host, so use `0.0.0.0:9000`. The port is set by the `ENVOY_DATA_PORT` environment variable.
- Kubernetes: Seldon creates a single Service `seldon-mesh` in its namespace (default `seldon-mesh`). With a load balancer:

```bash
kubectl get svc seldon-mesh -n seldon-mesh -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Without one, port-forward for development and send requests to `localhost:8080`:

```bash
kubectl port-forward svc/seldon-mesh -n seldon-mesh 8080:80
```

With Istio or Ambassador use the ingress IP of the mesh instead.

## Calling a model named iris
```bash
seldon model infer iris --inference-mode grpc \
   "{\"model_name\":\"iris\",\"inputs\":[{\"name\":\"input\",\"contents\":{\"fp32_contents\":[1,2,3,4]},\"datatype\":\"FP32\",\"shape\":[1,4]}]}"

curl -v http://0.0.0.0:9000/v2/models/iris/infer \
   -H "Content-Type: application/json" \
   -d @request.json
```

The `seldon model infer` default mode is REST. With grpcurl use `-plaintext -import-path apis -proto apis/mlops/v2_dataplane/v2_dataplane.proto` and the method `inference.GRPCInferenceService/ModelInfer`. The Python `tritonclient.http` `InferenceServerClient` also works with `client.infer("iris", inputs)`.

A pipeline can be called synchronously only if its spec has an output section.

## Checked

Confirmed against the Inference page: REST JSON versus gRPC and Kafka Protobuf payloads, the Docker Compose port 9000 and ENVOY_DATA_PORT, the seldon-mesh Service, the load balancer and port-forward commands, seldon model infer default REST mode, the grpcurl proto path and method, the tritonclient example, and the pipeline output requirement. Quoted the jsonpath argument as the page does.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb inference.md page (raw markdown).
