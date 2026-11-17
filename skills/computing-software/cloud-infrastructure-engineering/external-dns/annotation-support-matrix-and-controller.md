---
id: computing-software.cloud-infrastructure-engineering.external-dns.annotation-support-matrix-and-controller
name: annotation-support-matrix-and-controller
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, controller-annotation, annotation-support, dns-controller, source-annotations]
level: practitioner
status: docs-checked
description: "Which ExternalDNS sources honour which annotations, how the controller annotation makes a source skip a resource, and the footnoted exceptions."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annotation support by source

**controller annotation:** `external-dns.kubernetes.io/controller`. If it exists with a value other than `dns-controller`, the source ignores the resource. Use it to hand a resource to another controller.

Sources that read `controller`: Contour, Gateway, Ingress, Istio, Node, OpenShift, Service, Skipper.

**From the docs table**
- `hostname`: Contour, Gateway, Ingress, Istio, Kong, OpenShift, Pod, Service, Skipper, Traefik (unless `--ignore-hostname-annotation`).
- `internal-hostname`: Pod and Service.
- `target`: nearly all, but not the CRD source or Connector.
- `ttl`: all except Pod, CRD and Connector.
- The CRD source (DNSEndpoint) reads none of these annotations.

**Footnotes that bite**
- Gloo: `ttl` and provider-specific annotations must be on the listener's `VirtualService`.
- Service: `target` is also supported on Pods referenced from a headless Service's Endpoints.
- Traefik: needs an explicit `target`; no LB status exists.
- Gateway API: annotation placement differs between Gateway and Routes.

## Checked

2026-11-04. Confirmed against the ExternalDNS annotations page support table, its footnotes, the controller annotation section and the Gateway API placement section. Removed an unsourced debug-log verification line.
Method: documentation only; no commands were run.
