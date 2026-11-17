---
id: computing-software.cloud-infrastructure-engineering.kubernetes.custom-and-external-metrics-apis-deep-dive
name: custom-and-external-metrics-apis-deep-dive
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, metrics-server, custom-metrics-api, external-metrics-api, prometheus-adapter, apiservice, resource-metrics-api, hpa, cloudwatch-adapter, datadog-cluster-agent]
level: advanced
status: docs-checked
description: "The three distinct metrics APIs HPA can query, how prometheus-adapter maps a PromQL query to them, and the APIService wiring that makes it work."
sources: ["https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#scaling-on-custom-metrics", "https://github.com/kubernetes-sigs/prometheus-adapter/blob/master/docs/config.md", "https://github.com/kubernetes-sigs/prometheus-adapter/blob/master/docs/externalmetrics.md", "https://github.com/kubernetes-sigs/prometheus-adapter/blob/master/docs/walkthrough.md", "https://keda.sh/docs/2.22/operate/metrics-server/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom and external metrics APIs, deep dive

**Goal:** know exactly which of the three metrics APIs a given HPA metric type queries, and how
to write (or debug) the adapter rule that translates a PromQL/cloud-metric query into the shape
the API server expects. Without this, "HPA shows `<unknown>`" is unsolvable by guessing.

## 1. Three APIs, three purposes — don't conflate them
- **`metrics.k8s.io`** (Resource Metrics API) — generally provided by **metrics-server**. CPU/memory
  usage per pod/node, nothing else. HPA's `type: Resource` and `type: ContainerResource` metrics
  read this. No PromQL, no custom queries.
- **`custom.metrics.k8s.io`** — per-object metrics, namespaced to a specific Kubernetes resource
  (`type: Pods` or `type: Object` in HPA). Backed by an **adapter** you deploy (prometheus-adapter
  is the common one; cloud vendors ship their own). HPA's `type: Pods`/`type: Object` metrics
  read this.
- **`external.metrics.k8s.io`** — metrics about things **outside** any Kubernetes object (SQS
  queue depth, a Kafka consumer group's lag, a cost metric). HPA's `type: External` reads this.
  KEDA's metrics server exposes external metrics only (its `cpu` and `memory` scalers use the
  standard metrics from the Kubernetes Metrics Server instead).
Each is registered as a separate `APIService` (`kubectl get apiservices`); if one is missing or
its backing service is down, HPAs using *that* API fail. Check the `kubectl get apiservices`
AVAILABLE column first, before touching adapter config.

## 2. prometheus-adapter: query → metric mapping
prometheus-adapter's ConfigMap (`rules:`) maps an incoming API request (e.g.
"custom metric `http_requests_per_second` for Pods in namespace `shop`") to a PromQL template:
```yaml
rules:
- seriesQuery: 'http_requests_total{namespace!="",pod!=""}'
  resources:
    overrides: {namespace: {resource: "namespace"}, pod: {resource: "pod"}}
  name: {matches: "^(.*)_total$", as: "${1}_per_second"}
  metricsQuery: 'sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)'
```
- `seriesQuery` discovers which Prometheus series exist and which resources (pod/namespace/node)
  they can be grouped by — get this wrong and the metric does not appear under
  `/apis/custom.metrics.k8s.io/v1beta2/...`.
- `name.as` is the metric name HPA references in `metrics[].pods.metric.name` — a common bug is
  writing the HPA's metric name and the adapter rule's `as` slightly differently (plural vs
  singular, underscore vs no suffix) and getting silent non-matches.
- `metricsQuery`'s `<<.GroupBy>>`/`<<.LabelMatchers>>` are adapter template syntax, not literal
  PromQL — test the rendered query directly in Prometheus's UI by substituting real label values
  before trusting the adapter wiring.
- External metrics use `externalRules`, "almost identical" to `rules`, with the same template
  mechanism. The External Metrics API requires a namespace in the URL, so for an HPA the adapter
  adds a `namespace` label to the configured `seriesQuery`.

## 3. Debugging the pipeline end to end
1. `kubectl get apiservices v1beta2.custom.metrics.k8s.io` — `Available: True`? If not, the
   adapter's Service or its TLS setup is the problem, not Prometheus.
2. `kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta2/namespaces/<ns>/pods/*/http_requests_per_second"`
   — does the raw API return a value? If empty/404, the adapter rule doesn't match anything — check
   `seriesQuery` against Prometheus directly.
3. `kubectl describe hpa <name>` — does the `metrics` block reference the exact `name` and
   namespace the adapter actually serves? A mismatch shows up as `FailedGetObjectMetric`,
   `FailedGetPodsMetric` or `FailedGetExternalMetric` events.
4. If using a cloud-managed adapter (CloudWatch, Datadog, Stackdriver) instead of
   prometheus-adapter, the mapping step is proprietary to that adapter — same three-API model
   applies, but there's no PromQL template to inspect; consult that adapter's own metric-mapping
   docs/CRDs.

## Gotchas
- An `APIService` such as `v1beta1.external.metrics.k8s.io` points at a single Service, so one
  adapter serves each of those API versions. Check which adapter owns it
  (`kubectl get apiservice v1beta1.external.metrics.k8s.io -o yaml`) before installing a second
  one, such as KEDA's metrics server alongside prometheus-adapter.
- Resource Metrics API (`metrics.k8s.io`) has **no configuration surface** — if CPU/memory HPA
  metrics show `<unknown>`, the fix is never "edit metrics-server config for this metric," it's
  checking metrics-server is running and the pod has resource requests set.
- Adapter rules select series with `seriesQuery` and rename them with `name.matches`/`as` regexes;
  keep rules narrowly scoped per metric so two rules do not overlap on the same series.

## Verify
- [ ] `kubectl get apiservices | grep metrics` shows all required APIServices `Available: True`.
- [ ] The raw custom/external metrics endpoint returns a numeric value matching what you'd compute
      manually from the PromQL query.
- [ ] HPA's `metrics[].pods.metric.name` / `.external.metric.name` exactly matches the adapter
      rule's `name.as` output, including case and pluralization.
- [ ] Only one adapter is registered for each of `custom.metrics.k8s.io` and
      `external.metrics.k8s.io` cluster-wide.

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24), the prometheus-adapter docs on GitHub (config.md, externalmetrics.md, walkthrough.md) and the KEDA 2.22 docs (operate/metrics-server).
- HPA metric types and the three metrics APIs (`metrics.k8s.io` generally provided by metrics-server, `custom.metrics.k8s.io` v1beta2, `external.metrics.k8s.io` v1beta1): HPA page.
- prometheus-adapter registers `v1beta2.custom.metrics.k8s.io` (walkthrough), rule fields `seriesQuery`, `resources.overrides`, `name.matches`/`as`, `metricsQuery` with `<<.Series>>`, `<<.LabelMatchers>>`, `<<.GroupBy>>` (config.md), `externalRules` and the automatic `namespace` label (externalmetrics.md).
- KEDA's metrics server exposes external metrics only, and its `cpu` and `memory` scalers use the standard Kubernetes metrics: KEDA metrics-server page.
- Event reasons `FailedGetObjectMetric`, `FailedGetPodsMetric`, `FailedGetExternalMetric` exist in the HPA controller source.

Method: documentation only; no commands were run.
