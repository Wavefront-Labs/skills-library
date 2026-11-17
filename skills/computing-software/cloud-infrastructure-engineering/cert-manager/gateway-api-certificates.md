---
id: computing-software.cloud-infrastructure-engineering.cert-manager.gateway-api-certificates
name: gateway-api-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [gateway-api, gatewayapi, listener, certificaterefs, listenerset, annotations]
level: practitioner
status: docs-checked
description: "Issue Certificates from Gateway API Gateways: enable gatewayAPI in Helm, annotate the Gateway, and satisfy the listener TLS rules cert-manager checks."
sources:
  - https://cert-manager.io/docs/usage/gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable: install the Gateway API v1.4.1 CRDs (`kubectl apply --server-side -f .../standard-install.yaml`) and set Helm `config.gatewayAPI.enabled: true` (no feature flag since 1.15). Gateway API presence is checked only at startup: if CRDs arrive later, `kubectl rollout restart deployment cert-manager -n cert-manager`.

Trigger: annotate the Gateway with `cert-manager.io/issuer` or `cert-manager.io/cluster-issuer`. Certificate `secretName` and name come from `tls.certificateRefs[].name`; `dnsNames` come from the listener `hostname`.

A listener is skipped unless: `hostname` is non-empty; `tls.mode` is `Terminate` (`Passthrough` unsupported); `tls.certificateRefs[].name` is set; `kind`, if set, is `Secret`; `group`, if set, is `""`; `namespace`, if set, equals the Gateway's. Secrets must live in the Gateway's namespace.

Several listeners sharing a Secret name give one Certificate (duplicate hostnames de-duplicated); different names give separate Certificates.

Annotations mirror the Ingress ones: `issuer-kind`, `issuer-group`, `common-name`, `email-sans`, subject fields, `duration`, `renew-before`, `usages`, `revision-history-limit` (min 1), and `private-key-algorithm`, `-encoding`, `-size`, `-rotation-policy`. Copying custom annotations needs v1.18.0+ and `--extra-certificate-annotations`.

ListenerSet (alpha, v1.20.0-beta.0+, Gateway API v1.5+): `gatewayAPI.enableListenerSet: true` and `featureGates.ListenerSets: true`; ListenerSet annotations override the Gateway's. `acme.cert-manager.io/http01-parentreffallback: "true"` makes the HTTP-01 HTTPRoute use the parent Gateway.

## Checked

2026-11-03. Confirmed on the cert-manager Gateway page (usage/gateway): v1.4.1 CRD install, Helm enable flag, startup check and restart, trigger annotations, listener rules, shared Secret name handling, annotation list, v1.18.0 extra annotations, ListenerSet alpha gates (v1.20.0-beta.0, Gateway API v1.5+, enableListenerSet, featureGates), precedence and http01-parentreffallback. Nothing removed.
Method: documentation only; no commands were run.
