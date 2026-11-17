---
id: computing-software.software-engineering.hpc-parallel-computing.workflow-managers
name: workflow-managers
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, snakemake-slurm, nextflow-slurm, workflow-dag, snakemake, nextflow, parsl, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Pipelines"
sources: ["https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html", "https://docs.seqera.io/nextflow/executor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow managers on clusters

Goal: run many dependent tasks.
- Snakemake: `snakemake --executor slurm --jobs 100`; Nextflow: `process.executor = 'slurm'`.
Verify: DAG completes.

## Checked

2026-11-03. Confirmed against the official pages: Snakemake slurm executor invocation and Nextflow slurm executor setting. Removed: container-per-task and job-grouping advice, resume claim.

Method: documentation only; no commands were run.
