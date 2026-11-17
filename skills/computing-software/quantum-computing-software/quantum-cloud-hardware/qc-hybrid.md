---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-hybrid
name: qc-hybrid
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [hybrid-tls-kem]
level: practitioner
status: draft
description: "Enable and test hybrid X25519MLKEM768 key exchange and plan for handshake size growth."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid key exchange in TLS
- Hybrid groups (X25519MLKEM768 name used by browsers and servers, standardization in the IETF; verify current draft status) combine classical and ML-KEM secrets.
```bash
openssl s_client -connect <host>:443 -groups X25519MLKEM768   # OpenSSL 3.5 or later
```
- ClientHello grows by about 1.2 KB; check middleboxes and MTU.

## Gotchas
- Some legacy middleboxes drop large ClientHellos.

## Self-check
Confirm the negotiated group in the handshake output.
