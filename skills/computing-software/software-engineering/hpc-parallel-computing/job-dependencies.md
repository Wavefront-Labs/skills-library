---
id: computing-software.software-engineering.hpc-parallel-computing.job-dependencies
name: job-dependencies
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, sbatch-dependency, afterok, slurm-chain, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Pipelines"
sources: ["https://slurm.schedmd.com/sbatch.html", "https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html", "https://docs.seqera.io/nextflow/executor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependencies and workflows

Goal: chain jobs.
- `jid=$(sbatch --parsable a.sh); sbatch --dependency=afterok:$jid b.sh`.
- Types include after, afterany, afternotok, afterok and singleton.
- For complex DAGs consider Snakemake or Nextflow with their Slurm executors.
Verify: dependent job starts only after success.

## Checked

2026-11-03. Confirmed against the official pages: --parsable, --dependency types (sbatch page), Snakemake and Nextflow Slurm executors (Snakemake plugin catalog, Nextflow executor docs). Removed: nothing removed.

Method: documentation only; no commands were run.
