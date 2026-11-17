---
id: computing-software.software-engineering.hpc-parallel-computing.modules-lmod
name: modules-lmod
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, module-load, module-avail, modulepath, environment-modules, lmod, spack, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Software access"
sources: ["https://lmod.readthedocs.io/en/latest/010_user.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment modules and Lmod

Goal: manage software stacks.
- `module avail`, `module load gcc/12 openmpi/4.1`, `module list`, `module purge`, `module spider`.
- Load modules inside job scripts so the job records its software environment.
Verify: `which mpicc` points to the intended module.

## Checked

2026-11-03. Confirmed against the official pages: module avail, load, list, purge and spider (Lmod user guide). Removed: advice to keep module loads out of .bashrc (the user guide documents startup-file setup) and the compiler/MPI ABI claim.

Method: documentation only; no commands were run.
