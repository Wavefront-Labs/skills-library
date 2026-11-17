---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-network-ingress-and-openshift-route
name: awx-operator-network-ingress-and-openshift-route
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, ingress, ingress-hosts, tls-secret, route, contour, ingress-class]
level: practitioner
status: docs-checked
description: "Expose AWX through an Ingress with hosts and TLS secrets or an OpenShift Route, including the Contour special case."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/network-and-tls-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator network ingress and openshift route

`ingress_type` accepts `none`, `ingress` and `route`. The operator is not opinionated: when `ingress_type` is not specified it defaults to none and nothing ingress-wise is created.

Generic Ingress variables: `ingress_annotations`, `ingress_class_name` (cluster default), `ingress_hosts` (hostnames, each with optional `tls_secret`), `ingress_path` (/), `ingress_path_type` (Prefix) and `ingress_api_version` (networking.k8s.io/v1). `hostname` and `ingress_tls_secret` are deprecated.

```yaml
spec:
  ingress_type: ingress
  ingress_hosts:
    - hostname: awx-demo.example.com
    - hostname: awx-demo.sample.com
      tls_secret: sample-tls-secret
  ingress_annotations:
    environment: testing
```

Some Ingress Controllers need special configuration; set `ingress_controller`. The docs list Contour with value `contour`.

Route (OpenShift): `route_host` (default `<instance-name>-<namespace>-<routerCanonicalHostname>`), `route_tls_termination_mechanism` (Edge default or Passthrough), `route_tls_secret` and `route_api_version` (route.openshift.io/v1).

```yaml
spec:
  ingress_type: route
  route_host: awx-demo.example.com
  route_tls_termination_mechanism: Passthrough
  route_tls_secret: custom-route-tls-secret-name
```

The deprecated `hostname` defaults to `{{ meta.name }}.example.com`; `ingress_hosts` defines one or multiple FQDNs with an optional Secret holding the TLS information.

## Checked

2026-11-04. Confirmed against the AWX Operator "Network and TLS Configuration" page (Ingress Type, Generic Ingress Controller, Specialized Ingress Controller, Route sections): option lists, variable names, defaults and examples. Removed the claim that `route_tls_secret` supplies a custom certificate beyond the page's "Secret that contains the TLS information", and changed the annotations example to the mapping form the page shows.
Method: documentation only; no commands were run.
