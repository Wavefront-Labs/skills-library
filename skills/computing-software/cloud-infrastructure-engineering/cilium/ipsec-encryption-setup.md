---
id: computing-software.cloud-infrastructure-engineering.cilium.ipsec-encryption-setup
name: ipsec-encryption-setup
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, ipsec, cilium-ipsec-keys, encryption-type, per-tunnel-keys, native-routing-cidr]
level: practitioner
status: docs-checked
description: "Enable Cilium IPsec encryption: generate the cilium-ipsec-keys secret with the + prefix, set encryption.type=ipsec, interface and DNS proxy transparent mode."
sources:
  - https://docs.cilium.io/en/stable/security/network/encryption-ipsec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPsec transparent encryption setup

## Key secret
Create a secret `cilium-ipsec-keys` in the SAME namespace as Cilium (kube-system). It has one key-value pair; the value format is `key-id encryption-algorithms PSK-in-hex key-size`. Generate with:
```
cilium encrypt create-key --auth-algo rfc4106-gcm-aes
```
or
```
kubectl create -n kube-system secret generic cilium-ipsec-keys \
  --from-literal=keys="3+ rfc4106(gcm(aes)) $(dd if=/dev/urandom count=20 bs=1 2> /dev/null | xxd -p -c 64) 128"
```
The `+` after the key id is strongly recommended: it forces per-tunnel keys derived from the secret. Global IPsec keys are insecure (GHSA-pwqm-x5x6-5586) and deprecated in 1.16.

## Enable
`--set encryption.enabled=true --set encryption.type=ipsec` (ipsec is the default type). With any direct routing configuration set `ipv4NativeRoutingCIDR=CIDR` (agent flag `--ipv4-native-routing-cidr`). Traffic to the same node is not encrypted.

## Dependencies and interface
With L7 proxy enabled (`--enable-l7-proxy=true`), IPsec needs `--dnsproxy-enable-transparent-mode=true`. With direct routing and no interface set, Cilium takes the default route link; override with `--set encryption.ipsec.interface=ethX`.

## Validate
In a Cilium pod install tcpdump and run `tcpdump -l -n -i eth0 esp` (use `cilium_vxlan` when tunneling). ESP packets mean encrypted.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/network/encryption-ipsec/. 

Method: documentation only; no commands were run.
