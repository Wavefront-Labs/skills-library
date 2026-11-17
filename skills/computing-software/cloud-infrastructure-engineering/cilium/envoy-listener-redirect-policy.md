---
id: computing-software.cloud-infrastructure-engineering.cilium.envoy-listener-redirect-policy
name: envoy-listener-redirect-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, envoy, listener, ciliumenvoyconfig, toports, forward-proxy]
level: advanced
status: docs-checked
description: "Redirect matching Cilium egress traffic to a named Envoy listener via toPorts listener.envoyConfig, with scope, annotation and credential pitfalls."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer4/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envoy listener redirect

A `toPorts` entry can carry `listener` to hand traffic to a named Envoy listener defined in a CiliumEnvoyConfig (CEC) or CiliumClusterwideEnvoyConfig (CCEC). Prefer Gateway API (including GAMMA for east-west) first; the page warns that raw Envoy config gets minimal validation and mistakes are hard to debug.

Keys under `listener`: `envoyConfig` (with `kind` and `name`) and `name` (the listener name in that config).
- Kind omitted: a CiliumNetworkPolicy resolves a namespaced CiliumEnvoyConfig in its namespace; a CiliumClusterwideNetworkPolicy resolves a CiliumClusterwideEnvoyConfig.
- A CNP may reference a CCEC by setting `kind: CiliumClusterwideEnvoyConfig`; a CCNP can only reference a CCEC.
- Egress only, alongside `ports`. Cannot be combined with L7 `rules` (HTTP or DNS) in the same `toPorts` entry or another entry for the same port.

Names must match: policy `envoyConfig.name` equals CCEC `metadata.name`; policy `name` equals the listener name inside.

Annotation `cec.cilium.io/use-original-source-address`: defaults `"true"` for hand-written configs. Set `"false"` only when upstream traffic leaves the cluster, since reuse of the same 5-tuple fails (source pod or destination in host namespace, or destination pod on same node with an HTTP policy). Keep default for in-cluster upstreams.

The Cilium Envoy ships a curated extension subset; check the extensions build config for your version.

## Forward proxy with auth
Docs example: TCP proxy with `tunneling_config` adds `Proxy-Authorization` and forwards to a proxy at 10.0.100.10:3128; `toCIDRSet` matches everything except RFC 1918 ranges. `headers_to_add` takes only literals (no secrets or SDS), so credentials sit in plain text in the CCEC; restrict with RBAC.

Setting `port: "0"` is a wildcard for all ports of the protocol; pairs with a transport-level TCP proxy listener.

## Checked

2026-11-08. Read in full against the Cilium docs (source rst of the Layer 4 policy page, Envoy listener, forward proxy and wildcard port sections): https://docs.cilium.io/en/stable/security/policy/layer4/. Confirmed the listener keys, scope rules, annotation behaviour, forward proxy credential note and wildcard port stated above. Nothing was removed.

Method: documentation only; no commands were run.
