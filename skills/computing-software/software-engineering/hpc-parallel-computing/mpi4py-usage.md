---
id: computing-software.software-engineering.hpc-parallel-computing.mpi4py-usage
name: mpi4py-usage
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi4py-comm, mpi4py-buffers, mpi4py-allreduce, mpi4py, dask-jobqueue, numba-cuda, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "MPI from Python"
sources: ["https://mpi4py.readthedocs.io/en/stable/tutorial.html", "https://slurm.schedmd.com/mpi_guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mpi4py

Goal: use MPI in Python.
- `from mpi4py import MPI; comm = MPI.COMM_WORLD`; uppercase methods (`Send`, `Allreduce`) take buffer-like objects such as NumPy arrays and run at near C speed; lowercase methods pickle Python objects.
- Run with `mpiexec -n 4 python script.py`; under Slurm, `srun` can launch MPI programs when PMI/PMIx is configured.
Verify: allreduce result equals the NumPy sum.

## Checked

2026-11-03. Confirmed against the official pages: COMM_WORLD, uppercase buffer vs lowercase pickle methods, mpiexec launch (mpi4py tutorial), srun PMI launch (Slurm MPI guide). Removed: mpirun -n form (the tutorial uses mpiexec) and the build-against-system-MPI advice.

Method: documentation only; no commands were run.
