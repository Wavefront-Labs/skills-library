---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.k8sattributes-processor
name: k8sattributes-processor
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, k8sattributes, kubernetes, rbac, metadata]
level: practitioner
status: docs-checked
description: "Enrich telemetry with Kubernetes pod, namespace and node metadata using the k8sattributes processor and RBAC."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/k8sattributesprocessor/README.md
  - https://opentelemetry.io/docs/collector/transforming-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The k8sattributes processor discovers pods through the Kubernetes API, records their IPs, UIDs and metadata, and adds that metadata to spans, metrics and logs as resource attributes. The default block enables it:

```yaml
processors:
  k8sattributes/default:
```

The Collector pod needs RBAC read access to the relevant Kubernetes APIs.

Details from the README:

- Defaults added: `k8s.namespace.name`, `k8s.pod.name`, `k8s.pod.uid`, `k8s.pod.start_time`, `k8s.deployment.name` (derived from the ReplicaSet name by trimming the pod-template-hash) and `k8s.node.name`. Extend the list under `metadata`, and extract pod labels and annotations as tags.
- `pod_association` is a list of rules tried in order until one matches. Each rule has up to 4 `sources`, all of which must match, and duplicates are rejected at validation.
- Source types are `connection` (the incoming connection IP) and `resource_attribute` with a `name` such as `k8s.pod.ip`, or the pair `k8s.pod.name` and `k8s.namespace.name`.
- Without rules, association uses only the connection IP, which fails behind proxies.
- A `connection` source needs the processor to run before batching or tail sampling, which remove that information.
- With several containers in a pod, send `container.id` or `k8s.container.name` to select one.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/k8sattributesprocessor/README.md
- https://opentelemetry.io/docs/collector/transforming-telemetry/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
