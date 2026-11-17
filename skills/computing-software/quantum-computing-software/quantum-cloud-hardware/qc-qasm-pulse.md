---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-qasm-pulse
name: qc-qasm-pulse
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [openqasm3-timing-defcal]
level: sme
status: draft
description: "Use delay, durations and defcal grammar for calibration-level definitions on supporting backends."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timing and pulse-level (defcal)
```
duration t = 100ns;
delay[t] q[0];
defcal x q { /* pulse grammar, platform specific */ }
```
- Pulse grammar (OpenPulse) is a separate spec section; hardware vendors define their own ports and frames.
- IBM removed or changed pulse access on cloud backends in recent years; check current docs (unconfirmed).

## Gotchas
- defcal bodies are not portable between vendors.

## Self-check
Add a delay and verify the scheduled duration.
