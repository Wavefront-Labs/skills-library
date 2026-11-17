---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kube-prometheus-stack-and-operator-crds
name: kube-prometheus-stack-and-operator-crds
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, kubernetes, prometheus-operator, kube-prometheus-stack, kube-prometheus, servicemonitor, podmonitor, prometheusrule, scrapeconfig, probe, alertmanagerconfig, kube-state-metrics, cadvisor, kubelet-metrics, node-exporter, helm, label-selectors, servicemonitorselector, ruleselector, additional-scrape-configs, shards, pca]
level: advanced
status: docs-checked
description: "Run Prometheus on Kubernetes via the Operator: install kube-prometheus-stack, get ServiceMonitor, PodMonitor and PrometheusRule picked up, tame kube-state-metrics volume."
sources: ["https://prometheus-operator.dev/docs/", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack", "https://github.com/kubernetes/kube-state-metrics/tree/main/docs", "https://prometheus-operator.dev/docs/developer/getting-started/", "https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/platform/high-availability/", "https://prometheus-operator.dev/docs/developer/scrapeconfig/", "https://prometheus-operator.dev/docs/api-reference/api/", "https://github.com/prometheus/node_exporter"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# kube-prometheus-stack and Operator CRDs

**Goal:** a cluster where adding a `ServiceMonitor` next to a Deployment is all a team does
to be scraped and alerted, and nothing in `prometheus.yml` is hand-written.

## 1. Install
The chart is distributed as an OCI artifact and through the Helm repository
`https://prometheus-community.github.io/helm-charts` (chart `kube-prometheus-stack`). Prerequisites per the
README: Kubernetes 1.19+ and Helm 3+.
```bash
helm install kps oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack -n monitoring --create-namespace -f values.yaml
helm show values oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack   # every option, with comments
```
Key `values.yaml` decisions (all keys appear in the chart's `values.yaml`):
```yaml
prometheus:
  prometheusSpec:
    retention: 15d              # chart default 10d
    retentionSize: 45GB         # chart default ""
    storageSpec: { volumeClaimTemplate: { spec: { storageClassName: fast, resources: { requests: { storage: 50Gi } } } } }
    resources: { requests: { memory: 4Gi, cpu: 1 }, limits: { memory: 6Gi } }
    externalLabels: { cluster: prod-eu1 }
    replicas: 2
    podAntiAffinity: hard
    # By default the chart selects only ServiceMonitors/PodMonitors labelled with the release tag.
    serviceMonitorSelectorNilUsesHelmValues: false   # select ALL ServiceMonitors
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false
    probeSelectorNilUsesHelmValues: false
    scrapeConfigSelectorNilUsesHelmValues: false
    serviceMonitorNamespaceSelector: {}              # all namespaces
    remoteWrite: [{ url: "https://mimir.example.com/api/v1/push" }]
alertmanager:
  alertmanagerSpec: { replicas: 3 }   # alertmanagerConfigSelector / alertmanagerConfigNamespaceSelector pick AlertmanagerConfig CRs
grafana: { sidecar: { dashboards: { label: grafana_dashboard } } }
kubeStateMetrics: { enabled: true }
nodeExporter: { enabled: true }
kubeControllerManager: { enabled: false }   # set false for control-plane components Prometheus cannot reach
kubeScheduler: { enabled: false }
kubeEtcd: { enabled: false }
kubeProxy: { enabled: false }
```
By default the chart installs kube-state-metrics, prometheus-node-exporter and Grafana as dependent charts.
Chart README: Prometheus discovers monitors "labeled with the same release tag" as the release, and setting
`podMonitorSelectorNilUsesHelmValues` and `serviceMonitorSelectorNilUsesHelmValues` to `false` lifts that filter.
HA notes from the README: `replicas` is per shard, keep anti-affinity on, do not clear the replica external labels,
and a Kubernetes Service gives availability but no deduplication (use Thanos Query or another deduplicating backend).

## 2. The CRDs
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata: { name: api, namespace: payments, labels: { team: payments } }
spec:
  selector: { matchLabels: { app: api } }         # selects SERVICES (not pods) by label
  namespaceSelector: { matchNames: [payments] }
  endpoints:
    - port: http-metrics                            # Service port NAME, not number
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s
      metricRelabelings: [{ action: drop, regex: "go_gc_.*", sourceLabels: [__name__] }]
      tlsConfig: { insecureSkipVerify: false, ca: { secret: { name: api-ca, key: ca.crt } } }
      bearerTokenSecret: { name: api-token, key: token }
---
kind: PodMonitor                 # selects pods directly, bypassing the Service
spec: { selector: { matchLabels: { app: worker } }, podMetricsEndpoints: [{ port: metrics }] }
---
kind: PrometheusRule
metadata: { name: api-rules, namespace: payments, labels: { team: payments } }
spec:
  groups:
    - name: api.rules
      rules:
        - alert: ApiHighErrorRate
          expr: sum(rate(http_requests_total{job="api",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="api"}[5m])) > 0.05
          for: 10m
          labels: { severity: page, team: payments }
---
kind: Probe                      # blackbox exporter targets as a CRD
spec: { prober: { url: "blackbox-exporter:9115" }, module: http_2xx, targets: { staticConfig: { static: ["https://shop.example.com"] } } }
---
apiVersion: monitoring.coreos.com/v1alpha1
kind: ScrapeConfig               # targets outside Kubernetes or configs ServiceMonitor/Probe/PodMonitor cannot express
---
kind: AlertmanagerConfig         # per-namespace routes/receivers merged into the Alertmanager config
```
- API reference: ServiceMonitor `jobLabel` picks the job name from a Service label; if empty or absent the job
  defaults to the Service name. `scrapeTimeout` cannot be greater than the scrape interval or the operator rejects
  the resource. `bearerTokenSecret` must be in the same namespace as the custom resource.
- ScrapeConfig (v1alpha1) tier-1 service discovery: Kubernetes, file, static, DNS, HTTP. Cloud providers (Azure,
  EC2, GCE, DigitalOcean) are tier-2. Prefer ServiceMonitor, PodMonitor or Probe when they fit.
- AlertmanagerConfig: the API reference describes `alertmanagerConfigMatcherStrategy`; with the namespace
  strategies an AlertmanagerConfig only processes alerts whose `namespace` label equals its own namespace.
- The operator stores the generated Prometheus config in a Secret named `prometheus-<Prometheus object name>`
  (key `prometheus.yaml.gz`) in the Prometheus object's namespace.

## 3. "My ServiceMonitor is not picked up" checklist
1. Prometheus CR selectors: `serviceMonitorSelector` and `serviceMonitorNamespaceSelector` decide which monitors
   and namespaces are selected. With the Helm defaults the monitor needs the release label. Fix with the
   `*NilUsesHelmValues: false` settings above or add the label.
2. The namespace selector excludes it.
3. `spec.selector` matches the **Service's** labels (not Deployment or pod labels).
4. Endpoint `port` is the port **name** on the Service. Unnamed Service ports cannot be matched, and a numeric
   port gives `spec.endpoints.port in body must be of type string`.
5. A Service matching the selector exists. A ServiceMonitor with no matching Service never appears on the
   Service Discovery page.
6. The Prometheus ServiceAccount can get, list and watch Services and Endpoints in the target namespace.
7. The operator rejects invalid resources and emits a Kubernetes Event for AlertmanagerConfig, PrometheusRule,
   ServiceMonitor, PodMonitor, Probe and ScrapeConfig: `kubectl get events --field-selector=involvedObject.name=<name> -n <ns>`.
   Check the Prometheus `/service-discovery` page (port-forward `svc/prometheus-operated 9090:9090`) and grep the
   generated Secret: `kubectl -n monitoring get secret prometheus-<name> -ojson | jq -r '.data["prometheus.yaml.gz"]' | base64 -d | gunzip`.

## 4. Volume control
- **kube-state-metrics** (CLI arguments page): `--resources` takes a comma-separated list and defaults to the full
  set (pods, deployments, nodes and about two dozen more); `--namespaces` and `--namespaces-denylist` limit
  namespaces; `--metric-allowlist` and `--metric-denylist` take exact names or regexes and are mutually exclusive;
  `--shard` (zero-indexed) with `--total-shards` shards the instance, and sharding is disabled when total shards is 1.
  Label metrics (`kube_pod_labels`) expose no Kubernetes labels unless `--metric-labels-allowlist` is set.
- **kubelet**: `/metrics/cadvisor`, `/metrics/resource` and `/metrics/probes` are separate endpoints with their own
  lifecycle. Trim series with `metricRelabelings` on the kubelet ServiceMonitor and compare series counts before and after.
- **node_exporter**: disable a default collector with `--no-collector.<name>` (for example `arp`, `btrfs`), or start
  with `--collector.disable-defaults --collector.<name> ...`. `--collector.filesystem.mount-points-exclude` is a
  regex of mount points to skip.

## 5. Scaling the Operator setup
- `shards: N` on the Prometheus CR splits scrape targets across N StatefulSets (default sharding strategy hashes the
  target address). Total pods = `replicas` x `shards`. The operator HA page says querying all data then needs
  query federation such as Thanos Query and a distributed rule engine such as Thanos Ruler. Functional sharding is
  recommended where possible.
- Replicas get an external label `prometheus_replica` by default (`replicaExternalLabelName`). For Mimir or Grafana
  Cloud dedupe the troubleshooting page uses a `cluster` label (include `$(SHARD)` for sharded setups) and renames
  `prometheus_replica` to `__replica__` with `writeRelabelConfigs`.
- `additionalScrapeConfigs` (a Secret) remains the raw-YAML escape hatch; `ScrapeConfig` CRs are the CRD route.
- Upgrades: with Helm v3 the chart's CRDs are not updated by default, and CRD updates cause a major chart bump.
  Apply CRDs with `kubectl apply --server-side --force-conflicts` (the operator troubleshooting page: client-side apply
  fails with `metadata.annotations: Too long`; server-side needs Kubernetes 1.22+). The chart has an optional
  `crds.upgradeJob` (preview, off by default). UPGRADE.md lists per-version CRD URLs and breaking changes.

## Verify
- [ ] Port-forward `svc/prometheus-operated` 9090: `/targets` shows the new ServiceMonitor job `UP` after apply.
- [ ] `kubectl get prometheusrule -A` entries appear under `/rules`.
- [ ] No `TargetDown` alerts for control-plane components you disabled or cannot reach.
- [ ] Series counts from the kubelet job drop after relabelings (compare `count({job="kubelet"})`).

## Checked
2026-11-08. Confirmed in the kube-prometheus-stack README and `values.yaml` (OCI install, prerequisites, dependent
charts, every values key above, NilUsesHelmValues behaviour, HA notes, `crds.upgradeJob`), Prometheus Operator
getting-started, troubleshooting, high-availability and ScrapeConfig pages, the API reference (ServiceMonitor, PodMonitor,
Probe, `jobLabel`, `scrapeTimeout`, `replicaExternalLabelName`, shard and replica semantics, matcher strategy),
the kube-state-metrics CLI arguments page and the node_exporter README. Removed: ServiceMonitor relabeling on
`__meta_kubernetes_pod_node_name`, `humanizePercentage` annotation, cAdvisor labeldrop and container filter advice,
kubelet probes-endpoint advice, Operator RBAC claim (the docs name the Prometheus ServiceAccount), the guessed Secret
and Service names, and the `charts/crds/` path.
Method: documentation only; no commands were run.
