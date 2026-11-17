---
id: computing-software.devops-ci-cd.argo-cd.migrating-resource-tracking-method
name: migrating-resource-tracking-method
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, tracking-method-migration, resource-tracking, annotation-tracking]
level: advanced
status: docs-checked
description: "Switch Argo CD from label to annotation (or annotation+label) resource tracking safely: what changes, the one-time resync, and avoiding orphaned or pruned resources."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/resource_tracking/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/2.14-3.0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating resource tracking method

Argo CD 3.0 changed the default from label-based to annotation-based tracking (`argocd.argoproj.io/tracking-id`). Annotation tracking avoids the 63-character label-value truncation and
conflicts with other tools that set `app.kubernetes.io/instance` themselves. The 3.0 upgrade notes say it is more reliable because external code can copy tracking labels between resources.

## Setting
```yaml
# argocd-cm
application.resourceTrackingMethod: annotation      # label | annotation | annotation+label
```

## Safe migration
1. Upgrade/set the method in a maintenance window. Disable auto-prune temporarily
   (`prune: false` or a deny sync window) on critical apps.
2. Per the 3.0 upgrade notes, apps are not marked OutOfSync merely because the labels are absent; the tracking annotation appears on a resource only after a new Git commit or an explicit sync. Check first whether `application.resourceTrackingMethod` is unset or `label` (then you are affected) and whether any app uses `ApplyOutOfSyncOnly=true`: those need an explicit sync right after the upgrade or they are likely to leave orphan resources.
3. Sync each app so Argo writes the tracking annotation. Known edge case: if the first sync after switching deletes a resource, Argo CD may not recognise it as managed and will not delete it, so avoid pruning in that first sync.
   ```bash
   argocd app list -o name | xargs -n1 argocd app sync
   ```
4. Verify `argocd app diff` is clean, then re-enable pruning.
`annotation+label` keeps writing the label for tools that select on it (dashboards, NetworkPolicies).

## Gotchas
- Resources created by operators that copied the instance label are no longer treated as owned:
  good (fewer false "managed" resources), but check orphan warnings.
- To opt out of annotation tracking set `application.resourceTrackingMethod: label`; the docs say there are no plans to remove label tracking.
- Resources tracked by label but not managed by Argo CD (for example ones annotated to be ignored or not pruned) need tracking annotations constructed by hand, which is not an officially supported feature.

## Verify
- [ ] `kubectl get deploy x -o jsonpath='{.metadata.annotations.argocd\.argoproj\.io/tracking-id}'` returns `app:apps/Deployment:ns/x`.

## Checked

2026-11-02. Confirmed against the Argo CD Resource Tracking page and the 2.14 to 3.0 upgrade notes: annotation default in 3.0, argocd.argoproj.io/tracking-id format, label | annotation | annotation+label values in argocd-cm, ApplyOutOfSyncOnly caveat, orphan edge case on first sync, label opt-out. Fixed: the claim that apps show OutOfSync after the switch (docs say they do not); the Helm-specific cause; the --prune=false --async sync flags (not in the pages read; use the argocd app sync reference). Removed: installationID advice and the flip-flop claim (not stated). Kept the 63-character label limit as the docs say annotation+label truncates label values over 63 characters.

Method: documentation only; no commands were run.
