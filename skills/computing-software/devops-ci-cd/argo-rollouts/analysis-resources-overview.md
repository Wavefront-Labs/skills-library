---
id: computing-software.devops-ci-cd.argo-rollouts.analysis-resources-overview
name: analysis-resources-overview
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [analysis, analysistemplate, clusteranalysistemplate, analysisrun, experiment, crd, argo-rollouts]
level: intro
status: docs-checked
description: "Know the five Argo Rollouts CRDs and which ones carry analysis logic; new metric integrations must be plugins."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Progressive delivery in Argo Rollouts is driven by five custom resources.

- **Rollout**: drop-in replacement for a Deployment with blueGreen and canary strategies; those strategies can create AnalysisRuns and Experiments during an update.
- **AnalysisTemplate**: defines how to perform an analysis: the metrics, their frequency, and the values counted as successful or failed. It can take arguments.
- **ClusterAnalysisTemplate**: like an AnalysisTemplate but cluster-scoped, usable by any Rollout in any namespace.
- **AnalysisRun**: an instantiation of a template. Like a Job, it eventually completes as Successful, Failed or Inconclusive, and the result affects whether the update continues, aborts or pauses.
- **Experiment**: a limited run of one or more ReplicaSets for analysis, for a fixed duration or until stopped. It can run AnalysisRuns alongside.

The docs state that no new metric integrations are accepted in the core controller. A brand new metric integration must be written as a plugin (see the metric-provider-and-step-plugins skill), because the project is moving to a plugin architecture to keep the core small.

Analysis can run in the background during canary steps, inline as a step, or before and after blue-green promotion (pre-promotion and post-promotion analysis).

Verify by listing the AnalysisTemplate, ClusterAnalysisTemplate, AnalysisRun and Experiment objects in the cluster.

## Checked

2026-11-08. Confirmed against the Argo Rollouts analysis page (read in full): the five CRDs, the plugin-only rule for new metric integrations, and the pre and post promotion forms.

Removed or corrected: dropped the claim that analysis is optional with external checks through the CLI and API (not on the cited page) and the kubectl get command for the resources.

Method: documentation only; no commands were run.
