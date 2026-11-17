---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.servicemonitor-discovery-troubleshooting
name: servicemonitor-discovery-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [servicemonitor-selectors, servicemonitor-troubleshooting, servicemonitor, podmonitor, prometheus-operator, kube-prometheus-stack]
level: practitioner
status: docs-checked
description: "Fix ServiceMonitor/PodMonitor targets that never appear: Prometheus CR selectors, port names, label matching, generated config, events."
sources: ["https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/platform/troubleshooting.md", "https://prometheus-operator.dev/docs/api-reference/api/", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ServiceMonitor discovery troubleshooting

Chain that must hold: the Prometheus resource selects the ServiceMonitor (and its namespace), the ServiceMonitor selects
a Service by labels and by Service port name, and the Prometheus ServiceAccount may get, list and watch Services and
Endpoints for the target app.

## Checklist
1. Picked up by Prometheus? `serviceMonitorSelector` and `serviceMonitorNamespaceSelector` on the Prometheus object
   decide. For namespaces, an empty selector matches all namespaces and a null selector (the default) matches the
   Prometheus object's own namespace only. With kube-prometheus-stack the chart README says to set
   `prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues` and
   `podMonitorSelectorNilUsesHelmValues` to false to discover monitors without label filtering.
2. The operator writes the generated config into a Secret named `prometheus-<prometheus-name>` in the Prometheus
   namespace; check the monitor name appears:
```bash
kubectl -n monitoring get secret prometheus-k8s -ojson | jq -r '.data["prometheus.yaml.gz"]' | base64 -d | gunzip | grep "my-service-monitor"
```
3. Rejected resources: the operator emits a Kubernetes Event for invalid AlertmanagerConfig, PrometheusRule,
   ServiceMonitor, PodMonitor, Probe and ScrapeConfig objects:
```bash
kubectl get events --field-selector=involvedObject.name="<name>" -n "<namespace>"
```
   With kube-prometheus manifests the `PrometheusOperatorRejectedResources` alert fires for them.
4. In the config but missing from Service Discovery: the ServiceMonitor `selector` matches no Service (it references
   Services, not Deployments or Pods, by labels and by port name). List Services with the same labels.
5. `endpoints[].port` must be the Service port **name** (for example `web`), not a number string: `port: "8080"` fails
   with `spec.endpoints.port in body must be of type string: "integer"`. The Service port name is optional in
   Kubernetes but required for a ServiceMonitor. `targetPort` is the name or number of a container port on the pods.
6. Port-forward `svc/prometheus-operated` on 9090 and use the UI to check the live config and discovered targets.

## PodMonitor
Selects pods directly; its `namespaceSelector` defaults to the PodMonitor's own namespace. The Prometheus side uses
`podMonitorSelector`.

## Gotchas
- `ignoreNamespaceSelectors` (the API field `NamespaceSelectors` on the Prometheus spec) makes the operator ignore
  `spec.namespaceSelector` on monitors, so they only discover targets in their own namespace.
- `serviceDiscoveryRole` can be Endpoints (default) or EndpointSlice; for EndpointSlice the Prometheus ServiceAccount
  needs get/list/watch on `endpointslices` in `discovery.k8s.io`.
- Several operators managing the same Prometheus can cause pods stuck in a terminating loop; give each operator a
  distinct `--controller-id` and annotate resources with `operator.prometheus.io/controller-id`.

## Verify
- [ ] The target appears under Status > Targets and is up.

## Checked

2026-11-08. Confirmed against the Prometheus Operator troubleshooting page (raw from the repository; the website URL
returned 404), the API reference (namespace selector semantics, serviceDiscoveryRole, targetPort) and the
kube-prometheus-stack README (partial: only the NilUsesHelmValues sentence was read, not the full values table).
Removed as unconfirmed: the claim that the chart's default selector is `release: <helm release>`, the kubectl jsonpath
checklist, the 'Two Prometheus CRs scrape twice' note and the logs-grep step.
Method: documentation only; no commands were run.
