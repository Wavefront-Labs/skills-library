---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.opencost-ingestion
name: opencost-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, data-ingestion, opencost-ingestion, opencost, kubernetes-cost-allocation, prometheus, container-cost, cncf]
level: practitioner
status: docs-checked
description: "Ingest Kubernetes cost data with OpenCost: Helm install on an existing Prometheus, allocation API queries by namespace or label, idle cost and load into the cost warehouse."
sources: ["https://opencost.io/docs/", "https://opencost.io/docs/integrations/api", "https://www.opencost.io/docs/installation/helm", "https://www.opencost.io/docs/installation/prometheus", "https://www.opencost.io/docs/specification"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes cost data with OpenCost

OpenCost is a vendor-neutral open source project for measuring and allocating cloud infrastructure and container costs,
built for Kubernetes cost monitoring, showback and chargeback. It splits cluster asset cost to workloads so that container
spend can join the rest of the cost data.

## Install
OpenCost needs a Kubernetes cluster and Prometheus, which it uses for scraping metrics and data storage. The Helm
install assumes an existing Prometheus; the docs give a Prometheus Community chart command with an OpenCost scrape
configuration for a new one, or you can point OpenCost at your own Prometheus with the `PROMETHEUS_SERVER_ENDPOINT`
environment variable.
```bash
helm repo add opencost-charts https://opencost.github.io/opencost-helm-chart
helm repo update
helm install opencost opencost-charts/opencost --namespace opencost --create-namespace -f values.yaml
```
In `values.yaml`, `opencost.prometheus.internal` takes `namespaceName`, `serviceName` and `port` for the Prometheus
service. Pricing comes from the chart values: the docs show a `customPricing` block and per-provider pages for AWS, Azure,
GCP and on-premises. Cloud Costs (from the provider bill) need extra billing integration configuration. If another
kube-state-metrics is running, set `opencost.metrics.kubeStateMetrics.emitKsmV1Metrics` and `emitKsmV1MetricsOnly` to
false, as the docs advise, to avoid duplicate metrics.

## Query the API
Port-forward the service, then query (port 9003 by default, UI on 9090):
```bash
kubectl -n opencost port-forward deployment/opencost 9003
curl -G http://localhost:9003/allocation -d window=7d -d aggregate=namespace -d resolution=1m
curl -G http://localhost:9003/allocation -d window=7d -d step=1d -d aggregate=label:team
```
Parameters of `/allocation`: `window` (required; for example `today`, `7d`, an RFC3339 pair or Unix timestamps),
`aggregate` (`cluster`, `node`, `namespace`, `controllerKind`, `controller`, `service`, `pod`, `container`,
`label:LABEL_NAME`, `annotation:name`, or a comma-separated list), `step` (defaults to the window), `resolution`
(Prometheus query resolution, default `1m`), `includeIdle`, `shareIdle` and `idleByNode`. The allocation API is based on
on-demand list pricing; `/assets` returns the backing asset cost and `/cloudCost` returns provider bill data.

## Load into the warehouse
1. Run a daily job over a fixed window and step with the aggregation keys you need (for example cluster and namespace, or
   a label you enforce) and store the rows with the window start date.
2. Decide how to treat idle cost. By default idle is a separate `__idle__` allocation; `shareIdle=true` spreads it in
   proportion to non-idle cost, per resource, by cluster or by node.

## Gotchas
- Workload cost is the greater of request and usage for resources with allocation cost, so containers with no requests
  carry little cost and push more into idle (OpenCost specification).
- Lower `resolution` values are faster but lose accuracy for short-running pods; the API page tables the error bounds
  (for example, at 30 minutes a pod that runs for 5 minutes can be missed altogether).
- Data lives in Prometheus; ingest on a schedule rather than relying on long history (the chart's daily resolution
  retention defaults to 15 days).
- List prices differ from negotiated or discounted rates; the specification recommends amortised net cost as the price
  input where a provider supplies it.

## Verify
- [ ] The daily load returns rows for every cluster and namespace expected.
- [ ] Every namespace maps to an owner; unlabelled share is tracked.

## Checked
Confirmed against the OpenCost docs home, API page, Helm and Prometheus install pages, API examples and the OpenCost
specification (read in full): Prometheus requirement, Helm repo and install command, values keys, port 9003 and 9090,
allocation parameters and aggregate values, list-price basis, idle behaviour, max(request, usage), resolution accuracy,
15 day default daily resolution retention, amortised net cost recommendation. Removed: the Helm flag `internal.enabled`,
the list of response field names (cpuCoreRequestAverage, efficiency and others not shown on the pages read), the jq
filter, the reconcile-within-5-percent target and the claim about RI and spot price adjustment and the double-counting step.
Method: docs-checked 2026-11-09 against the OpenCost documentation pages listed in sources.
