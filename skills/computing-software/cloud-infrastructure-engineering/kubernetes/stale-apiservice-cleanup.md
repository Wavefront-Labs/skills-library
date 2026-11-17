---
id: computing-software.cloud-infrastructure-engineering.kubernetes.stale-apiservice-cleanup
name: stale-apiservice-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, aggregation-layer, stale-apiservice, faileddiscoverycheck, namespace-termination, api-discovery]
level: practitioner
status: docs-checked
description: "Find and remove APIServices left behind by uninstalled add-ons, which break kubectl discovery, Helm, garbage collection and namespace deletion."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/namespaces/", "https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kube-aggregator/pkg/controllers/status/remote/remote_available_controller.go", "https://github.com/kubernetes-sigs/metrics-server", "https://keda.sh/docs/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing stale APIServices

An add-on is uninstalled but its APIService object remains, pointing at a Service that no longer
exists. Symptoms across the cluster:
- `kubectl` prints discovery errors for the group (for example `metrics.k8s.io/v1beta1`) ending in
  `the server is currently unable to handle the request`.
- Clients that run full API discovery report the same errors.
- Namespaces stick in `Terminating` with condition `NamespaceDeletionDiscoveryFailure`.

## Find
```bash
kubectl get apiservices | grep -v True
kubectl get apiservice v1beta1.custom.metrics.k8s.io -o jsonpath='{.spec.service}{"\n"}{.status.conditions[0].reason}: {.status.conditions[0].message}{"\n"}'
```
`Available=False` reasons set by the aggregator include `ServiceNotFound`, `EndpointsNotFound`,
`MissingEndpoints` and `FailedDiscoveryCheck` (`ServiceAccessError` gives `Unknown`).

## Decide
- Add-on still wanted: fix it (pods, Service, certificates, network policies blocking the
  apiserver).
- Add-on gone: delete the APIService.
  ```bash
  kubectl delete apiservice v1beta1.custom.metrics.k8s.io
  ```
  Common leftovers: `v1beta1.metrics.k8s.io` (metrics-server), `v1beta1.custom.metrics.k8s.io`
  (Prometheus Adapter) and `v1beta1.external.metrics.k8s.io` (KEDA), plus APIs of removed operators.

## Prevent
Uninstall through the same tool that installed (Helm deletes its APIService), and include
APIServices in decommissioning checklists.

## Verify
`kubectl get apiservices | grep -v True` returns only the header, `kubectl api-resources` runs
without errors, and stuck namespaces finish terminating.

## Checked
2026-10-27 against Kubernetes sources and docs: the kube-aggregator remote availability
controller and `k8s.io/api` core types (kubernetes master), the aggregation layer task page
(kubernetes/website main, v1.38 development tree; v1.37 is the latest release), the
metrics-server, prometheus-adapter and KEDA docs repositories. Confirmed: the APIService condition
reasons, the `NamespaceDeletionDiscoveryFailure` namespace condition, the ServiceUnavailable
message text, and which add-on registers each metrics APIService. Removed unchecked claims about
garbage collector and quota controller stalls and replaced a quoted kubectl message that no source
showed verbatim.
Method: documentation only; no commands were run.
