---
id: computing-software.devops-ci-cd.argo-cd.ignoring-hpa-managed-replicas
name: ignoring-hpa-managed-replicas
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, hpa-replicas-diff, ignoredifferences, diffing]
level: practitioner
status: docs-checked
description: "Stop Argo CD fighting a HorizontalPodAutoscaler over spec.replicas: remove replicas from manifests, ignoreDifferences, RespectIgnoreDifferences and server-side apply."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#respect-ignore-difference-configs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ignoring HPA-managed replicas

Symptom: Deployment shows OutOfSync on `spec.replicas`; with self-heal, Argo resets replicas to the
Git value and the HPA scales back up: pods churn.

## Best fix: omit replicas
Remove `spec.replicas` from the Deployment/Rollout manifest when an HPA manages it. Helm charts:
render `replicas` only when autoscaling is disabled:
```yaml
{{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
{{- end }}
```
Scale-safe approach: remove the field and add the ignore rule below in the same change.

## ignoreDifferences
```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers: [/spec/replicas]
    - group: argoproj.io
      kind: Rollout
      jsonPointers: [/spec/replicas]
  syncPolicy:
    syncOptions: [RespectIgnoreDifferences=true]
```
`RespectIgnoreDifferences=true` matters: by default `ignoreDifferences` only affects the diff, so a sync triggered by another change still applies the Git replicas value. The option is only effective for resources that already exist.

System-wide (argocd-cm):
```yaml
resource.customizations.ignoreDifferences.apps_Deployment: |
  jqPathExpressions: ['.spec.replicas']
```
Prefer per-app rules; global ignores hide real drift in apps without HPAs.

## Server-side apply
With `ServerSideApply=true` and no `replicas` in the manifest, Argo CD does not set the field, so the HPA's value stays. You can also ignore a controller's fields with `managedFieldsManagers` (see the managed-fields skill).
For HPA objects themselves, the HPA controller is known to reorder `spec.metrics`; order `spec.metrics` in Git the way the controller prefers (kubernetes issue 74099).

## Verify
- [ ] Scaling via HPA does not mark the app OutOfSync; a sync leaves current replica count untouched.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `ignoreDifferences` with `jsonPointers: [/spec/replicas]` for apps/Deployment, system-level `resource.customizations.ignoreDifferences.apps_Deployment` with `jqPathExpressions`, `RespectIgnoreDifferences` semantics, HPA `spec.metrics` reordering note. Removed unconfirmed client-side-apply and field-manager claims.

Method: documentation only; no commands were run.
