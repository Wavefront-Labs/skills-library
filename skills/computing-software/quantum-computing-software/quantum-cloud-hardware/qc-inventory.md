---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-inventory
name: qc-inventory
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [crypto-inventory-agility, pqc-migration]
level: practitioner
status: draft
description: "Inventory algorithms and libraries in code, certs and protocols so each can be swapped for PQC."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cryptographic inventory and agility
- Scan source, dependencies, certs (openssl x509 -text), TLS configs and HSM policies for RSA, ECDH, ECDSA.
- Abstract algorithm choice behind configuration, and test larger key and signature sizes.
```bash
grep -rEi "RSA|ECDSA|ECDH|X25519" src/ | head
```

## Gotchas
- Long-lived data is at risk now from harvest-now-decrypt-later.

## Self-check
Produce a table of algorithm, location, data lifetime and migration priority.
