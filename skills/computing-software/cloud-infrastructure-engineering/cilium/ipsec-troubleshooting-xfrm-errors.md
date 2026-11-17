---
id: computing-software.cloud-infrastructure-engineering.cilium.ipsec-troubleshooting-xfrm-errors
name: ipsec-troubleshooting-xfrm-errors
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, ipsec, xfrm, cilium-dbg-encrypt-status, xfrminnostates, troubleshooting]
level: advanced
status: docs-checked
description: "Troubleshoot Cilium IPsec with cilium-dbg encrypt status, expected key counts, tcpdump interpretation and the meaning of Xfrm error counters."
sources:
  - https://docs.cilium.io/en/stable/security/network/encryption-ipsec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPsec troubleshooting

Checks:
- Pods fail to start after enabling: confirm the IPsec Secret and Cilium share a namespace.
- Look for `level=warning` and `level=error` in agent logs; `Device eth0 does not exist` means set `encryption.ipsec.interface=ethX`.
- Run `cilium-dbg encrypt status`. Output includes `Encryption: IPsec`, decryption interfaces, `Keys in use`, `Max Seq. Number`, `Errors`. Keys in use should be 2 per remote node per enabled IP family, 4 during rotation (3 nodes, IPv4 and IPv6, no rotation: 8 per node). Decryption interfaces must include all native devices that may receive pod traffic (for example ENIs).

## tcpdump
It is normal to see both the outer ESP packet and the decrypted inner packet on the same interface (decrypted packets are recirculated). Filter `esp` for encrypted only, a protocol like `icmp` for decrypted only, `esp or icmp` for both.

## Xfrm counters (each is a kernel drop)
- `XfrmInNoStates` / `XfrmOutNoStates`: rise while a rebooted node new key deploys; also if old key cleaned (default after 5 minutes) before the new one is installed everywhere. Agents apply updates within about 1 minute. Raise `ipsec-key-rotation-duration` for slow rollouts like ClusterMesh.
- `XfrmInStateProtoError`: key changed without incrementing the SPI (KEYID), or anti-replay seq mismatch; fix by a proper new rotation.
- `XfrmFwdHdrError` / `XfrmInError`: decrypted packet for a deleted pod, or memory pressure.
- `XfrmInStateInvalid`: packet received while an XFRM state is being deleted (scale-down, some upgrades).
- `XfrmOutStateSeqError`: encryption sequence number hit its maximum.
- `XfrmOutPolBlock`: Cilium dropped packets that would have left the node in plain text.
- `XfrmInTmplMismatch`, `XfrmInNoPols`: bug in decryption XFRM config.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/network/encryption-ipsec/. 

Method: documentation only; no commands were run.
