---
id: computing-software.cloud-infrastructure-engineering.knative.requests-limits-queue-proxy
name: requests-limits-queue-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [resources, requests-limits, queue-proxy-resources, queue-sidecar-cpu-request, config-deployment]
level: practitioner
status: docs-checked
description: "Set CPU and memory requests and limits for the user container and the queue-proxy sidecar."
sources:
  - https://knative.dev/docs/serving/services/configure-requests-limits-services/
  - https://knative.dev/docs/serving/configuration/deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size both containers of a Knative Service pod.

User container: set `resources` on the container in the Service template, exactly as in Kubernetes:

```yaml
spec:
  template:
    spec:
      containers:
        - image: docker.io/user/example-app
          resources:
            requests:
              cpu: 100m
              memory: 640M
            limits:
              cpu: 1
```

Queue Proxy: set its requests and limits either globally in the Deployment ConfigMap or per Service with annotations on the template metadata for cpu, memory and ephemeral-storage, for example `queue.sidecar.serving.knative.dev/cpu-resource-request: "1"`, `queue.sidecar.serving.knative.dev/memory-resource-limit: "2Gi"` and `queue.sidecar.serving.knative.dev/ephemeral-storage-resource-request: "400Mi"` (the `-limit` variants follow the same pattern).

The annotation `queue.sidecar.serving.knative.dev/resource-percentage` sizes the Queue Proxy as a percentage of the application container, within bounds (CPU request 25m to 100m, CPU limit 40m to 500m, memory request 50Mi to 200Mi, memory limit 200Mi to 500Mi). It is deprecated and will be removed in future versions, and a specific resource annotation set at the same time takes precedence.

`config-deployment` (namespace `knative-serving`) keys, from the page's example:
- `queue-sidecar-cpu-request`: default `25m` if omitted.
- `queue-sidecar-cpu-limit`, `queue-sidecar-memory-request`, `queue-sidecar-memory-limit`, `queue-sidecar-ephemeral-storage-request`, `queue-sidecar-ephemeral-storage-limit`: if omitted, no value is set and the system default applies. The sample values are `1000m`, `400Mi`, `800Mi`, `512Mi` and `1024Mi`.
- `queue-sidecar-image`: the Go import path of the queue binary that is containerized (`ko://knative.dev/serving/cmd/queue` in the example).
- `registries-skipping-tag-resolving`: repositories where tag to digest resolution is skipped, for example `kind.local,ko.local,dev.local`.
- `digest-resolution-timeout`: maximum time to resolve an image digest, `10s` in the example.

View the live ConfigMap with `kubectl get configmap -n knative-serving config-deployment -oyaml`.

## Checked

2026-11-04. Confirmed against the Configure resource requests and limits page and the Configure Deployment resources page (knative/docs source): the user container `resources` example, the global versus per-Service choice for the Queue Proxy, the six `queue.sidecar.serving.knative.dev/*` annotations, the deprecated `resource-percentage` annotation with its min and max table and the precedence note, and the `config-deployment` keys with the example values, the `25m` default for `queue-sidecar-cpu-request`, the omitted-means-system-default comments, `registries-skipping-tag-resolving`, `digest-resolution-timeout` and the `kubectl get configmap` command. Added the annotation names and the deprecated percentage annotation, listed the Deployment configuration page as a source, and reworded `queue-sidecar-image` to match the page's comment. Nothing removed.

Method: documentation only; no commands were run.
