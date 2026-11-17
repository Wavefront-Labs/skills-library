---
id: computing-software.cloud-infrastructure-engineering.cilium.deny-policies
name: deny-policies
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, deny-policy, network-policy, precedence, default-deny, ciliumnetworkpolicy]
level: practitioner
status: docs-checked
description: "How Cilium deny policies take precedence over allow policies, the resulting allow/deny matrix, and what deny rules cannot do (L7, toFQDNs)."
sources:
  - https://docs.cilium.io/en/stable/security/policy/deny/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cilium deny policies

Goal: explicitly block traffic to or from a pod regardless of allow rules.

- Available and enabled by default since Cilium 1.9.
- Deny beats allow whether the allow comes from a CiliumNetworkPolicy, a CiliumClusterwideNetworkPolicy or a Kubernetes NetworkPolicy.
- As with allow policies, a pod enters default-deny mode as soon as one policy selects it.

## Worked outcomes from the docs matrix
Server has allows for L7 HTTP, 80/TCP, 81/TCP and the client pod (L3):
- With a deny on 80/TCP: curl server:81 allowed (allow on 81, no deny), curl server:80 denied, ping allowed (L3 allow, no deny).
- With a deny on the client pod at L3: all of curl 80, curl 81 and ping are denied.

## Example
A policy denying ingress from `world` across all namespaces for Cilium-managed pods (the docs example `from_world_deny.yaml`); other inter-cluster traffic stays allowed because only `world` is denied.

## Limits
Deny policies do not support L7 enforcement (denying a URL) and do not support `toFQDNs` (denying a domain name).

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/deny/. 

Method: documentation only; no commands were run.
