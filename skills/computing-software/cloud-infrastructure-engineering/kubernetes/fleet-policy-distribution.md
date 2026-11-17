---
id: computing-software.cloud-infrastructure-engineering.kubernetes.fleet-policy-distribution
name: fleet-policy-distribution
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-cluster, fleet-policy, kyverno, gitops, policy-reports]
level: practitioner
status: docs-checked
description: "Distribute the same admission policies to every cluster in a fleet with GitOps generators, roll them out in audit mode first and aggregate policy reports centrally."
sources: ["https://kyverno.io/docs/policy-types/overview/", "https://kyverno.io/docs/guides/reports/", "https://open-policy-agent.github.io/gatekeeper/website/docs/violations/", "https://open-policy-agent.github.io/gatekeeper/website/docs/audit/", "https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/Generators-Cluster/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributing policy across a fleet

## Store policies once, deliver everywhere
Argo CD ApplicationSet with the cluster generator:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata: {name: baseline-policies, namespace: argocd}
spec:
  generators:
  - clusters:
      selector: {matchLabels: {policy-tier: standard}}
  template:
    metadata: {name: 'policies-{{name}}'}
    spec:
      project: platform
      source: {repoURL: https://git.example.com/platform/policies.git, targetRevision: main, path: 'kyverno/{{metadata.labels.env}}'}
      destination: {server: '{{server}}', namespace: kyverno}
      syncPolicy: {automated: {prune: true, selfHeal: true}}
```
Rancher Fleet `GitRepo` targets can do the same job (see `rancher-fleet-management`).

## Roll out safely
1. Ship new policies in a non-blocking mode to all clusters: Kyverno `failureAction: Audit` on the
   validate rule (`spec.validationFailureAction` is deprecated; `ValidatingPolicy` uses `validationActions`),
   or Gatekeeper `enforcementAction: dryrun` on the constraint (default is `deny`).
2. Collect violations for a week; fix workloads or add scoped exceptions.
3. Switch to Enforce per environment label: dev first, then staging, then prod.

## Aggregate results
Kyverno writes `PolicyReport` resources (API group `wgpolicyk8s.io`; `kubectl get policyreport -A`) per cluster, from
admission events and background scans. Policy Reporter is a Kyverno sub-project that manages policy reports
in-cluster with a web UI (its forwarding targets were not checked). Gatekeeper lists audit violations in each
constraint's `status` field and exports the `gatekeeper_violations` Prometheus metric. Add the cluster name
when aggregating reports centrally.

## Exceptions
Keep Kyverno `PolicyException` resources (stable since v1.19 per the Kyverno policy-types overview) or Gatekeeper
exempt namespaces in the same repo, per cluster overlay.

## Verify
A policy commit reaches every selected cluster (the generated Applications show Synced), and a test
violation appears in the central report tagged with its cluster.

Note: the Kyverno docs mark `ClusterPolicy` (`kyverno.io/v1`) as deprecated in v1.19 and removed in v1.20, with
`ValidatingPolicy` (`policies.kyverno.io/v1`) as the stable replacement; check which policy type your Kyverno
release supports before copying any `ClusterPolicy` examples.

## Checked

2026-10-26, against Kyverno docs (kyverno/website, src/content/docs, last push 2026-10-23: policy-types overview, validate rules, CRD reference, reports guide), Gatekeeper docs (violations, audit) and the Argo CD ApplicationSet cluster generator docs. Confirmed: Kyverno `failureAction` on validate rules and the deprecation of `spec.validationFailureAction`, ClusterPolicy deprecation timeline, `ValidatingPolicy` and `PolicyException` status, PolicyReport resources and kubectl command, Policy Reporter is an in-cluster report manager with a UI, Gatekeeper `enforcementAction: dryrun` (default deny), constraint status and `gatekeeper_violations`, ApplicationSet cluster-generator label fields such as `metadata.labels.<key>`. Removed unconfirmed claims about Flux, OCM, GKE Config Sync and Azure Policy equivalents, Policy Reporter push targets, and annotation-based exception expiry.

Method: documentation only; no commands were run.
