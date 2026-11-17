---
id: computing-software.cloud-infrastructure-engineering.cilium.wireguard-node-to-node-encryption
name: wireguard-node-to-node-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, node-encryption, node-encryption-opt-out-labels, wireguard, control-plane, beta]
level: advanced
status: docs-checked
description: "Encrypt node-to-node and pod-node traffic with encryption.nodeEncryption, control-plane opt-out label behaviour and LB or egress gateway gaps."
sources:
  - https://docs.cilium.io/en/stable/security/network/encryption-wireguard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-to-node WireGuard (beta)

Default WireGuard only encrypts Cilium-managed pod traffic. Add `--set encryption.nodeEncryption=true` (with `encryption.enabled=true` and `encryption.type=wireguard`) to also encrypt node-to-node, pod-to-node and node-to-pod.

## Control-plane opt-out
Nodes labeled `node-role.kubernetes.io/control-plane` opt out. Reason: workers must reach the kube-apiserver to update their WireGuard public key; encrypting that connection creates a bootstrapping loop when a key changes (reboot or re-provisioning). Change the selector with ConfigMap option `node-encryption-opt-out-labels` (default `node-role.kubernetes.io/control-plane`). An empty selector forces encryption but is not recommended: you must then update the key in the node `CiliumNode` manually when a worker key changes.

## Gaps
- N/S load balancer traffic is not encrypted when an intermediate node redirects the request with LoadBalancer/NodePort XDP acceleration, or DSR in non-Geneve dispatch mode.
- Egress Gateway replies are not encrypted with XDP acceleration.

## Coverage table highlights
Pod to remote pod and via ClusterIP: default mode. Pod to remote node, node to pod, node to node: need node-to-node. Pod to remote pod via non-ClusterIP Service: default with Socket LB, node-to-node with kube-proxy. Anything not in the docs table is unencrypted.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the WireGuard encryption page: https://docs.cilium.io/en/stable/security/network/encryption-wireguard/. Confirmed the statements above. Nothing was removed.

Method: documentation only; no commands were run.
