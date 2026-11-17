---
id: natural-sciences.biology.bioinformatics.reproducible-analysis-pipeline
name: reproducible-analysis-pipeline
category: natural-sciences
field: biology
product: bioinformatics
tags: [bioinformatics, pipeline, workflow-manager, snakemake, nextflow, nf-core, conda, bioconda, mamba, docker, singularity, apptainer, containers, reproducibility, version-pinning, reference-genome, genome-build, grch38, annotation-version, fastqc, multiqc, md5sum, checksums, raw-data, provenance, hpc, slurm]
level: practitioner
status: gated
description: "Build a bioinformatics analysis someone else can re-run: immutable raw data, pinned tools via conda/containers, a workflow manager, recorded genome builds, checksums and MultiQC."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A reproducible bioinformatics analysis pipeline

**Goal:** an analysis that gives the same answer when a colleague (or you in a year)
re-runs it from raw data, and whose every output can be traced back to the exact
inputs, tool versions and reference files that made it.

## 1. Lay out the project
```
project/
  raw/          # read-only. Never edited, never overwritten
  ref/          # genome FASTA, annotation GTF/GFF, indices — with a README of versions
  config/       # sample sheet, parameters (YAML)
  workflow/     # Snakefile or main.nf, rules/modules
  envs/         # conda env YAMLs or container definitions
  results/      # generated; deletable and re-creatable
  logs/
```
Make `raw/` read-only (`chmod -R a-w raw/`) and keep checksums:
`md5sum raw/*.fastq.gz > raw/MD5SUMS`, then verify after every copy with
`md5sum -c raw/MD5SUMS`. Sequencing providers usually ship their own checksum file —
check against it on download.

## 2. Pin the software
- Use **conda/mamba with Bioconda** and write explicit versions in `envs/*.yaml`
  (`samtools=1.19`, not `samtools`). Channel order matters: conda-forge then bioconda,
  with strict channel priority, is the Bioconda-recommended setup (`conda config --add channels bioconda`, `--add channels conda-forge`, `--set channel_priority strict`; the `defaults` channel was dropped from the recommendation in August 2024, and Bioconda's front page also shows pixi with default channels conda-forge and bioconda).
- Or use **containers** (Docker; Apptainer/Singularity on HPC where Docker is not
  allowed). BioContainers publishes images for most Bioconda packages.
- Export what actually got installed: `conda env export > envs/lock-<date>.yaml`.

## 3. Use a workflow manager
**Snakemake** (Python-like rules, file-based) or **Nextflow** (channels/processes;
large curated **nf-core** pipeline collection). Either gives you:
- re-running only the steps whose inputs changed,
- per-rule environments/containers,
- cluster/cloud execution (SLURM, etc.) without rewriting,
- a dry-run (`snakemake -n`, run here with Snakemake 9.27.0 on a one-rule workflow; Nextflow `-preview` in recent versions (gated: unconfirmed, source is paywalled or blocked; Nextflow needs Java, not available here)) to see the plan.

Before writing your own RNA-seq, variant-calling or ATAC pipeline, check nf-core: a
community pipeline with tests and documentation is usually a better starting point.
Record the pipeline release (`-r 3.14.0`), not `master`.

## 4. Record the references
The single most common silent error is mixing genome builds or annotation versions.
- Write the build and source in `ref/README`: e.g. "GRCh38, Ensembl release 110,
  primary assembly" or "hg38 UCSC". Note chromosome naming (`chr1` vs `1`).
- Every index (BWA, STAR, salmon) must be built from the same FASTA and, for STAR/salmon,
  the same GTF used downstream.
- Never lift results between builds without a liftover step you document.

## 5. QC throughout
- **FastQC** on raw reads; trimming only if adapter content/quality demands it.
- Alignment stats (`samtools flagstat`, tool logs), duplication rate, insert size.
- **MultiQC** to aggregate all logs in one report — look at it per batch; outliers show
  up as a single line off the trend.

## 6. Make it re-runnable
- Version control `workflow/`, `config/`, `envs/` in git; never the data.
- Set random seeds for anything stochastic.
- Write a one-command entry point and a README stating the command, hardware used and
  expected runtime.
- Archive raw data to a public repository (SRA/ENA/GEO) on publication, and the code
  with a DOI (e.g. via Zenodo).

## Gotchas
- `conda install` into `base` and ad-hoc `pip install` break reproducibility — one
  environment per tool group, defined in files.
- Spreadsheet software silently converts gene names (SEPT2, MARCH1) into dates (Ziemann et al. 2016 found gene-list errors in about 19.6% of papers screened); HGNC has since renamed them (SEPT2 is now SEPTIN2 and MARCH1 is now MARCHF1, confirmed in the HGNC REST API). Read sample sheets as text.
- Paired-end files must stay in sync; filtering one mate without the other breaks aligners.
- Default parameters change between tool versions; your methods section needs versions.

Checked 2026-10-19: `md5sum -c` and `snakemake -n -s workflow/Snakefile` run; HGNC symbols and Bioconda commands fetched. The nf-core release number is an example; conda/container/FastQC/MultiQC practice was not run (gated: unconfirmed, source is paywalled or blocked).

Uncertain here: specific command flags differ between Snakemake/Nextflow major versions;
check the docs for the version you pin.

## Verify
- [ ] Raw data read-only with passing checksums.
- [ ] Every tool version pinned in a committed file; containers/envs listed.
- [ ] Genome build and annotation release written down and consistent across indices.
- [ ] A fresh clone + one command reproduces the key result table.
- [ ] MultiQC report reviewed; outlier samples explained or excluded with reason.
