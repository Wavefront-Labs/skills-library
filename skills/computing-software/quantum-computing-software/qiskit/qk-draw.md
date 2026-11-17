---
id: computing-software.quantum-computing-software.qiskit.qk-draw
name: qk-draw
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [circuit-visualization, qiskit-visualization]
level: intro
status: draft
description: "Draw circuits in text, mpl and latex styles and plot count histograms."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Circuit drawing and histograms
```python
qc.draw("mpl", fold=-1); qc.draw("text")
from qiskit.visualization import plot_histogram
plot_histogram(counts)
```
- mpl needs matplotlib and pylatexenc.

## Gotchas
- Draw output is little-endian top to bottom by register order; check bit labels.

## Self-check
Save a circuit image to a file with the filename argument.
