---
id: computing-software.data-science-and-analytics.jupyter-notebooks.kernel-management-restarts
name: kernel-management-restarts
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [kernel-restart, kernel-interrupt, hidden-state]
level: intro
status: draft
description: "Recover from hung or stale kernels and avoid hidden state by restarting and running all cells before trusting results."
sources:
  - https://docs.jupyter.org/en/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kernel hygiene
- Interrupt (I, I) stops a running cell; Restart (0, 0) clears all state.
- Before sharing: Restart Kernel and Run All Cells; fix any cell that only worked because of earlier out-of-order execution.
- Free memory: `del big; import gc; gc.collect()`, or restart.
## Gotchas
- Execution counters out of order (3, 1, 7) indicate hidden state.
- Long jobs belong in scripts or papermill, not an open browser tab.
## Verify
- [ ] Run All from a fresh kernel finishes without errors and the outputs match.
