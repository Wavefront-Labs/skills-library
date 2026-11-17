---
id: computing-software.devops-ci-cd.argo-cd.ignore-aggregated-cluster-roles
name: ignore-aggregated-cluster-roles
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, ignore-aggregated-roles, aggregated-clusterrole-drift, aggregation-rule]
level: practitioner
status: docs-checked
description: "Stop aggregated ClusterRoles from showing permanent OutOfSync in Argo CD with resource.compareoptions ignoreAggregatedRoles, and what it changes."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/#aggregated-clusterroles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ignoreAggregatedRoles

## Problem
A ClusterRole with an `aggregationRule` has its `rules` filled in by the Kubernetes
clusterrole-aggregation controller from other roles' labels:
```yaml
kind: ClusterRole
metadata: { name: monitoring-view }
aggregationRule:
  clusterRoleSelectors:
    - matchLabels: { rbac.example.com/aggregate-to-monitoring: "true" }
rules: []          # Git says empty; live has dozens of rules
```
Argo CD compares Git `rules: []` with the populated live rules, so the app is reported **OutOfSync**.

## Fix (`argocd-cm`)
```yaml
data:
  resource.compareoptions: |
    ignoreAggregatedRoles: true
```
Argo CD then no longer detects the `rules` changes of aggregated ClusterRoles as an event that requires syncing.

## Notes
- Global setting in `argocd-cm`; applies to all apps. Alternative per app: `ignoreDifferences` on `rbac.authorization.k8s.io/ClusterRole` with `jsonPointers: [/rules]`, scoped by name.
- This setting sits next to `ignoreResourceStatusField` in `resource.compareoptions`; keep both keys in the same block.

## Verify
- [ ] Apps containing aggregated ClusterRoles report Synced after a refresh.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `resource.compareoptions` with `ignoreAggregatedRoles: true` and its documented effect (aggregated ClusterRole `rules` changes no longer cause a sync event), Kubernetes aggregated ClusterRole mechanism as named in the Argo CD page. Removed unconfirmed claims (rules wiped on sync, chart examples).

Method: documentation only; no commands were run.
