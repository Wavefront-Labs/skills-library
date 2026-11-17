---
id: computing-software.cloud-infrastructure-engineering.kubernetes.prometheus-operator-servicemonitor-and-podmonitor
name: prometheus-operator-servicemonitor-and-podmonitor
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, prometheus-operator, servicemonitor, podmonitor, probe-crd, scrape-config, crd, label-selector, namespaceselector, relabeling, kube-prometheus-stack, scrape-gap]
level: advanced
status: docs-checked
description: "How Prometheus Operator compiles ServiceMonitor/PodMonitor CRDs into scrape configs, and the selector/RBAC mismatches that cause silent scrape gaps."
sources: ["https://prometheus-operator.dev/docs/api-reference/api/", "https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/platform/webhook/", "https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus Operator: ServiceMonitor and PodMonitor without the mystery

**Goal:** know the actual mechanism — CRD → generated scrape config in a Secret → reload —
well enough to diagnose "my target isn't being scraped" in minutes instead of restarting
Prometheus and hoping.

## 1. The mechanism
The Prometheus Operator is a controller that watches `ServiceMonitor`, `PodMonitor`, `Probe`,
`ScrapeConfig` and `Prometheus` objects and **renders them into a single scrape-config Secret**
(`prometheus-<name>`, key `prometheus.yaml.gz`), which is mounted into the Prometheus pod and reloaded
by the config-reloader. Nothing is scraped directly
from the CRD — the CRD is a template; the generated config is what actually runs.
```bash
kubectl -n <prom-ns> get secret prometheus-<name> -o jsonpath='{.data.prometheus\.yaml\.gz}' | base64 -d | gunzip
# or, faster: hit Prometheus's own config endpoint
kubectl -n <prom-ns> port-forward svc/prometheus-operated 9090 &
curl -s localhost:9090/api/v1/status/config
```
If a `ServiceMonitor` exists but no corresponding `job_name` appears in that rendered config,
the Operator never picked it up — stop looking at Prometheus and look at the Operator's
selection logic instead.

## 2. ServiceMonitor vs PodMonitor vs Probe
- **ServiceMonitor** — targets Endpoints behind a Kubernetes **Service**; `spec.selector`
  matches Service labels (not Pod labels directly), `spec.endpoints[].port` is the **name** of the
  Service port (it takes precedence over `targetPort`, which names or numbers a container port).
- **PodMonitor** — targets Pods directly, no Service needed; useful for Pods not fronted by a
  stable Service (batch workers, some StatefulSet members). `spec.podMetricsEndpoints[].port` is the
  **container port name**; `portNumber` takes a port number, and `targetPort` is deprecated.
- **Probe** — for blackbox-style external probing (via blackbox_exporter), not for scraping
  an app's own `/metrics`.
Picking the wrong one for the topology is the most common "CRD exists, nothing scrapes"
mistake — a headless/no-Service pod needs PodMonitor, not ServiceMonitor.

## 3. The selector chain that silently drops everything
Three independent selectors must all line up, and a miss on any one produces **no error, just
no target**:
1. `Prometheus.spec.serviceMonitorSelector` (and `podMonitorSelector`) — which ServiceMonitor/
   PodMonitor objects the Operator even looks at. An empty selector (`{}`) matches all objects and a null
   selector matches none. kube-prometheus-stack defaults `serviceMonitorSelectorNilUsesHelmValues` to
   `true`, so it selects ServiceMonitors carrying the chart's `release` label; a ServiceMonitor without
   that label is invisible even if everything else is correct. Check with
   `kubectl get prometheus <name> -o jsonpath='{.spec.serviceMonitorSelector}'`.
2. `Prometheus.spec.serviceMonitorNamespaceSelector` — an empty selector matches all namespaces and a
   null selector (the default) matches the current namespace only; a ServiceMonitor in an app namespace is
   ignored unless this selector is set.
3. `ServiceMonitor.spec.selector` — must match the target Service's labels, and
   `ServiceMonitor.spec.namespaceSelector` must include the Service's namespace if it differs
   from the ServiceMonitor's own namespace.

Diagnostic order: confirm the Operator's own selectors first (step 1-2, cluster-wide
Prometheus config), then the ServiceMonitor's selector against the actual Service labels
(step 3) — most "it worked yesterday" cases are an app team adding a ServiceMonitor without
knowing the `release` label convention.

## 4. RBAC and TLS specifics
- The Prometheus ServiceAccount needs `get`, `list`, `watch` on `nodes`, `nodes/metrics`, `services`,
  `endpoints` and `pods` (and `get` on `configmaps`) in the documented RBAC; the troubleshooting guide notes
  the Endpoints to EndpointSlice transition in kube-prometheus. A missing permission shows up as a
  missing target or 403 in Prometheus, not an Operator-level error.
- `spec.endpoints[].bearerTokenSecret` and similar secret references must be in the **same namespace as
  the ServiceMonitor** (the custom resource) and readable by the Operator, not in the Prometheus namespace
  unless that is where the ServiceMonitor lives.
- `relabelings` vs `metricRelabelings`: the former rewrites target labels (job, instance,
  address) **before** scrape; the latter filters/rewrites scraped samples **after** — mixing
  these up either breaks target discovery or fails to drop high-cardinality series.

## Gotchas
- If `Prometheus.spec.scrapeInterval` is unset it defaults to `30s`; set it explicitly if you rely on a value.
- `additionalScrapeConfigs` (raw Prometheus-native config, bypassing CRDs entirely) coexists
  with CRD-generated jobs — a target "already scraped" via a raw config entry can mask a
  broken ServiceMonitor, hiding the real problem until someone removes the raw config.
- `up{job="..."} == 0` is the reliable first signal of a scrape failure (auth, TLS, network);
  a target entirely missing from `/api/v1/targets` means it was never selected at all — these
  are different failure classes and need different fixes.

## Verify
- [ ] `curl localhost:9090/api/v1/targets` shows the expected job with `health: up`.
- [ ] The Prometheus CR's `serviceMonitorSelector`/`NamespaceSelector` are documented somewhere a new team can find before they write a ServiceMonitor.
- [ ] An alert exists on `up == 0` for critical jobs, not just on missing targets.
- [ ] `metricRelabelings` drops are tested against a sample scrape before merging, so cardinality cuts don't also delete a metric a dashboard needs.

## Checked

Checked against `prometheus-operator/prometheus-operator` main (latest release v0.94.2, 2026-10-23): `Documentation/api-reference/api.md`, `platform/troubleshooting.md`, `platform/rbac.md`, and the kube-prometheus-stack `values.yaml` on `prometheus-community/helm-charts`.
Confirmed: Secret `prometheus-<name>` with key `prometheus.yaml.gz`; `ServiceMonitor` `port` (Service port name) and `PodMonitor` `port`, `portNumber`, deprecated `targetPort`; null versus empty selector semantics for both selectors; kube-prometheus-stack `serviceMonitorSelectorNilUsesHelmValues: true`; RBAC rule list; Secret namespace rule; `scrapeInterval` default `30s`.
Wrong in the draft: secrets live in the ServiceMonitor's namespace, not the target's; unset selectors matched "own namespace" only for the namespace selector, while a null monitor selector matches nothing. Removed as unconfirmed: the claim that upgrades silently change default intervals.

Method: documentation only; no commands were run.
