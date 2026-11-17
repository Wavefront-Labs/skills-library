---
id: computing-software.cloud-infrastructure-engineering.cilium.ipsec-key-rotation
name: ipsec-key-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, ipsec, key-rotation, keyid, ipsec-key-rotation-duration, thundering-herd]
level: advanced
status: docs-checked
description: "Rotate the Cilium IPsec key by patching cilium-ipsec-keys with an incremented key ID, ClusterMesh timing and the jitter that protects the API server."
sources:
  - https://docs.cilium.io/en/stable/security/network/encryption-ipsec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPsec key rotation

Preconditions: do not rotate during upgrades or downgrades (all nodes on one Cilium version). Do not change algorithms with different auth key lengths during rotation: Cilium delays applying the new key until the agent restarts and keeps using the old one.

Procedure from the docs:
```
KEYID=$(kubectl get secret -n kube-system cilium-ipsec-keys -o go-template --template={{.data.keys}} | base64 -d | grep -oP "^\d+")
if [[ $KEYID -ge 15 ]]; then KEYID=0; fi
data=$(echo "{\"stringData\":{\"keys\":\"$((($KEYID+1)))+ "rfc4106\(gcm\(aes\)\)" $(dd if=/dev/urandom count=20 bs=1 2> /dev/null | xxd -p -c 64) 128\"}}")
kubectl patch secret -n kube-system cilium-ipsec-keys -p="${data}" -v=1
```
KEYID is a uint8 from 1 to 15, monotonically increasing per rekey, rolling from 15 to 1; agents default to 0 if absent. During transition both keys work because the agent tracks the key used per endpoint.

ClusterMesh: apply the rotation to every cluster in the mesh and raise the transition time with agent flag `ipsec-key-rotation-duration` if needed.

Large clusters: to avoid a thundering herd on the API server (all agents updating CiliumNode at once) Cilium adds random jitter from [0, keyRotationDuration/10] before loading new keys.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/network/encryption-ipsec/. 

Method: documentation only; no commands were run.
