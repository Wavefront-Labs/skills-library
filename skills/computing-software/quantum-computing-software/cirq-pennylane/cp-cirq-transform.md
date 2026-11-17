---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-cirq-transform
name: cp-cirq-transform
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [cirq-transformers]
level: advanced
status: draft
description: "Apply cirq.optimize_for_target_gateset and merge_single_qubit_gates to retarget circuits."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Circuit transformers and optimization
```python
c2 = cirq.optimize_for_target_gateset(c, gateset=cirq.CZTargetGateset())
c3 = cirq.merge_single_qubit_gates_to_phxz(c)
```
- Cirq transformers replace older cirq.google optimizers; check cirq version docs.

## Gotchas
- Verify equivalence with cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent.

## Self-check
Compile a Toffoli to CZ+PhasedXZ and test equivalence.
