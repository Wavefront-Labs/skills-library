---
id: computing-software.cloud-infrastructure-engineering.kyverno.policy-reports
name: policy-reports
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [policyreport, clusterpolicyreport, allowedresults, enablereporting, openreports, background-scan]
level: practitioner
status: docs-checked
description: "Read and tune Kyverno policy reports: report kinds, result values, reporting flags, background scan limits and what reports never show."
sources:
  - https://kyverno.io/docs/guides/reports/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kinds: `PolicyReport` (namespaced) and `ClusterPolicyReport` in `wgpolicyk8s.io/v1alpha2`. Intermediate `AdmissionReport`/`ClusterAdmissionReport` and `BackgroundScanReport`/`ClusterBackgroundScanReport` are merged automatically. OpenReports (`openreports.io/v1alpha1` `Report`, alpha since 1.15) turns on with `--openreportsEnabled` or Helm `openreports.enabled=true`. ValidatingAdmissionPolicy reports need `--validatingAdmissionPolicyReports` (default false). Reports cover validate, mutate, generate and verifyImages rules.

Results: `pass`; `fail`; `skip` (preconditions unmet or an exception applied); `warn` (policy annotation `policies.kyverno.io/scored: "false"` converts fail to warn); `error` (variable substitution failed outside preconditions). `kubectl get polr -o wide` shows the counts; report names are random.

Flags: `--enableReporting=validate,mutate,mutateExisting,generate,imageVerify`; `--allowedResults` (1.17+, default all five; `--allowedResults=fail` cuts etcd load); background scan interval defaults to one hour. Policy `spec.background: false` skips scanning; label `reports.kyverno.io/disabled` on a policy (1.16+) suppresses its reports. The reports controller needs get, list, watch on scanned resources.

Limits:
- Reports show current state only and vanish with the resource.
- Under `Enforce` a blocked resource gets no `fail` entry; use metrics or events.
- `Pod/exec` is not reported.
- Background scans cannot evaluate `request.userInfo`, Roles, ClusterRoles or Subjects (set `background: false`), ignore the ConfigMap namespace selector, skip generate and mutate rules, and never block existing resources.
- A sibling `pass` can mask a conditional-anchor `skip`.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
