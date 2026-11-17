---
id: computing-software.ai-ml-engineering.mlops.ci-cd-for-ml-pipelines
name: ci-cd-for-ml-pipelines
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, ci-cd, continuous-training, continuous-integration, model-testing, data-validation, pipeline-orchestration, github-actions, dvc, artifact-promotion, reproducibility, gitops, model-deployment-pipeline]
level: advanced
status: draft
description: "CI/CD for ML: test data and models in the pipeline (not just code), gate promotion on evaluation thresholds, and keep training reproducible across environments."
sources:
  - https://ml-ops.org/content/mlops-principles
  - https://www.tensorflow.org/tfx/guide
  - https://dvc.org/doc
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CI/CD for ML pipelines — testing data and models, not just code

**Goal:** a pipeline where a code change, a data change, or a retrain all go through the same gates before reaching production, and a bad promotion is caught before users see it.

## 1. What "CI" means for ML, beyond unit tests
Standard software CI (lint, unit tests, build) is necessary but not sufficient — it never touches the thing that actually changes behavior: data and the trained artifact. A full ML CI pipeline adds:
- **Data validation tests**: schema checks (column types, allowed ranges, required columns present), row-count sanity bounds, and null-rate thresholds on every new training data pull — run these as a pipeline stage that fails the build, not a notebook cell someone runs manually. Great Expectations, TFX's `ExampleValidator`, or hand-rolled pandera schemas all work; the point is that it's automated and blocking.
- **Training smoke tests**: run the actual training code for a handful of steps on a tiny fixture dataset in CI on every PR — catches a broken loss function, a shape mismatch, or a dependency bump that silently changes behavior, in minutes instead of discovering it after a multi-hour cluster job.
- **Model evaluation gates**: after a real training run, compare the candidate's metrics against the current production model's metrics on a frozen, versioned test set — not just "did training complete." Promotion is blocked automatically if a key metric regresses beyond a documented tolerance, and per-segment checks run too (see computing-software.ai-ml-engineering.model-training.data-splits-and-evaluation): an aggregate metric can hide a regression on a minority segment.
- **Behavioral/invariance tests**: specific input→expected-output assertions that encode business rules a model must never violate (a loan model must not approve a negative income; a classifier's prediction must not flip when you perturb an irrelevant token) — these catch regressions aggregate metrics miss entirely.

## 2. Reproducibility is the dependency CI actually protects
- Pin everything that affects the trained artifact: code version (git SHA), data version (DVC/LakeFS hash or an immutable snapshot id, not "the latest table"), library versions (lockfile, not a loose requirements.txt), hardware/driver version if numerics are sensitive, and random seeds. Log all of these into the run's metadata (the experiment tracker — see computing-software.ai-ml-engineering.mlflow.experiment-tracking-and-model-registry) so any production model can be traced back to the exact inputs that produced it.
- Treat the training pipeline itself as versioned code with its own CI — a pipeline DAG change (reordering steps, changing a default hyperparameter) is a code change and should go through PR review and the smoke test, same as application code.
- **Continuous training vs continuous deployment are separate gates.** Automatically retraining on new data on a schedule is fine; automatically promoting that retrain to serve production traffic without the evaluation gate is how a bad data pull becomes a production incident. Keep a human or an automated-but-strict evaluation gate between "trained" and "serving."

## 3. Pipeline failure modes specific to ML
- **Silent schema drift upstream**: an upstream team renames or changes the type of a column feeding your pipeline; without a schema check, this doesn't fail the build, it just quietly changes what the model trains on. This is the single most common cause of "the model got worse and we don't know why."
- **Non-deterministic training masking a real regression**: if training isn't seeded and reproducible, a metric drop between runs could be noise or a real regression, and the gate becomes untrustworthy — fix the seeding before trusting thresholds, or set thresholds wide enough to account for measured run-to-run variance (measure it, don't guess it).
- **Artifact/environment mismatch at serving time**: a model trained with library version X served with library version Y can silently produce different predictions (different default hyperparameters, different floating-point behavior) — package the serving environment (container image) alongside the model artifact as one promoted unit, not independently.
- **Long pipeline runtimes starving CI feedback**: full retraining on every PR is often too slow/expensive to run synchronously — split into fast PR-time checks (smoke test, data validation on a sample) and slower scheduled/triggered full pipeline runs (nightly, or on data-version change), with the full run's evaluation gate blocking only the deploy step, not every PR.

## Verify
- [ ] Data schema/null-rate/range checks run as an automated, blocking pipeline stage on every new data version.
- [ ] A training smoke test on a tiny fixture dataset runs in CI on every code PR touching the training path.
- [ ] Promotion to production is blocked by an automated comparison against the current production model on a frozen eval set, including per-segment metrics.
- [ ] Code version, data version, library lockfile and seed are all logged per run and traceable from a production model back to its training inputs.
- [ ] Serving environment is packaged with the model artifact as one promoted unit.
- [ ] Continuous training and continuous deployment are gated separately — retraining does not auto-serve without passing evaluation.
