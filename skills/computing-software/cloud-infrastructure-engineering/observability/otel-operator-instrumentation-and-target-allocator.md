---
id: computing-software.cloud-infrastructure-engineering.observability.otel-operator-instrumentation-and-target-allocator
name: otel-operator-instrumentation-and-target-allocator
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [otel-operator, instrumentation-crd-config, inject-annotations, target-allocator-config, allocation-strategy, prometheus-cr-discovery, k8sattributes-config, pod-association, k8s-metadata-enrichment, kubeletstats-receiver-config, k8s-cluster-receiver-config, opentelemetrycollector-crd-modes]
level: advanced
status: docs-checked
description: "OpenTelemetry Operator: Instrumentation CRD injection, collector CRD modes, target allocator with ServiceMonitors, k8sattributes and kubelet/cluster receivers."
sources: ["https://opentelemetry.io/docs/kubernetes/operator/", "https://opentelemetry.io/docs/kubernetes/operator/automatic/", "https://opentelemetry.io/docs/kubernetes/operator/target-allocator/", "https://opentelemetry.io/docs/kubernetes/collector/components/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTel Operator: instrumentation, target allocator, k8s components

## Instrumentation CRD
```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata: {name: default, namespace: apps}
spec:
  exporter: {endpoint: http://otel-agent.monitoring:4318}
  propagators: [tracecontext, baggage]
  sampler: {type: parentbased_traceidratio, argument: "0.2"}
  resource: {addK8sUIDAttributes: true}
  java: {env: [{name: OTEL_INSTRUMENTATION_JDBC_ENABLED, value: "true"}]}
  python: {env: [{name: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED, value: "true"}]}
```
Pod template annotations: `instrumentation.opentelemetry.io/inject-java: "true"` (or `inject-python`,
`inject-nodejs`, `inject-dotnet`, `inject-go` with `otel-go-auto-target-exe`); the operator docs describe how to select a specific CR. Restart deployments after adding the annotation. Multi-container
pods: `instrumentation.opentelemetry.io/container-names`.

## OpenTelemetryCollector CRD modes
`mode: deployment` (gateway), `daemonset` (node agent: logs, kubeletstats, hostmetrics), `statefulset` (target
allocator, persistent queues), `sidecar` (injected with `sidecar.opentelemetry.io/inject: "true"`).
`spec.upgradeStrategy` controls operator-managed upgrades; the collector CRD apiVersion is `opentelemetry.io/v1beta1`.

## Target allocator
```yaml
spec:
  mode: statefulset
  replicas: 3
  targetAllocator:
    enabled: true
    prometheusCR: {enabled: true, serviceMonitorSelector: {}, podMonitorSelector: {}}
  config:
    receivers:
      prometheus: {config: {scrape_configs: []}}   # filled by the allocator
```
Distributes Prometheus scrape targets across the cluster of collectors. Targets are served at `/jobs/<job>/targets` on the allocator service.

## Kubernetes components
```yaml
processors:
  k8sattributes:
    auth_type: serviceAccount
    passthrough: false
    pod_association:
      - sources: [{from: resource_attribute, name: k8s.pod.ip}]
      - sources: [{from: resource_attribute, name: k8s.pod.uid}]
      - sources: [{from: connection}]
    extract:
      metadata: [k8s.namespace.name, k8s.pod.name, k8s.deployment.name, k8s.node.name, container.image.tag]
      labels: [{tag_name: team, key: team, from: namespace}]
    filter: {node_from_env_var: K8S_NODE_NAME}     # DaemonSet: only watch local pods
receivers:
  kubeletstats: {collection_interval: 30s, auth_type: serviceAccount, insecure_skip_verify: true, metric_groups: [pod, container, node]}
  k8s_cluster: {collection_interval: 30s, node_conditions_to_report: [Ready, MemoryPressure]}  
```

## Verify
- [ ] Injected pods have the init container and `OTEL_*` env; traces appear with k8s attributes.
- [ ] Allocator shows targets assigned across the collectors.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Operator auto-instrumentation, target-allocator and Kubernetes collector component pages, the operator README and the k8sattributes processor README (main, 2026-10).
- Confirmed: Instrumentation `exporter.endpoint`, `parentbased_traceidratio` sampler type, `addK8sUIDAttributes`, inject annotations, `container-names`, collector modes (`deployment`, `daemonset`, `statefulset`, `sidecar`), `sidecar.opentelemetry.io/inject`, `upgradeStrategy`, `pod_association`, `node_from_env_var`, `passthrough`, `tag_name` labels, kubeletstats `metric_groups` and `insecure_skip_verify`, `node_conditions_to_report`, `/jobs/<job>/targets`.
- Removed (unconfirmed): `allocationStrategy` values, RBAC statement, kubelet port, single-replica and connection-association claims, CR migration claim.
Method: documentation only; no commands were run.
