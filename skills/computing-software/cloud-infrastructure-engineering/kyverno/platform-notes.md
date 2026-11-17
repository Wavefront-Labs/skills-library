---
id: computing-software.cloud-infrastructure-engineering.kyverno.platform-notes
name: platform-notes
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [argocd, openshift, eks, aks, serversidediff, webhookannotations, platform]
level: practitioner
status: docs-checked
description: "Apply Kyverno platform-specific settings for ArgoCD, OpenShift SCCs, EKS VPC CNI and the AKS Admission Enforcer."
sources:
  - https://kyverno.io/docs/installation/platform-notes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ArgoCD:
- Needs v2.10+ for `ServerSideDiff`. Enable per Application with annotation `argocd.argoproj.io/compare-options: ServerSideDiff=true,IncludeMutationWebhook=true`, or globally in the `argocd-cmd-params-cm` ConfigMap.
- Sync options: `ServerSideApply=true`, `CreateNamespace=true`; avoid `Replace=true`.
- Helm default `config.preserve=true` can show OutOfSync with App of Apps and block cleanup; use `config.preserve=false`.
- Optional Helm value `webhookLabels` with `app.kubernetes.io/managed-by: argocd`.
- Both tools set `app.kubernetes.io/instance`; configure a different ArgoCD tracking method.

OpenShift: the default SCC on 4.11 is `restricted-v2`. The chart's default pod `securityContext` can fail with "unable to validate against any security context constraint". Set the offending `securityContext` fields to `null` so OpenShift applies its SCC; on 4.11+ `restricted-v2` lets the chart deploy unmodified.

EKS (VPC CNI): with the operability strategy, exclude `kube-system` from webhooks. Risk: if all nodes go away (a node group scaled to zero) and a `Fail`-mode policy matches Pods, VPC CNI DaemonSet Pods may not start, blocking node bootstrap. Kyverno 1.12+ excludes `kube-system` by default.

AKS: the AKS Admission Enforcer may remove Kyverno's webhooks, causing reconciliation conflicts. Set Helm `config.webhookAnnotations` to include `"admissions.enforcer/disabled": true`; Kyverno 1.12+ sets it by default.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
