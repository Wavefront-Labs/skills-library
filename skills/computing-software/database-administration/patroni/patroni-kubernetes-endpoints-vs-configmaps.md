---
id: computing-software.database-administration.patroni.patroni-kubernetes-endpoints-vs-configmaps
name: patroni-kubernetes-endpoints-vs-configmaps
category: computing-software
field: database-administration
product: patroni
tags: [patroni, kubernetes, endpoints, configmap, leader-election]
level: practitioner
status: docs-checked
description: "Choose Endpoints or ConfigMaps for Patroni's Kubernetes DCS and configure related keys."
sources:
  - https://patroni.readthedocs.io/en/latest/kubernetes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Patroni on Kubernetes without a separate etcd.

Patroni can store cluster state and the leader key in Kubernetes objects, chosen by `kubernetes.use_endpoints` (or `PATRONI_KUBERNETES_USE_ENDPOINTS`).

- Endpoints: recommended, but off by default for compatibility. Configuration and leader key live in the Endpoints' metadata annotations. Changing leader is safer because the annotations and the actual addresses to the leader pod update in one go.
- ConfigMaps: Patroni creates ConfigMaps and keeps keys in their metadata. A leader change needs at least two updates (the ConfigMap, then the Endpoint). Direct traffic using a Service with a label selector on the `role_label`. Sometimes, for instance on OpenShift, ConfigMaps are the only option.

Settings in the `kubernetes` section:
- `namespace` (default `default`), `labels` (used to find and tag objects), `scope_label` (default `cluster-name`).
- `pod_ip`: required when `use_endpoints` is enabled; populates the leader Endpoint subsets on promotion.
- `ports`: if the Service names a port, the Endpoint must have the same name, for example `[{"name": "postgresql", "port": 5432}]`; used only with `use_endpoints`.
- `bypass_api_service`: resolve API nodes behind the service and connect directly.
- `cacert`, and `retriable_http_codes` (default retries on 500, 503, 504, or a retry-after header).

Release 4.1.1 retries the leader update within `retry_timeout` on a temporary Kubernetes 403.

## Checked

2026-11-03. Confirmed against the Kubernetes page and YAML Configuration Settings (kubernetes section): use_endpoints, pod_ip, ports, labels, scope_label, bypass_api_service, retriable_http_codes; release 4.1.1 note.

Method: documentation only; no commands were run.
