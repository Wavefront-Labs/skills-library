---
id: computing-software.cloud-infrastructure-engineering.knative.encryption-overview
name: encryption-overview
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [encryption, tls, cert-manager, external-domain-tls, cluster-local-domain-tls, system-internal-tls]
level: practitioner
status: docs-checked
description: "Understand the three independent Serving encryption layers and which need cert-manager."
sources:
  - https://knative.dev/docs/serving/encryption/encryption-overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick which encryption layer you need.

Knative Serving encryption has three independent parts, which may use different Certificate Authorities:

1. HTTPS at the ingress layer external to the cluster, for domains like `myapp-<namespace>.example.com`.
2. HTTPS at the ingress layer internal to the cluster, for cluster-local domains like `myapp.<namespace>.svc.cluster.local`.
3. HTTPS between Knative system components: ingress-controller, activator and queue-proxy.

External domain encryption:
- Certificate CN/SAN holds the external domain.
- Certificates are hosted via SNI by the ingress-controller's external endpoint.
- Callers must trust the signing CA; that is outside Knative's scope.
- Certificates are provided manually or by automatic provisioning.

Cluster-local encryption:
- CN/SAN holds names like `myapp.namespace.svc.cluster.local`, `myapp.namespace.svc` and `myapp.namespace`.
- Hosted via SNI on the cluster-local endpoint.
- Callers must trust the CA; trust-manager from cert-manager is one option.
- Needs cert-manager plus the Knative cert-manager integration.

System-internal encryption:
- The ingress-controller, activator and queue-proxy host TLS endpoints when enabled.
- Also needs cert-manager and its integration.
- Each connection is verified by specific SANs, and each component must trust the CA (possibly the full chain) via a `CABundle` the cluster administrator provides.

Each part is switched on with its own key in `config-network`: `external-domain-tls`, `cluster-local-domain-tls` and `system-internal-tls`, each set to `Enabled`. Control-plane traffic (including Kubernetes PreStopHooks and metrics metadata) is not encrypted.

## Checked

2026-11-04. Confirmed against the Serving Encryption Overview page and the three per-part pages (knative/docs source): the three independent parts, the example domains, CN/SAN contents, SNI hosting, trust responsibilities, cert-manager and integration requirements for cluster-local and system-internal encryption, specific SANs and `CABundle` provided by the administrator, and the `Enabled` keys in `config-network`. Added the three key names and the note that control-plane traffic is unencrypted, both stated on those pages. Nothing removed.

Method: documentation only; no commands were run.
