---
id: computing-software.devops-ci-cd.argo-cd.system-level-diffing-customizations
name: system-level-diffing-customizations
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, resource-compare-options, system-level-diffing, resource-customizations, ignore-resource-updates]
level: advanced
status: docs-checked
description: "Configure Argo CD diffing once for all apps in argocd-cm: per-kind ignoreDifferences keys, the all-resources key, and ignoreResourceUpdates to cut reconcile load."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/reconcile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System-level diffing customisations

## 1. Per kind
```yaml
# argocd-cm
data:
  resource.customizations.ignoreDifferences.admissionregistration.k8s.io_MutatingWebhookConfiguration: |
    jqPathExpressions:
      - '.webhooks[]?.clientConfig.caBundle'
  resource.customizations.ignoreDifferences.apps_Deployment: |
    jsonPointers:
      - /spec/replicas
```
Key format: `resource.customizations.ignoreDifferences.<group>_<Kind>` (as in `apps_Deployment`).

## 2. All resources
```yaml
  resource.customizations.ignoreDifferences.all: |
    managedFieldsManagers:
      - kube-controller-manager
```

## 3. Reduce reconcile churn: ignoreResourceUpdates
Diff ignores do not stop resource updates from triggering app refreshes. `ignoreResourceUpdates` ignores updates at given JSON paths to cut unnecessary reconciles. It is on by default (`resource.ignoreResourceUpdatesEnabled` defaults to true) and applies only to tracked resources of an application:
```yaml
  # resource.ignoreResourceUpdatesEnabled: 'false'   # opt out; default is true
  resource.customizations.ignoreResourceUpdates.all: |
    jsonPointers:
      - /status
  resource.customizations.ignoreResourceUpdates.argoproj.io_Application: |
    jqPathExpressions:
      - '.metadata.annotations."notified.notifications.argoproj.io"'
```

## 4. Notes
- Prefer system-level config for cluster-wide noise (webhooks, cert injection) and app-level for app specifics.
- Keep `argocd-cm` in Git and review changes to these blocks.

## Verify
- [ ] Known noisy kinds stay Synced after the change, and refreshes triggered by the ignored paths stop.

## Checked

2026-10-28. Confirmed against the Argo CD diffing and reconcile pages: resource.customizations.ignoreDifferences.<group>_<Kind> keys, the .all key with managedFieldsManagers, ignoreResourceUpdates.all and argoproj.io_Application keys, tracked-resources-only behaviour. Corrected: ignoreResourceUpdatesEnabled is true by default (the skill presented it as opt-in). Removed: Secret core-group key, last-applied annotation pointer, argocd_app_reconcile_count metric, restart and hard-refresh notes.

Method: documentation only; no commands were run.
