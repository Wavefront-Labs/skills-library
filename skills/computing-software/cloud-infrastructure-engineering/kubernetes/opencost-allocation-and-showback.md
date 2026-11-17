---
id: computing-software.cloud-infrastructure-engineering.kubernetes.opencost-allocation-and-showback
name: opencost-allocation-and-showback
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, finops, opencost, kubecost-install, cost-allocation-labels, showback, chargeback, cost-allocation]
level: practitioner
status: docs-checked
description: "Allocate Kubernetes spend to teams: install OpenCost, enforce cost allocation labels, handle idle and shared costs, and publish showback or chargeback reports."
sources: ["https://www.opencost.io/docs/installation/install", "https://www.opencost.io/docs/installation/helm", "https://www.opencost.io/docs/specification", "https://www.opencost.io/docs/integrations/api", "https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost allocation with OpenCost, labels and showback

## Install
```bash
helm repo add opencost-charts https://opencost.github.io/opencost-helm-chart
helm repo update
helm install opencost opencost-charts/opencost --namespace opencost --create-namespace -f values.yaml
kubectl port-forward --namespace opencost service/opencost 9003 9090   # API on :9003, UI on :9090
```
`values.yaml` points OpenCost at your existing Prometheus:
```yaml
opencost:
  prometheus:
    internal:
      namespaceName: monitoring
      serviceName: prometheus-kube-prometheus-prometheus
      port: 9090
```
OpenCost requires Prometheus for scraping metrics and storage; it uses cAdvisor usage metrics
and requests from the Kubernetes API. By default it prices nodes from public on-demand list
prices (on AWS, the public pricing API). Its Cloud Costs feature reads real billing data, for
AWS the Cost and Usage Report through Athena. OpenCost was originally developed and open sourced
by Kubecost.

## How allocation works (OpenCost spec)
Per running pod, CPU and memory are charged on the greater of requested and used, plus PVC
storage requests. Workload costs plus idle costs equal asset costs: the part of node cost not
allocated to any workload is **idle**. Shared costs (the spec's example is kube-system) can be
distributed across tenants.

## Labels make it useful
Agree a small set and enforce it at admission (an admission policy on namespaces and workloads):
```yaml
metadata:
  labels:
    team: payments
    cost-center: cc-4711
    env: prod
```
Prefer **namespace-level** labels (one team per namespace) because pod labels drift. The
allocation API aggregates by `namespace`, `label:<name>` or `annotation:<name>`, and accepts
comma-separated lists such as `aggregate=namespace,label:team`.

## Showback vs chargeback
- **Showback**: monthly report per team (cost, efficiency, idle share). Start here.
- **Chargeback**: actually bill cost centers. It needs agreed rules for idle (distribute
  proportionally, or charge to the platform team), shared services, and amortised discounts.
```bash
curl -sG http://localhost:9003/allocation -d window=lastmonth -d aggregate=label:team -d shareIdle=true \
  | jq '.data[0] | map_values(.totalCost)'
```

## Gotchas
- Without a billing integration, numbers use list prices; present them as estimates.
- Overrequested workloads look "expensive" because they reserve capacity; that is the point and
  it drives right-sizing. Show efficiency next to cost.
- Workloads without the aggregation label land in an `__unallocated__` bucket; track its share.

## Verify
- [ ] Monthly allocated plus idle cost is close to the cloud bill for the cluster's nodes and disks.
- [ ] Every namespace has `team` and `cost-center`; the unallocated share is tracked.

## Checked
2026-10-27 against the OpenCost docs (opencost/opencost-website main) and opencost/opencost source.
Confirmed: Helm repo URL and install command, `opencost.prometheus.internal` values, ports 9003
(API) and 9090 (UI), the Prometheus requirement, on-demand list pricing and CUR-via-Athena Cloud
Costs, the max(request, usage) rule and idle definition in the specification, the allocation API
`window=lastmonth`, `aggregate=label:...` and `shareIdle` parameters, the `totalCost` field in the
example output, and the `__unallocated__` name in the source. Removed the Kubecost install command
and percentage targets that no doc covers.
Method: documentation only; no commands were run.
