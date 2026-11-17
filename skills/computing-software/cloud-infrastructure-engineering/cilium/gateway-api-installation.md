---
id: computing-software.cloud-infrastructure-engineering.cilium.gateway-api-installation
name: gateway-api-installation
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, gateway-api, gatewayapi-enabled, crds, tproxy, kube-proxy-replacement]
level: advanced
status: docs-checked
description: "Enable the Cilium Gateway API controller: prerequisites, required and optional Gateway API CRDs, standard vs experimental channel, and the TPROXY timeout trap."
sources:
  - https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cilium Gateway API installation

## Prerequisites
- `kubeProxyReplacement=true`.
- L7 proxy on: `l7Proxy=true` (default).
- Gateway traffic is forwarded to Envoy with TPROXY. With default `bpf.tproxy=false` this uses iptables, so nodes need iptables and the netfilter modules from the L7 proxy requirements; if missing, connections to the Gateway time out without reaching Envoy. `bpf.tproxy=true` (beta) removes the iptables dependency.
- The controller creates a Service of type LoadBalancer, so the environment must support it; since Cilium 1.16 you can instead expose the L7 proxy on the host network.

## CRDs (must be installed first)
GatewayClass, Gateway, HTTPRoute, GRPCRoute, BackendTLSPolicy, ReferenceGrant, TLSRoute, applied with `kubectl apply --server-side -f` from the Gateway API `config/crd/standard/` files (for example `gateway.networking.k8s.io_gatewayclasses.yaml`). The experimental channel is standard plus experimental fields (for example HTTPRoute Retry); install it if you need those. TCPRoute, UDPRoute and ListenerSet CRDs are optional; without them Cilium disables those features. Before upgrading CRDs read the upgrade guide (1.20 notes mention Gateway API v1.6.1 and TLSRoute).

## Enable
`helm upgrade ... --reuse-values --set kubeProxyReplacement=true --set gatewayAPI.enabled=true`, then `kubectl -n kube-system rollout restart deployment/cilium-operator` and `kubectl -n kube-system rollout restart ds/cilium`. CLI equivalent: `cilium upgrade --version <v> --set kubeProxyReplacement=true --set gatewayAPI.enabled=true`. Check with `cilium status`.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/installation/. 

Method: documentation only; no commands were run.
