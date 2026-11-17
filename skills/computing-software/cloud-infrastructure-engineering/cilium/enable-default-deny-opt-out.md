---
id: computing-software.cloud-infrastructure-engineering.cilium.enable-default-deny-opt-out
name: enable-default-deny-opt-out
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, enabledefaultdeny, default-deny, dns-visibility, ciliumclusterwidenetworkpolicy, layer7]
level: advanced
status: docs-checked
description: "Apply a Cilium policy that selects endpoints without triggering default-deny using enableDefaultDeny, for example to intercept DNS cluster-wide, and the L7 caveat."
sources:
  - https://docs.cilium.io/en/stable/security/policy/intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opt out of default-deny with enableDefaultDeny

Goal: apply policy (for example DNS interception) cluster-wide without switching endpoints into default-deny.

Set `enableDefaultDeny` with `egress: false` and/or `ingress: false` in the spec. Rules with it disabled are ignored when Cilium decides the endpoint default mode.

Docs example: a `CiliumClusterwideNetworkPolicy` named `intercept-all-dns` whose `endpointSelector` uses `matchExpressions` with `NotIn` on `io.kubernetes.pod.namespace` (kube-system) and `k8s-app` (kube-dns); `enableDefaultDeny` egress and ingress false; one egress rule `toEndpoints` kube-dns in kube-system on port 53 TCP and UDP with `rules.dns` `matchPattern: "*"`. All DNS traffic is intercepted, nothing blocked, even if this is the first policy on the endpoint.

## Warning from the page
`enableDefaultDeny` does not apply to layer-7 policy. Adding an L7 rule that does not include an L7 allow-all causes drops even with default-deny disabled.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/intro/. 

Method: documentation only; no commands were run.
