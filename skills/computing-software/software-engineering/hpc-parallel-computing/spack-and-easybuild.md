---
id: computing-software.software-engineering.hpc-parallel-computing.spack-and-easybuild
name: spack-and-easybuild
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, spack-install, spack-env, easybuild, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Building software"
sources: ["https://spack.readthedocs.io/en/latest/package_fundamentals.html", "https://spack.readthedocs.io/en/latest/environments.html", "https://docs.easybuild.io/using-easybuild/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spack and EasyBuild

Goal: build HPC software reproducibly.
- `spack install hdf5 +mpi ^openmpi`, `spack env create`, `spack concretize`; `eb HPL-2.3-foss-2021b.eb --robot`.
- Spack can use externally installed packages for system software.
- Record the spec (`spack spec`) with results.
Verify: `spack find` shows the built spec.

## Checked

2026-11-03. Confirmed against the official pages: spack install with ^ dependency specs, env create, concretize, spec, find, externals; eb with --robot (EasyBuild usage page). Removed: spack find -lv flags and the system MPI/CUDA example.

Method: documentation only; no commands were run.
