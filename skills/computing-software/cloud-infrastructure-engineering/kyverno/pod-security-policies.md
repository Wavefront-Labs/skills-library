---
id: computing-software.cloud-infrastructure-engineering.kyverno.pod-security-policies
name: pod-security-policies
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [pod-security, pod-security-standards, kyverno-policies-chart, policygroups, kustomize, psp-migration]
level: intro
status: docs-checked
description: "Install Kyverno's Pod Security Standards policy set via kustomize or the kyverno-policies Helm chart, and know the PSP migration category."
sources:
  - https://kyverno.io/docs/guides/pod-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kyverno ships policies for every control in the Kubernetes Pod Security Standards, grouped into Privileged, Baseline and Restricted levels so each workload gets the right level.

Install all: with Kyverno and upstream kustomize present, `kustomize build https://github.com/kyverno/policies/pod-security | kubectl apply -f -`. Use upstream kustomize when customising; the version bundled in kubectl often fails with these policies.

Helm: add the Kyverno repo and install chart `kyverno/kyverno-policies` with `--set policyGroups=pod-security`. Policies are placed in namespace `kyverno-policies` by default, which can be changed.

PSP migration: a policy category replicates PodSecurityPolicy behaviour; a linked blog compares PodSecurityPolicy with Pod Security Admission.

Gaps: the page does not give the `podSecurity` validate rule syntax, versions or control exclusions. For those see the validate-rules skill (rule fields `level`, `version`, `exclude[]`) and the policy-exceptions skill (`podSecurity[]` in legacy exceptions). Note that `validate.podSecurity` is not supported in the CEL policy types, per the migration guide.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
