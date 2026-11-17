---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-operator-and-kubernetes-telemetry
name: opentelemetry-operator-and-kubernetes-telemetry
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, kubernetes, otel-operator, opentelemetry-operator, opentelemetrycollector-crd, instrumentation-crd, auto-instrumentation-injection, target-allocator, prometheus-receiver, servicemonitor, podmonitor, k8sattributes, kubeletstats, k8s-cluster-receiver, k8sobjects-receiver, k8s-events, hostmetrics, otel-helm-chart, kube-stack-chart, daemonset-mode, sidecar-mode, statefulset-mode, cert-manager, rbac, kubernetes-telemetry]
level: advanced
status: docs-checked
description: "Run OpenTelemetry on Kubernetes with the Operator: OpenTelemetryCollector CRs in four modes, and Instrumentation CRs that inject language agents by annotation."
sources: ["https://opentelemetry.io/docs/platforms/kubernetes/operator/", "https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/", "https://opentelemetry.io/docs/platforms/kubernetes/operator/target-allocator/", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md", "https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-operator", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kubeletstatsreceiver", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sobjectsreceiver", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sclusterreceiver"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenTelemetry Operator and Kubernetes telemetry

**Goal:** Collectors and auto-instrumentation managed as Kubernetes objects, Prometheus
scraping sharded automatically, and the standard Kubernetes signals (kubelet, cluster
state, events, host metrics) flowing with proper `k8s.*` resource attributes.

## 1. Install
```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
# cert-manager required for the admission webhooks (or set admissionWebhooks.certManager.enabled=false + autoGenerateCert)
helm upgrade --install opentelemetry-operator open-telemetry/opentelemetry-operator -n opentelemetry-operator-system --create-namespace \
  --set manager.collectorImage.repository=otel/opentelemetry-collector-contrib \
  --set admissionWebhooks.certManager.enabled=true
# alternative one-shot: open-telemetry/opentelemetry-kube-stack (operator + collectors + instrumentation + dashboards)
```
Pin the chart version and the collector image together so the image matches your tested config. The chart README also documents certificate options: cert-manager, `admissionWebhooks.autoGenerateCert.enabled=true` with cert-manager off, or your own cert files.

## 2. OpenTelemetryCollector CR
```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: { name: agent, namespace: observability }
spec:
  mode: daemonset                     # deployment | daemonset | sidecar | statefulset
  image: otel/opentelemetry-collector-contrib:<VERSION>
  serviceAccount: otel-agent          # with the RBAC below
  hostNetwork: false
  env:
    - { name: K8S_NODE_NAME, valueFrom: { fieldRef: { fieldPath: spec.nodeName } } }
    - { name: K8S_NODE_IP,   valueFrom: { fieldRef: { fieldPath: status.hostIP } } }
  resources: { requests: { cpu: 100m, memory: 256Mi }, limits: { memory: 512Mi } }
  volumeMounts: [{ name: varlogpods, mountPath: /var/log/pods, readOnly: true }]
  volumes: [{ name: varlogpods, hostPath: { path: /var/log/pods } }]
  ports: [{ name: otlp-grpc, port: 4317, hostPort: 4317 }]
  config:
    receivers:
      otlp: { protocols: { grpc: { endpoint: 0.0.0.0:4317 }, http: { endpoint: 0.0.0.0:4318 } } }
      kubeletstats:
        collection_interval: 30s
        auth_type: serviceAccount
        endpoint: https://${env:K8S_NODE_IP}:10250
        insecure_skip_verify: true
        metric_groups: [node, pod, container, volume]
        extra_metadata_labels: [container.id]
      hostmetrics: { root_path: /hostfs, collection_interval: 30s, scrapers: { cpu: {}, memory: {}, filesystem: {}, network: {}, load: {} } }
      filelog: { include: [/var/log/pods/*/*/*.log], operators: [{ type: container }] }
    processors:
      memory_limiter: { check_interval: 1s, limit_percentage: 80, spike_limit_percentage: 20 }
      k8sattributes:
        auth_type: serviceAccount
        passthrough: false
        filter: { node_from_env_var: K8S_NODE_NAME }        # only this node's pods → small cache
        extract:
          metadata: [k8s.namespace.name, k8s.pod.name, k8s.pod.uid, k8s.deployment.name, k8s.statefulset.name, k8s.daemonset.name, k8s.job.name, k8s.node.name, k8s.container.name, container.image.name, container.image.tag]
          labels: [{ tag_name: app, key: app.kubernetes.io/name, from: pod }, { tag_name: team, key: team, from: namespace }]
        pod_association:
          - sources: [{ from: resource_attribute, name: k8s.pod.ip }]
          - sources: [{ from: resource_attribute, name: k8s.pod.uid }]
          - sources: [{ from: connection }]                   # match by source IP of the OTLP connection
      resourcedetection: { detectors: [env, system, eks, gcp, azure], timeout: 5s }
      batch: {}
    exporters:
      otlp/gateway: { endpoint: gateway-collector.observability:4317, tls: { insecure: true }, sending_queue: { enabled: true }, retry_on_failure: { enabled: true } }
    service:
      pipelines:
        traces:  { receivers: [otlp], processors: [memory_limiter, k8sattributes, resourcedetection, batch], exporters: [otlp/gateway] }
        metrics: { receivers: [otlp, kubeletstats, hostmetrics], processors: [memory_limiter, k8sattributes, resourcedetection, batch], exporters: [otlp/gateway] }
        logs:    { receivers: [otlp, filelog], processors: [memory_limiter, k8sattributes, resourcedetection, batch], exporters: [otlp/gateway] }
```
A second CR `mode: deployment` (gateway, `replicas: 3`, `autoscaler: { minReplicas: 2, maxReplicas: 10, targetCPUUtilization: 70 }`)
holds `k8s_cluster` (cluster-wide state such as `k8s.deployment.desired` and `k8s.deployment.available`; the README says a **single** instance should run, or several with its `k8s_leader_elector` extension),
`k8sobjects` (events: `objects: [{ name: events, mode: watch }]`), tail sampling, and backend exporters.
The Operator creates Service(s), ConfigMap, ServiceAccount (if unset), and reconciles on CR change
(`kubectl get opentelemetrycollectors -A`).

RBAC for the agent/gateway ServiceAccounts: `pods`, `namespaces`, `nodes`, `replicasets`,
`events` get/list/watch; `nodes/stats`, `nodes/proxy` get for kubeletstats; `k8s_cluster` needs
most core resources list/watch.

## 3. Auto-instrumentation with the Instrumentation CR
```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata: { name: default, namespace: observability }
spec:
  exporter: { endpoint: http://$(OTEL_K8S_NODE_IP):4317 }   # or the agent Service; for http/protobuf use :4318
  propagators: [tracecontext, baggage]
  sampler: { type: parentbased_traceidratio, argument: "0.25" }
  resource: { addK8sUIDAttributes: true }
  env: [{ name: OTEL_K8S_NODE_IP, valueFrom: { fieldRef: { fieldPath: status.hostIP } } }]
  java:   { image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-java:<VERSION>, env: [{ name: OTEL_INSTRUMENTATION_KAFKA_ENABLED, value: "true" }], resources: { limits: { memory: 64Mi } } }
  python: { image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-python:<VERSION>, env: [{ name: OTEL_EXPORTER_OTLP_PROTOCOL, value: http/protobuf }, { name: OTEL_EXPORTER_OTLP_ENDPOINT, value: http://$(OTEL_K8S_NODE_IP):4318 }] }
  nodejs: { image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-nodejs:<VERSION> }
  dotnet: { image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-dotnet:<VERSION> }
  go:     { image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-go:<VERSION> }   # eBPF sidecar: needs privileged + feature gate
```
Enable per workload with pod annotations (in `spec.template.metadata.annotations`):
`instrumentation.opentelemetry.io/inject-java: "true"` (default CR in the namespace; or `"my-instrumentation"`,
`"other-namespace/my-instrumentation"` to name the CR; `"false"` to opt out), `inject-python`, `inject-nodejs`,
`inject-dotnet`, `inject-go` (plus `instrumentation.opentelemetry.io/otel-go-auto-target-exe`, which sets
`OTEL_GO_AUTO_TARGET_EXE`), and `instrumentation.opentelemetry.io/container-names: "app"` (comma-separated) for
multi-container pods; per-language `<lang>-container-names` annotations exist too. Go does not support
multi-container pods. The annotation can also go on a namespace. Pods must be **recreated** after annotating.
`service.name` is taken from the `resource.opentelemetry.io/service.name` pod annotation, then (with
`defaults.useLabelsForResourceAttributes: true`) the `app.kubernetes.io/name` label, then `k8s.deployment.name`,
`k8s.replicaset.name`, and so on; `OTEL_SERVICE_NAME` or `OTEL_RESOURCE_ATTRIBUTES` env vars win over all of them.

## 4. Target allocator: sharded Prometheus scraping
```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: { name: prom-scraper }
spec:
  mode: statefulset
  replicas: 3
  targetAllocator:
    enabled: true
    serviceAccount: otel-targetallocator
    allocationStrategy: consistent-hashing     # least-weighted | consistent-hashing (default) | per-node
    prometheusCR:
      enabled: true                            # consume ServiceMonitor/PodMonitor/ScrapeConfig/Probe CRs
      serviceMonitorSelector: {}
      podMonitorSelector: {}
      scrapeInterval: 30s
  config:
    receivers:
      prometheus:
        config:
          scrape_configs:
            - job_name: kube-state-metrics
              static_configs: [{ targets: ["kube-state-metrics.kube-system:8080"] }]
    exporters: { prometheusremotewrite: { endpoint: http://mimir/api/v1/push, headers: { X-Scope-OrgID: platform } } }
    service: { pipelines: { metrics: { receivers: [prometheus], processors: [memory_limiter, batch], exporters: [prometheusremotewrite] } } }
```
The allocator discovers targets (from `scrape_configs` and Prometheus Operator CRs), splits
them across the collector replicas, and each replica fetches its share via
`http://<ta>/jobs/<job>/targets?collector_id=<pod>`. The Operator rewrites the receiver's `scrape_configs` to use
`http_sd_configs` pointing at that endpoint and drops other service-discovery settings such as `static_configs`.
The allocator needs the same RBAC as Prometheus service discovery plus the `monitoring.coreos.com` CRDs installed for
`prometheusCR`. The `per-node` strategy suits a DaemonSet collector, but it ignores targets without a Node, such as
control plane components.

## 5. The Kubernetes signal set
| Signal | Receiver / processor | Deploy on |
|---|---|---|
| container/pod/node CPU, memory, fs, net (from kubelet) | `kubeletstats` | daemonset |
| host CPU/mem/disk/net | `hostmetrics` (mount `/` at `/hostfs`) | daemonset |
| cluster state (desired vs available, phases, conditions, quotas) | `k8s_cluster` | single deployment |
| kube-state-metrics / cAdvisor / node-exporter scrape | `prometheus` receiver + target allocator | statefulset / daemonset per-node |
| events | `k8sobjects` (`events`, mode watch) → logs pipeline | single deployment |
| container logs | `filelog` with `container` operator | daemonset |
| enrichment of everything | `k8sattributes` (+ `resourcedetection`) | every pipeline |
| app traces/metrics/logs | `otlp` receiver, apps point at node IP:4317 | daemonset |
Use semconv `k8s.*` attribute names end to end; Loki/Mimir/Tempo and vendors key off them.

## Gotchas
- The admission webhook needs a certificate (cert-manager, the chart's auto-generated cert, or your own); without one the Operator's CRs are rejected.
- Injection happens at pod **creation**; `kubectl rollout restart` after adding annotations.
- `k8sattributes` without `node_from_env_var` filter on a DaemonSet watches **all** pods on every node: memory × nodes.
- Check `/jobs` on the allocator to see what it rendered before trusting a Prometheus feature to carry over.
- `k8s_cluster` and `k8sobjects` must run as one replica (or use `k8s_leader_elector`), otherwise they produce duplicated data; `k8sobjects` supports a `storage` extension so watch mode resumes from its persisted resourceVersion instead of duplicating events after a restart.
- CR config is YAML inside a CR; the Operator validates structure on admission but not component correctness—test with `otelcol validate` locally first.

## Verify
- [ ] `kubectl get otelcol -A` shows the CRs with the expected mode/replicas; agent pods on every node (`kubectl get ds -n observability`).
- [ ] A pod annotated `inject-java` has the injected init container (`kubectl describe pod`), and its traces appear with `k8s.deployment.name`.
- [ ] Target allocator `/jobs` lists your ServiceMonitors, and `/jobs/<job>/targets?collector_id=prom-scraper-0` returns a subset; `up` series arrive in Mimir from all replicas.
- [ ] `kubeletstats` metrics (`k8s.pod.cpu.usage`/`container.memory.working_set`) and cluster-state metrics (`k8s.deployment.available`) are visible with `k8s.namespace.name` attributes.

## Checked

2026-10-31. Confirmed against the OpenTelemetry Operator docs (automatic instrumentation, target allocator), the Operator CRD API reference (`allocationStrategy` enum and default, autoscaler `targetCPUUtilization`), the operator Helm chart README and values (`admissionWebhooks.certManager`, `autoGenerateCert`, `manager.collectorImage.repository`), and the READMEs and metric docs of `k8sattributes`, `kubeletstats`, `k8s_cluster` and `k8sobjects`.
Removed: pinned image and collector versions (now `<VERSION>`), the unverified `JAVA_TOOL_OPTIONS`/`PYTHONPATH`/`NODE_OPTIONS` list, the Java startup and memory figures, the `relabel` claim, the `failed calling webhook` message, and the non-existent metric name `k8s.pod.cpu.utilization`.
Method: documentation only; no commands were run.
