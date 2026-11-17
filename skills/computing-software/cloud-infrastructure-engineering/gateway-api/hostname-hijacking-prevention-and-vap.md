---
id: computing-software.cloud-infrastructure-engineering.gateway-api.hostname-hijacking-prevention-and-vap
name: hostname-hijacking-prevention-and-vap
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [security, hostname-hijacking, validatingadmissionpolicy, namespace-selector, allowedroutes, multi-tenant]
level: advanced
status: docs-checked
description: "Prevent one team claiming another team s hostnames: restrict listener allowedRoutes by namespace selector and enforce with a ValidatingAdmissionPolicy."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/security.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/hostnames.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Risk: distinct Routes and ListenerSets can claim the same hostname. Controllers resolve this, usually first-come first-served (the first created resource wins). If route1 (older, in ns1) later adds route2's hostname to its `hostnames` list, route1 hijacks that hostname because it is older.

Controls from the security guidance:

1. On the Gateway, delegate each hostname clearly to a namespace or set of namespaces: one listener per hostname, each with `allowedRoutes.namespaces.from: Selector` and a `matchLabels` of `kubernetes.io/metadata.name: <namespace>`. The page marks sharing listeners across namespaces as the insecure configuration.
2. `kubernetes.io/metadata.name` is consistently set on namespaces to the namespace name; other labels (such as `env`) are not as safe, because anyone who can label namespaces could change which ones attach.
3. A Gateway has a 64-listener limit. If you need more, let users set hostnames on their Routes but limit which namespace may use which hostname with a mechanism such as a `ValidatingAdmissionPolicy`. Consider a similar limit for hostnames a ListenerSet can claim.
4. The page's example policy (`httproute-hostname-policy`, with a binding) validates that every entry in `spec.hostnames` is contained in an allowed-hostnames annotation, and rejects HTTPRoutes with unauthorized hostnames. Write your own policy against the current page.

## Checked

2026-11-04. Confirmed on the Gateway API security concepts page (security.md), section "Avoiding hostname/domain hijacking": first-created-wins scenario, delegation by namespace selector, metadata.name label, 64-listener limit, ValidatingAdmissionPolicy approach. Removed the unsourced advice (prefer Same/Selector over All, wildcard certificate remark, "tenants cannot edit the label").

Method: documentation only; no commands were run.
