---
id: computing-software.quantum-computing-software.qiskit.qk-install
name: qk-install
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [qiskit-installation, qiskit-environment]
level: intro
status: draft
description: "Install Qiskit in an isolated environment and pin versions to avoid API breaks."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installation and version management
```bash
python -m venv .venv && . .venv/bin/activate
pip install "qiskit>=2" qiskit-aer qiskit-ibm-runtime matplotlib pylatexenc
python -c "import qiskit; print(qiskit.__version__)"
```
- Pin versions in requirements; use release notes before upgrading. Qiskit 1.0 removed many deprecated APIs.
- Never pip install over an existing qiskit-terra in the same env; start clean.

## Gotchas
- Package qiskit-terra is the legacy name; mixed installs break imports.

## Self-check
Print qiskit.__version__ and run a Bell circuit.
