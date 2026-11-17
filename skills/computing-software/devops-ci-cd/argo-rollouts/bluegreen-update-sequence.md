---
id: computing-software.devops-ci-cd.argo-rollouts.bluegreen-update-sequence
name: bluegreen-update-sequence
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [blue-green, promotion, prepromotionanalysis, postpromotionanalysis, sequence, argo-rollouts]
level: advanced
status: docs-checked
description: "Follow the exact ordered sequence of a blue-green update, including pre- and post-promotion analysis hooks."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this ordering to reason about where a blue-green rollout is stuck.

1. Steady state: revision 1 ReplicaSet is selected by both `activeService` and `previewService`.
2. You change the pod template.
3. A revision 2 ReplicaSet is created at size 0.
4. `previewService` is repointed to revision 2; `activeService` stays on revision 1.
5. Revision 2 scales to `spec.replicas`, or to `previewReplicaCount` if set.
6. When its pods are fully available, `prePromotionAnalysis` starts.
7. On success the rollout pauses if `autoPromotionEnabled` is false or `autoPromotionSeconds` is non-zero.
8. A user resumes it, or `autoPromotionSeconds` elapses.
9. If `previewReplicaCount` was used, revision 2 is scaled up to `spec.replicas`.
10. The rollout promotes: `activeService` now points at revision 2, so no Service selects revision 1.
11. `postPromotionAnalysis` begins.
12. When it succeeds, revision 2 is marked stable and the rollout is fully promoted.
13. After `scaleDownDelaySeconds` (default 30), revision 1 is scaled down.

Pre-promotion analysis can block the selector switch; its failure aborts the rollout. If post-promotion analysis fails or errors, the rollout enters an aborted state and switches traffic back to the previous stable ReplicaSet.

Verify by watching `kubectl argo rollouts get rollout NAME -w` and matching the printed phase to the step above.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts/.

Removed or corrected: nothing; the 13-step sequence matched the page.

Method: documentation only; no commands were run.
