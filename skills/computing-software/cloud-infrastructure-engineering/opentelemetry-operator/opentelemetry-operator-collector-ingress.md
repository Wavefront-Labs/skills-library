---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-ingress
name: opentelemetry-operator-collector-ingress
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, ingress, openshift-route, ingressclassname, ruletype, subdomain]
level: practitioner
status: docs-checked
description: "Expose Collector receivers outside the cluster using spec.ingress, choosing ingress or OpenShift route, path or subdomain rules, hostname and TLS."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Expose a Collector with ingress or route

`spec.ingress` controls how the Collector is exposed. The doc says it is only available for modes `deployment`, `daemonset` and `statefulset`.

Fields in the v1beta1 reference:
- `type`: `ingress` or `route` (the default value is empty). `route` is OpenShift-specific.
- `hostname`: the hostname by which the ingress proxy can be reached.
- `ingressClassName`: names an IngressClass, which controller implementations use to decide whether they serve this Ingress.
- `ruleType`: how receivers are exposed. `path` exposes each receiver port on a unique path of the single domain in `hostname`. `subdomain` exposes each receiver port on its own subdomain.
- `annotations`: added to the Ingress, for example a cert-manager issuer annotation such as `cert-manager.io/cluster-issuer`.
- `tls`: a list of TLS configurations.
- `route`: OpenShift route settings, only considered when type is `route`.

Example outline:

```yaml
spec:
  mode: deployment
  ingress:
    type: ingress
    ruleType: path
    hostname: otel.example.com
    ingressClassName: nginx
```

## Checked

2026-11-04. Confirmed in the generated OpenTelemetryCollector API reference (docs/api/opentelemetrycollectors.md, read as raw Markdown because the GitHub page view is a stub) (v1beta1 section): `spec.ingress` limited to deployment, daemonset and statefulset, `type` enum `ingress` or `route`, `hostname`, `ingressClassName`, `ruleType` path or subdomain (default path), `annotations` with the cert-manager issuer example, `tls`, and the OpenShift-specific `route` section considered only for type route. Reworded the meaning of the empty default type, which the reference states only as 'default value is empty'.

Method: documentation only; no commands were run.
