---
id: computing-software.devops-ci-cd.argo-rollouts.upgrade-controller
name: upgrade-controller
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [upgrade, controller, install, in-flight-rollouts, argo-rollouts]
level: practitioner
status: docs-checked
description: "Upgrade the Argo Rollouts controller safely, knowing it holds no external state and resumes in-flight rollouts."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/installation/
  - https://argo-rollouts.readthedocs.io/en/stable/FAQ/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Argo Rollouts is a Kubernetes controller that keeps no external state, and it is active only while deployments are happening. That makes upgrades simple.

The documented procedure:

1. Find a period when no deployments are happening.
2. Delete the previous version of the controller and apply or install the new one.
3. When the next Rollout takes place, the new controller is activated.

If rollouts are in flight while you upgrade, the docs state you should not see downtime: current Rollouts are paused, and as soon as the new controller becomes active it resumes all in-flight deployments.

Practical checklist:

- Check which Kubernetes versions the target release is tested against. The docs point to the e2e testing workflow file (`.github/workflows/testing.yaml`) in the repository; switch to the tag of the release you want to see its tested versions.
- `namespace-install.yaml` does not include the CRDs; they are installed separately from the `manifests/crds` directory (the docs give `kubectl apply --server-side -k` against that path).
- The plugin's version is shown by `kubectl argo rollouts version`; the FAQ advises keeping the plugin reasonably current because older plugins may not understand new Rollout fields.
- If you installed into a namespace other than `argo-rollouts`, `install.yaml`'s ClusterRoleBinding service account namespace must be updated to match.

Verify: the controller pod in its namespace runs the new image, and existing Rollouts resume (the plugin's `get rollout` shows their status).

## Checked

2026-11-08. Confirmed against the Argo Rollouts installation page (read in full): no external state, the three upgrade steps, in-flight rollouts pause and resume, supported versions pointer, namespace-install CRDs, ClusterRoleBinding tip. Version skew is from the FAQ (read in full) and get rollout from the kubectl plugin page (read in full).

Removed or corrected: removed the instruction to re-apply CRDs after upgrade, the instruction to upgrade the plugin to match, and the kubectl get pods and list rollouts verify commands (not documented).

Method: documentation only; no commands were run.
