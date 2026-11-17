---
id: computing-software.devops-ci-cd.argocd-image-updater.multi-cluster-and-multiple-instances
name: multi-cluster-and-multiple-instances
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, multi-cluster, controller-placement, multiple-instances, team-isolation, argocd-user]
level: practitioner
status: docs-checked
description: "Place the controller and ImageUpdater CRs on the Argo CD control-plane cluster, and run several isolated instances per team without them touching the same applications."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-cluster placement and multiple instances

Multi-cluster: if Argo CD runs on a central cluster A and deploys Applications to cluster B, then:

- the Image Updater controller must be installed on cluster A
- every `ImageUpdater` CR must also be created on cluster A

The controller cannot discover `ImageUpdater` CRs created on cluster B. In short, the controller and its CRs live with the Argo CD `Application` resources, not with the deployed workloads. Related limitation from the overview: image pull secrets must exist in the cluster where the updater runs (or one it can access); fetching them from other clusters is not possible.

Multiple instances: several instances can share one cluster, for example so application teams manage their own apps, but they must not operate on the same set of applications. Make sure that:

- each instance runs in its own namespace
- each instance has a dedicated user in Argo CD with dedicated RBAC permissions
- RBAC is set up so instances cannot interfere with each other's managed resources

Related trap: two `ImageUpdater` CRs whose `namePattern` rules match the same application overwrite each other every cycle; keep one CR per application.

## Checked

2026-11-04. Confirmed against installation.md (Multi-Cluster Environments, Running multiple instances), the docs index page (pull secrets limitation) and applications.md (multiple CR conflict warning). Removed a generic self-check line the pages do not state.

Method: documentation only; no commands were run.
