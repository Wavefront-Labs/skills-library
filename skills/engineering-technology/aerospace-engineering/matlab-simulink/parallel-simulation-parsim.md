---
id: engineering-technology.aerospace-engineering.matlab-simulink.parallel-simulation-parsim
name: parallel-simulation-parsim
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, monte-carlo-dispersions, monte-carlo, parsim, simulation-input, parallel-computing, batch-simulation]
level: practitioner
status: docs-checked
description: "Run many Simulink simulations in parallel with Simulink.SimulationInput and parsim, with per-run variables, shipped files and failure handling."
sources:
  - https://www.mathworks.com/help/simulink/slref/parsim.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Parallel simulation with parsim

**Goal:** thousands of runs with traceable inputs and outputs.

## Pattern
```matlab
N = 500;
in(1:N) = Simulink.SimulationInput('myModel');
for k = 1:N
    in(k) = in(k).setVariable('mass', samples(k,1));
    in(k) = in(k).setVariable('cgx',  samples(k,2));
    in(k) = in(k).setModelParameter('StopTime', '120');
end
out = parsim(in, ShowProgress="on");
```
`parsim` returns an array of `Simulink.SimulationOutput` objects. Extract metrics per run into a table.

## Practice
- `setPreSimFcn` and `setPostSimFcn` are `Simulink.SimulationInput` methods; see their reference pages for how to
  use them for initialisation and metric extraction.
- Check each output for failed runs and re-run them; report the failure count.
- Save the inputs table with the results.

## Gotchas
- `TransferBaseWorkspaceVariables` defaults to "off". Setting it to "on" sends everything in the base workspace to
  the workers, which the page does not recommend for large-scale simulations; prefer `setVariable` per run.
- `AttachedFiles` (a cell array of character vectors) attaches extra files to the parallel pool; From File blocks
  cannot load MAT files from subdirectories.

## Verify
- [ ] A single-run `sim` result equals the matching `parsim` element.

## Checked

2026-11-01. Confirmed on the MathWorks parsim page: `simOut = parsim(in,Name=Value)` syntax, `ShowProgress`
(default "on"), `TransferBaseWorkspaceVariables` (default "off", not recommended at scale), `AttachedFiles`,
`Simulink.SimulationOutput` array result, and that `setVariable`, `setModelParameter`, `setPreSimFcn` and
`setPostSimFcn` are `Simulink.SimulationInput` methods. Removed because not on the page: `out(k).logsout`,
`out(k).ErrorMessage`, large-memory and worker-path remarks, and the base-workspace-callback claim.
Method: documentation only; no commands were run.
