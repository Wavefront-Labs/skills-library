---
id: computing-software.ai-ml-engineering.model-training.ml-reproducibility-checklist
name: ml-reproducibility-checklist
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, reproducibility-checklist, ml-reporting, neurips-checklist, model-cards, experiment-reporting, statistical-significance]
level: practitioner
status: draft
description: "Apply an ML reproducibility checklist before reporting results: data and code availability, splits, hyperparameter search, seeds and variance, compute and statistical claims."
sources:
  - https://neurips.cc/public/guides/PaperChecklist
  - https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf
  - https://arxiv.org/abs/2003.12206
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ML reproducibility checklist for reports

Based on the NeurIPS paper checklist and Pineau et al.'s reproducibility checklist, adapted for internal reports and model reviews.

## Data
- [ ] Source, version/snapshot date and licence of each dataset; how it was collected and labelled.
- [ ] Preprocessing steps (with code), exclusions and their counts.
- [ ] Exact train/validation/test split definition (IDs or seeded procedure); split method justified (time, group, stratified).
- [ ] Known biases, label noise estimate, and overlap/contamination checks between splits and with pretraining data.

## Code and environment
- [ ] Repository commit hash; one command reproduces the main result.
- [ ] Environment lock (requirements/conda lock/container digest), hardware type and count.
- [ ] Config files for every reported run (not just the best).

## Training and tuning
- [ ] Model architecture, parameter count, initialisation/pretrained checkpoint (with revision).
- [ ] Hyperparameter search: space, method, number of trials, selection metric and the split used for selection. Baselines tuned with comparable effort.
- [ ] Final hyperparameters listed.
- [ ] Compute: GPU hours per run and for the whole project including search.

## Results
- [ ] Number of runs with different seeds per configuration; report mean and standard deviation or confidence intervals, not best seed.
- [ ] Statistical test or bootstrap CI for claimed improvements; effect size in context of seed variance.
- [ ] Metrics precisely defined (averaging, thresholds, k for top-k); evaluation code provided.
- [ ] Baselines: simple (majority/linear), previous production model, and published SOTA where relevant.
- [ ] Slice/subgroup metrics and failure cases; ablations for each claimed component.
- [ ] Test set used once at the end; any repeated test use disclosed.

## Claims and limits
- [ ] Claims match evidence (scope of data, languages, populations).
- [ ] Limitations and conditions where the model fails.
- [ ] Ethical/safety considerations and intended use (model card).

## How to use it
- Copy into the report template; reviewers block sign-off on unchecked items without justification.
- Automate what you can: log seeds, configs, environment and data versions with the experiment tracker so the checklist is mostly filled from metadata.
- Run a "fresh clone" reproduction by someone else before publishing or launching.
