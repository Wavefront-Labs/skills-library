---
id: computing-software.devops-ci-cd.argo-rollouts.architecture-and-components
name: architecture-and-components
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [architecture, controller, rollout, replicaset, analysistemplate, argo-rollouts]
level: intro
status: docs-checked
description: "Map the moving parts of an Argo Rollouts deployment: controller, Rollout CR, ReplicaSets, Services, analysis resources, CLI and UI."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/architecture/
  - https://argo-rollouts.readthedocs.io/en/stable/concepts/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Knowing which object does what makes failures easy to localise.

**Controller.** Watches `Rollout` resources and drives the cluster to the state in the spec. It does not touch normal Deployments, so you can run it in a cluster that deploys other apps in other ways. Deployments must be migrated to Rollouts before the controller manages them.

**Rollout resource.** A custom resource mostly compatible with a Deployment, plus fields for steps, thresholds and strategy. It can replace a Deployment when you need blue-green, canary, ingress or mesh traffic routing, metric analysis, or automated promote/rollback.

**ReplicaSets.** Standard Kubernetes ReplicaSets, one per version, labelled with extra metadata so the controller can track them. They are fully managed; do not modify them with external tools.

**Services and Ingress.** Traffic enters through standard Service resources carrying extra metadata. A rollout may use separate Services for new only, old only, or both. Canaries can use meshes or ingresses for exact percentage splits, and several routers can be combined.

**AnalysisTemplate, ClusterAnalysisTemplate, AnalysisRun.** The template defines the metric queries and success conditions; an AnalysisRun is the instance attached to a rollout. Cluster-wide templates are shared across rollouts. Analysis can also be a Kubernetes Job or a web hook.

**CLI and dashboard.** Optional: the kubectl plugin and an integrated UI.

Verify by inspecting the Rollout, its ReplicaSets and any AnalysisRuns in the cluster; the kubectl plugin's `get rollout` shows them as a tree.

## Checked

2026-11-08. Confirmed against the Argo Rollouts architecture and concepts pages (both read in full): controller scope, Rollout resource, ReplicaSets, Services and Ingress, analysis resources, Job and web analysis, optional CLI and UI. The tree view is from the kubectl plugin page (read in full).

Removed or corrected: replaced the unsourced kubectl get verify command.

Method: documentation only; no commands were run.
