---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-concepts-architecture
name: kubeflow-katib-concepts-architecture
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [katib, experiment, suggestion, trial, worker, automl]
level: intro
status: docs-checked
description: "Katib AutoML concepts: Experiment, Suggestion, Trial, Worker, the control plane components, and what happens between creating an Experiment and finishing it."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/overview.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/reference/architecture.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/reference/experiment-cr.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib concepts architecture

Katib is the Kubernetes-native AutoML project in Kubeflow: hyperparameter tuning, early stopping and neural architecture search (NAS), agnostic to ML framework and language. NAS is described as alpha with limited support.

Core CRDs:
- **Experiment**: one tuning run (also called an optimization run). Main settings: the objective (metric plus maximize or minimize), the search space (hyperparameters with min/max or allowed values) and the search algorithm (for example Bayesian Optimization or Random Search).
- **Suggestion**: a set of hyperparameter values the tuning process proposed. Katib creates a Trial to evaluate it.
- **Trial**: one iteration, corresponding to one worker job instance with a list of parameter assignments (the Suggestion).
- **Worker**: the process that runs to evaluate a Trial and compute its objective value. It can be any Kubernetes resource or CRD; the Trial template guide shows how to support your own.

The overview says Katib integrates with Kubeflow Training Operator jobs such as PyTorchJob for distributed training, and can orchestrate workflows such as Argo Workflows and Tekton Pipelines.

Control plane components: `katib-controller` (manages the Experiment, Suggestion and Trial CRDs; if the certificate generator is enabled in Katib Config it creates self-signed certificates for the webhooks), `katib-ui`, `katib-db-manager` (gRPC API server for the Katib DB interface) and `katib-mysql` (MySQL backend that stores Experiment metrics).

Lifecycle after submitting an Experiment:
1. The mutating and validating webhooks set default values and validate the CR.
2. The Experiment controller creates the Suggestion; the Suggestion controller creates the algorithm deployment and service.
3. When the service is ready, it generates `spec.request - len(status.suggestions)` sets of hyperparameters, appended to `status.suggestions`.
4. The Experiment controller creates a Trial for each new set; the Trial controller generates the worker job from the Trial's `runSpec`.
5. The job controller (Kubernetes batch Job, Kubeflow TFJob, Tekton Pipeline and so on) creates Pods; the Katib Pod mutating webhook injects the metrics collector sidecar, which persists metrics to the Katib DB.
6. When training ends the Trial controller updates the Trial status, and the Experiment controller raises the Suggestion `request` if needed and repeats from step 3. The Experiment ends when a Trial meets an end condition: `maxTrialCount`, `maxFailedTrialCount` or `goal`.

## Checked

2026-11-08. Confirmed against the three cited pages (Katib overview, architecture, Experiment lifecycle): CRD definitions, control plane components, the lifecycle steps and end conditions. Removed the unsupported claim that Worker examples are Job/PyTorchJob/Tekton/Argo resources specifically (the pages name those only as integrations and job controllers).
Method: docs-only read of cited pages, 2026-11-08
