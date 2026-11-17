---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-configure-hp-experiment
name: kubeflow-katib-configure-hp-experiment
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [hyperparameter-tuning, objective, parallel-trial-count, max-trial-count, metric-strategies, experiment-yaml]
level: practitioner
status: docs-checked
description: "Write a Katib hyperparameter tuning Experiment spec: objective and metricStrategies, algorithm, trial counts, parameters, trialTemplate, and the Istio sidecar caveat."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/hp-tuning/configure-experiment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib configure hp experiment

Package training code as a container image unless you use the SDK `tune` API. The Experiment YAML defines:

- **objective**: `type` (maximize or minimize), `objectiveMetricName`, optional `additionalMetricNames` and `goal`. The best value and its parameters appear in `.status.currentOptimalTrial.parameterAssignments`. Without a `goal`, the Experiment runs until `maxTrialCount` successful Trials.
- **metricStrategies**: per-metric rule (`min`, `max` or `latest`) for extracting a Trial's value. Default equals the objective type. Example: `accuracy` with strategy `latest` compares the latest reported accuracy of each Trial.
- **algorithm**: for example random, grid, Bayesian optimization.
- **parallelTrialCount**: concurrent Trials, default 3.
- **maxTrialCount**: total Trials; if omitted, runs until the goal or failure limit.
- **maxFailedTrialCount**: Trials with status `Failed` or `MetricsUnavailable` count; reaching the limit fails the Experiment.
- **parameters**: name, type (`int`, `double`, `categorical`) and feasible range or list.
- **trialTemplate**: `trialSpec` with `trialParameters`, and `primaryContainerName`.

Istio: the page says the example Experiment does not work with Istio sidecar injection because Trials need internet access to download datasets. With Kubeflow Community Distribution, add the annotation `"sidecar.istio.io/inject": "false"` under `spec.template.metadata.annotations` of the Job in `trialSpec`. For PyTorchJob or other Training Operator jobs the page links to separate instructions.

Run the random-search example with `kubectl create -f` on the Katib repo `examples/v1beta1/hp-tuning/random.yaml`, then `kubectl -n kubeflow get experiment random -o yaml` to read `status`.

## Checked

2026-11-08. Confirmed against the HP tuning Experiment guide: objective, metricStrategies, parallelTrialCount default 3, maxTrialCount and maxFailedTrialCount behaviour, parameter types, trialTemplate fields, the Istio annotation and the example commands. Removed the unsupported replica-template detail for training operator jobs.
Method: docs-only read of cited pages, 2026-11-08
