---
id: computing-software.cloud-infrastructure-engineering.contour.contour-deployment-models-and-multi-instance
name: contour-deployment-models-and-multi-instance
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [deploy-options, multiple-instances, ingress-class-name, hostnetwork, nodeport, certgen, leader-election-resource-name, secrets-name-suffix]
level: advanced
status: docs-checked
description: "Contour deployment options: resource requests, NodePort and hostNetwork, disabling features, and running multiple instances in separate or shared namespaces."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/deploy-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour deployment options

Install needs a TLS Secret pair for Contour<>Envoy gRPC (made by the `certgen` Job or supplied) and traffic forwarded to Envoy, normally a `type: LoadBalancer` Service.

Starting resource requests: `contour` 128Mi / 250m; `envoy` 256Mi / 500m; `shutdown-manager` 50Mi / 25m. Set limits too; the example manifests omit them.

Without a LoadBalancer:
- NodePort: set the Envoy Service `type: NodePort` (second number in `80:30274/TCP` is the port).
- Host networking: Envoy pod `hostNetwork: true`, `dnsPolicy: ClusterFirstWithHostNet`, and `contour serve --envoy-service-http-port=80 --envoy-service-https-port=443`; pair with a DaemonSet.

`--disable-feature=extensionservices` (repeatable) makes that CRD optional.

Multiple Contour instances (external vs internal ingress, per-class):
- Separate namespaces (recommended): change namespaces everywhere, make cluster-scoped names unique (`ClusterRole`, `ClusterRoleBinding`), share the CRDs, add `--ingress-class-name=<unique>` to the Contour container, and remove the two `hostPort` entries from `03-envoy.yaml`.
- Same namespace: unique names for everything, adjusted selectors and labels, certgen `--secrets-name-suffix=<suffix>`, `--leader-election-resource-name=<unique lease>`, `--envoy-service-name=<unique>`, envoy `--xds-address` pointing at the unique Contour Service, and no `hostPort`s.
- Gateway provisioner: one Gateway per instance, each GatewayClass with a `ContourDeployment` setting `spec.runtimeSettings.ingress.classNames`.

Alongside another controller: annotate Ingresses `kubernetes.io/ingress.class: "contour"`. Uninstall by deleting the namespace (`kubectl delete ns projectcontour`).

## Checked

2026-11-04. Confirmed against the Contour deployment options page (deploy-options.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
