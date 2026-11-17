---
id: computing-software.cloud-infrastructure-engineering.kubernetes.admission-warnings-and-audit-annotations
name: admission-warnings-and-audit-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, admission-control, admission-warnings, audit-annotations, validatingadmissionpolicy, webhooks]
level: practitioner
status: docs-checked
description: "Return non-blocking warnings and audit annotations from admission webhooks and ValidatingAdmissionPolicy to roll out policies gently and leave an audit trail."
sources: ["https://kubernetes.io/blog/2020/09/03/warnings/", "https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/", "https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response", "https://kubernetes.io/docs/reference/labels-annotations-taints/audit-annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admission warnings and audit annotations

## Warnings
Returned to the client in HTTP `Warning` headers (code 299) and do not block the request; they can
accompany allowed or rejected responses. kubectl prints them; client-go logs them.

Webhook response:
```json
{"apiVersion":"admission.k8s.io/v1","kind":"AdmissionReview",
 "response":{"uid":"<uid>","allowed":true,
   "warnings":["image uses :latest; pin a tag or digest (policy img-001)"],
   "auditAnnotations":{"img-policy":"latest-tag"}}}
```
Keep each warning short (120 characters or fewer if possible), actionable, and without a "Warning:"
prefix. The API server may truncate individual messages over 256 characters and ignores further
warnings once more than 4096 characters have been added from all sources.

`auditAnnotations` is a string map added to the request's audit event; the API server prefixes
each key with the webhook name (for example `imagepolicy.example.com/error`).

## ValidatingAdmissionPolicy
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata: {name: require-limits-warn}
spec:
  policyName: require-limits
  validationActions: [Warn, Audit]       # later: [Deny]
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata: {name: require-limits}
spec:
  matchConstraints:
    resourceRules: [{apiGroups: [apps], apiVersions: [v1], operations: [CREATE, UPDATE], resources: [deployments]}]
  validations:
  - expression: "object.spec.template.spec.containers.all(c, has(c.resources.limits))"
    message: "all containers need resource limits"
  auditAnnotations:
  - key: missing-limits
    valueExpression: "'containers without limits in ' + object.metadata.name"
```
`Audit` writes the failure into the audit event (`validation.policy.admission.k8s.io/validation_failure`
annotation) so you can measure who would be blocked before switching to `Deny`.

## CI
The kubectl global flag `--warnings-as-errors` treats server warnings as errors and exits non-zero,
so it makes warnings fail pipelines (for example `kubectl apply -f x.yaml --warnings-as-errors`).

## Verify
`kubectl apply -f deploy-without-limits.yaml` succeeds and prints the warning; the audit log entry
for that request carries the annotation.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: webhook `warnings` behaviour and 120/256/4096 limits; `auditAnnotations` response field and key prefixing
(admission/v1 types.go); ValidatingAdmissionPolicy stable (`admissionregistration.k8s.io/v1`, v1.30), `validationActions`
Warn/Audit/Deny and the `validation.policy.admission.k8s.io/validation_failure` annotation; kubectl `--warnings-as-errors` flag (kubectl source).
Note: the docs say `Deny` and `Warn` may not be combined in one binding.
Method: documentation only; no commands were run.
