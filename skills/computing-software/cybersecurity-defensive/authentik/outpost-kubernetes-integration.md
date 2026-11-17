---
id: computing-software.cybersecurity-defensive.authentik.outpost-kubernetes-integration
name: outpost-kubernetes-integration
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, outpost, kubernetes, httproute, ingress, json-patches, remote-cluster]
level: advanced
status: docs-checked
description: "Use the authentik Kubernetes outpost integration: resources created, kubernetes_* settings, disabled components, JSON patches, x509 strict and remote clusters."
sources:
  - https://docs.goauthentik.io/add-secure-apps/outposts/integrations/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let authentik deploy and keep outposts updated in a cluster.

## Resources created
Deployment, protocol Service, metrics Service, Secret with the outpost token; ServiceMonitor if the Prometheus Operator exists; for proxy outposts an Ingress, an HTTPRoute (needs Gateway API installed and `kubernetes_httproute_parent_refs` set), and a Traefik Middleware for forward auth.

## Settings
- General: `object_naming_template`, `container_image`, `kubernetes_replicas`, `kubernetes_namespace` (defaults to authentik's namespace), `kubernetes_service_type` (`ClusterIP`, `LoadBalancer`), `kubernetes_image_pull_secrets` (create secrets in the target namespace first), `kubernetes_json_patches` (RFC 6902 patches on generated objects), `kubernetes_disable_x509_strict`.
- Ingress: `kubernetes_ingress_annotations` (for example cert-manager), `kubernetes_ingress_secret_name` (empty disables TLS config), `kubernetes_ingress_class_name`, `kubernetes_ingress_path_type`.
- Gateway API: `kubernetes_httproute_parent_refs`, `kubernetes_httproute_annotations`.
- `kubernetes_disabled_components` stops creation of: `secret`, `deployment`, `service`, `service-metrics`, `prometheus servicemonitor`, `ingress`, `traefik middleware`, `httproute`.

Gotcha: `certificate verify failed` in outpost logs means the cluster root CA lacks certain key usage extensions; set `kubernetes_disable_x509_strict` to true.

## Permissions and remote clusters
The required cluster-level and namespace-level permissions are documented in the authentik Helm chart. To manage a remote cluster, install that chart in the target cluster and namespace; it prints an example kubeconfig to add to authentik as the integration.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/add-secure-apps/outposts/integrations/kubernetes/ (read in full); dropped the Helm chart file names, which the page does not state.
