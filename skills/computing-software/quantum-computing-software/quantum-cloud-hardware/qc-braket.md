---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-braket
name: qc-braket
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [amazon-braket, quantum-cloud-providers]
level: practitioner
status: draft
description: "Run circuits on Braket simulators and QPUs with the Python SDK, S3 results and cost control."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Amazon Braket SDK
```python
from braket.circuits import Circuit
from braket.aws import AwsDevice
task = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1").run(Circuit().h(0).cnot(0,1), shots=100)
```
- Results land in an S3 bucket you own (amazon-braket-* by default). Local simulator: braket.devices.LocalSimulator.
- QPU billing is per task plus per shot; set budget alerts.

## Gotchas
- Hybrid jobs and QPU access are region specific.

## Self-check
Run the Bell circuit on LocalSimulator then SV1.
