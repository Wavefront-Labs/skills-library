---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-admission-audit-annotations
name: opa-gatekeeper-admission-audit-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, audit-annotations, emit-admission-audit-annotations, api-server-audit, evaluation, vap]
level: sme
status: docs-checked
description: "Add Gatekeeper evaluation results to Kubernetes API server audit events with --emit-admission-audit-annotations and the include-success option."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/customize-startup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper admission audit annotations

`--emit-admission-audit-annotations` (alpha, off by default) adds audit annotations to validation requests that reach policy evaluation. By default only violations are annotated; add `--admission-audit-annotations-include-success=true` to annotate evaluations with zero violations too (it has no effect unless the first flag is on, and deny, warn and dryrun violations are annotated regardless). Requests skipped before evaluation, such as excluded namespaces, are not annotated.

The validating webhook returns one `evaluation` entry in `AdmissionResponse.auditAnnotations`; the API server prefixes it with the webhook name, giving `validation.gatekeeper.sh/evaluation` in the API audit event. Its versioned JSON holds the `allowed` decision, bounded summaries of deny, warn and dryrun violations, total and included counts, and a `truncated` flag. A clean success looks like `{"schemaVersion":"v1","allowed":true,"violations":[],"totalViolations":0,"includedViolations":0,"truncated":false}`.

For generated ValidatingAdmissionPolicyBindings, the `Audit` action is added alongside `Deny` or `Warn`, so failed native validations produce the standard `validation.policy.admission.k8s.io/validation_failure` annotation. In split deployments set both flags consistently on the webhook process and on the process running `generate`, and restart them after changing. API server audit logging must be at `Metadata` level or higher. These annotations do not create Event resources.

## Checked

2026-11-08: read the Emit API server audit annotations section of website/docs/customize-startup.md in the Gatekeeper repo. Confirmed the flags, defaults, the evaluation annotation and its JSON example, the VAP Audit action, split-deployment guidance and the Metadata audit level. Nothing removed.

Method: documentation only; no commands were run.
