---
id: computing-software.messaging-and-integration.strimzi.deploy-http-bridge
name: deploy-http-bridge
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [http-bridge, kafkabridge, http-clients]
level: practitioner
status: docs-checked
description: "Deploy the HTTP Bridge so HTTP clients can reach Kafka."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying the HTTP Bridge

**Goal:** expose Kafka to HTTP-based clients with a `KafkaBridge` resource.

The HTTP Bridge provides an API for integrating HTTP clients with a Kafka cluster. The example file is `examples/bridge/kafka-bridge.yaml`. Edit:

- `spec.bootstrapServers`: the Kafka bootstrap address.
- `spec.authentication`: `tls`, `scram-sha-256`, `scram-sha-512`, `plain` or `custom`.
- `spec.tls.trustedCertificates`: use `[]` (empty array) to trust the default Java CAs, or list secrets with certificates.

```bash
kubectl apply -f examples/bridge/kafka-bridge.yaml
kubectl get pods -n my-namespace
```

Output shows pods such as `my-bridge-bridge-<pod_id>`; by default one pod is created and the deployment is successful when STATUS is `Running`.

For local access use port forwarding, which gives `http://localhost:8080`. The docs say port forwarding is suitable only for development and testing.

The bridge service is discoverable inside the cluster: it carries the label `strimzi.io/discovery: "true"` and an annotation listing port `8080`, `protocol: http`, `auth: none`.

**Checklist**

1. Set bootstrap address, auth and trusted certificates.
2. Use `kubectl port-forward` only for testing.
3. Use service discovery labels for in-cluster clients.

## Checked

2026-11-03. Confirmed in the HTTP Bridge section: example file, authentication types, trustedCertificates [] for default Java CAs, port forwarding for testing only, and the strimzi.io/discovery label with port 8080, http, auth none annotation.

Method: documentation only; no commands were run.
