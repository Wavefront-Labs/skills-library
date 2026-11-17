---
id: computing-software.devops-ci-cd.argo-cd.ignore-differences-json-pointers-and-jq
name: ignore-differences-json-pointers-and-jq
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, json-pointers, jq-path-expressions, ignore-differences, respect-ignore-differences]
level: practitioner
status: docs-checked
description: "Silence expected drift in Argo CD with ignoreDifferences: jsonPointers vs jqPathExpressions, targeting by group/kind/name, and RespectIgnoreDifferences on sync."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#respect-ignore-difference-configs", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_diff/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ignoreDifferences: jsonPointers and jqPathExpressions

```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers: [/spec/replicas]                  # HPA owns replicas
    - group: admissionregistration.k8s.io
      kind: MutatingWebhookConfiguration
      jqPathExpressions: ['.webhooks[]?.clientConfig.caBundle']   # injected by cert-manager
    - group: ""
      kind: ConfigMap
      name: feature-flags
      namespace: app
      jsonPointers: [/data/rollout-percent]
    - group: apps
      kind: Deployment
      jqPathExpressions:
        - '.spec.template.spec.containers[] | select(.name == "istio-proxy")'
  syncPolicy:
    syncOptions: [RespectIgnoreDifferences=true]
```

## jsonPointers vs jq
- JSON Pointer: exact paths; a `/` inside a key is written `~1` (`/metadata/annotations/example.com~1hash`; RFC 6901 writes `~` as `~0`). Cannot express "every element where...".
- jq path expressions: arrays, selects, optional `?`. Each evaluation is time-limited (default 1 s, see the jq normalizer timeout skill).
- `group` is the Kubernetes API group without the version (`""` is the core group); `name` and `namespace` narrow the match, otherwise all resources of the kind match.

## RespectIgnoreDifferences
By default `ignoreDifferences` is only used to compute the diff, so a sync still applies Git's value. With the `RespectIgnoreDifferences=true` sync option, Argo CD also pre-patches the desired state during sync so ignored fields keep the live value.
Caveat: only effective when the resource already exists in the cluster; on creation the desired state is applied as-is.

## Gotchas
- Best fix is removing the field from Git (do not set `replicas` when an HPA owns it).
- Over-broad ignores hide real drift — scope by name where possible.

## Verify
- [ ] `argocd app diff <app>` shows no diff for the ignored field; app stays Synced while HPA scales.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `ignoreDifferences` fields (`group`, `kind`, `name`, `namespace`, `jsonPointers`, `jqPathExpressions`), `~1` escape, `RespectIgnoreDifferences` semantics and its create-time caveat, system-level MutatingWebhookConfiguration `caBundle` example, jq timeout default 1 s from the CLI flag help. Removed unconfirmed slowness remark.

Method: documentation only; no commands were run.
