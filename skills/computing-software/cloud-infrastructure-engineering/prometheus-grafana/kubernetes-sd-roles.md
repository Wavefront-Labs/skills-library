---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kubernetes-sd-roles
name: kubernetes-sd-roles
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, service-discovery, kubernetes-sd, kubernetes-sd-roles, endpointslice-role, pod-role, node-role, service-role, endpoints-role, ingress-role, kubernetes-sd-configs, meta-labels, namespaces-filter, selectors, attach-metadata, pca]
level: practitioner
status: docs-checked
description: "Pick the right kubernetes_sd role (node, service, pod, endpoints, endpointslice, ingress), the __meta labels each exposes, selectors and attach_metadata."
sources:
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config
  - https://github.com/prometheus/prometheus/blob/main/documentation/examples/prometheus-kubernetes.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubernetes_sd roles

**Goal:** choose the discovery role that yields one target per thing you want to scrape, with the metadata you need for relabeling.

## 1. Role cheat-sheet
| Role | One target per | Address | Key `__meta_kubernetes_*` labels | Typical use |
|---|---|---|---|---|
| `node` | cluster node | first existing node address in the order NodeInternalIP, NodeExternalIP, NodeLegacyHostIP, NodeHostName; Kubelet HTTP port | `node_name`, `node_provider_id`, `node_condition_<type>`, `node_label_<k>`, `node_annotation_<k>`, `node_address_<type>` | kubelet and cAdvisor (the example config scrapes cAdvisor at `/metrics/cadvisor`) |
| `service` | service port of each service | Kubernetes DNS name of the service and port | `service_name`, `service_port_name`, `service_port_number`, `service_port_protocol`, `service_type`, `service_cluster_ip`, `service_label_*`, `service_annotation_*`, `namespace` | blackbox monitoring of a service |
| `pod` | declared port of each container; a port-free target per container if none declared | pod IP and port (pod IP only when no port) | `pod_name`, `pod_ip`, `pod_container_name`, `pod_container_port_name`, `pod_container_port_number`, `pod_container_init`, `pod_ready`, `pod_phase`, `pod_node_name`, `pod_controller_kind`, `pod_label_*`, `pod_annotation_*` | scraping pods directly |
| `endpoints` | endpoint address and port; also extra pod container ports not bound to an endpoint port | endpoint | `endpoints_name`, `endpoint_ready`, `endpoint_port_name`, `endpoint_node_name`; service labels if it belongs to a service; pod labels if pod-backed | classic Service-based scraping; the Endpoints API is deprecated in Kubernetes v1.33+, so use endpointslice |
| `endpointslice` | endpoint address in each EndpointSlice; extra pod ports as for endpoints | endpoint | `endpointslice_name`, `endpointslice_endpoint_conditions_ready`, `_serving`, `_terminating`, `endpointslice_port_name`, `endpointslice_address_target_kind`; service and pod labels | modern replacement for endpoints; needs `discovery.k8s.io/v1` (Kubernetes v1.21+) |
| `ingress` | path of each ingress | host from the ingress spec | `ingress_name`, `ingress_host`, `ingress_path` (default `/`), `ingress_scheme` (https if TLS set, default http), `ingress_class_name` | blackbox monitoring of an ingress; needs `networking.k8s.io/v1` (v1.19+) |

For `node` the `instance` label is set to the node name from the API server.

## 2. Config shape
```yaml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: [prod, staging]        # omit = all namespaces
        selectors:
          - role: pod
            label: "app=example"
            field: "spec.nodeName=<node-name>"
        attach_metadata:
          node: true                    # needs permission to list/watch Nodes
```
- `role` is one of endpoints, endpointslice, service, pod, node, ingress.
- With `api_server` empty, Prometheus assumes it runs in the cluster, discovers API servers automatically and uses the pod's CA certificate and bearer token under `/var/run/secrets/kubernetes.io/serviceaccount/`. `api_server` and `kubeconfig_file` are mutually exclusive. `namespaces` also has `own_namespace`.
- `selectors` filter by label/field, and a selector role must match the role itself, with these exceptions: the endpoints role supports pod, service and endpoints selectors, and the pod role supports node selectors when `attach_metadata.node` is on. Each selector combination adds its own LIST/WATCH, so Prometheus can no longer share a single list/watch across scrape configs. For a small subset of pods in a big cluster, selectors are recommended.
- `attach_metadata` (all default false): `node` is valid for pod, endpoints, endpointslice and needs list/watch on Nodes; `namespace` is valid for pod, endpoints, endpointslice, service, ingress and needs list/watch on Namespaces (enables `namespace_label_*`); `deployment` (pod; needs ReplicaSets) enables `pod_deployment_name`; `job` and `cronjob` (pod; need Jobs) enable `pod_job_name` and `pod_cronjob_name`.
- Label and annotation names have unsupported characters converted to underscores, so `app.kubernetes.io/name` becomes `__meta_kubernetes_pod_label_app_kubernetes_io_name`; `labelpresent_*` variants are `true` for each label present.

## 3. Phase and init containers
`pod_phase` is Pending, Running, Succeeded, Failed or Unknown. To skip finished pods:
```yaml
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_phase]
        regex: Pending|Succeeded|Failed|Unknown
        action: drop
```
`pod_container_init` is `true` for init containers; the pod role includes their ports, so drop those with the same pattern.

## Gotchas
- The pod role makes one target per declared container port, so a pod with several ports yields several targets; keep the one you want by matching `pod_container_port_name`.
- The service role is meant for blackbox monitoring; the address is the service DNS name, not individual pods.
- Narrow with `namespaces.names` or `selectors` when many Prometheus servers would otherwise watch everything.

## Verify
- [ ] The Prometheus service-discovery page shows the expected number of targets per job.
- [ ] After relabeling, a pod with two declared ports yields exactly one active target.

## Checked
Checked 2026-11-08 against the Prometheus configuration reference (kubernetes_sd_config: roles, meta labels, API access, selectors, attach_metadata) and the example prometheus-kubernetes.yml. Removed because the pages do not state them: kubelet port 10250, a per-role RBAC verb table, "forbidden" log behaviour, the claim that endpointslice is required above 1000 endpoints and that Endpoints are truncated, scale-to-zero timing, and the `$(NODE_NAME)` field selector value.

Method: docs-only read of cited pages, 2026-11-08
