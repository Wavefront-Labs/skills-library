---
id: computing-software.cloud-infrastructure-engineering.gateway-api.multi-team-shared-gateway
name: multi-team-shared-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [shared-gateway, multi-tenancy, cross-namespace, httproute, namespaces, tls-ownership]
level: practitioner
status: docs-checked
description: "Build a shared Gateway in an infra namespace that team namespaces attach to via a namespace label, with centrally managed TLS and domain."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/multiple-ns.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/use-cases.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scenario: an infra team owns `shared-gateway` in `infra-ns` for `foo.example.com`; `site-ns` (apps home, login) and `store-ns` (store) attach HTTPRoutes; the security team owns the certificate.

The Gateway:

- Has an `https` listener for `foo.example.com` with the certificate Secret `foo-example-com` in `infra-ns`, so TLS is centrally managed and terminates all attached Routes with no TLS config on the HTTPRoutes.
- Constrains attachment with a label selector:

```yaml
allowedRoutes:
  namespaces:
    from: Selector
    selector:
      matchLabels:
        shared-gateway-access: "true"
```

Only namespaces labelled `shared-gateway-access: "true"` can attach. An HTTPRoute in a namespace without the label that names `infra-ns/shared-gateway` is ignored.

The app teams' HTTPRoutes set `parentRefs` to `shared-gateway` in `infra-ns` and omit `hostnames`, so they match all traffic on the listener and stay domain agnostic. Example split: `store` matches `/store` to Service `store`; `home` is the default rule for `foo.example.com/*`; `login` matches `/login` and weights traffic between `login-v1` and `login-v2`.

The Gateway merges all attached Routes into one flat rule list. Precedence is most specific match first, with conflicts resolved by the API design rules (oldest creation timestamp, then `namespace/name` alphabetical).

Use separate HTTPRoutes per app to isolate canary rollouts and failure domains while sharing IP, port, DNS domain and certificate.

## Checked

2026-11-04. Confirmed on the Gateway API cross-namespace routing guide (multiple-ns.md) and the API design guide (conflict tie-breakers: oldest creation timestamp, then namespace/name order): scenario, listener TLS, label selector, ignored Route, domain-agnostic Routes, flat merge. Nothing removed.

Method: documentation only; no commands were run.
