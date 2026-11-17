---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.kubernetes-admission-deny-rules
name: kubernetes-admission-deny-rules
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [kubernetes, admission-control, kube-mgmt, deny-rules, admissionreview]
level: practitioner
status: docs-checked
description: "Write kube-mgmt style admission policy in Rego: package kubernetes.admission, a deny set of messages, and the AdmissionReview input fields for Pods."
sources:
  - https://www.openpolicyagent.org/docs/kubernetes/primer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reject Kubernetes objects that break policy, with a clear message per violation. This page covers the kube-mgmt version of OPA admission; Gatekeeper has its own documentation.

```rego
package kubernetes.admission

deny contains msg if {
    input.request.kind.kind == "Pod"
    image := input.request.object.spec.containers[_].image
    not startswith(image, "hooli.com/")
    msg := sprintf("image '%v' comes from untrusted registry", [image])
}
```

Structure:
- `package kubernetes.admission` names the rules hierarchically; the default OPA admission-controller installation queries this package.
- `deny` is a set of error messages returned to the user. Each rule you write adds to the set, and rule order does not change the result, which is why the docs recommend starting admission policy with `deny` rules.
- `input` is the AdmissionReview object the API server sends to the webhook. This policy uses `input.request.kind` (group/version/kind) and `input.request.object`, the YAML of the object being created or modified.

For a Pod with `nginx` and `mysql` images, the iteration over `containers[_]` produces one message per untrusted image, so the user sees both violations at once.

Test locally by saving the AdmissionReview as `input.json` and evaluating `admission.deny` through a small wrapper (`result := admission.deny` in another package).

Check: evaluate with the nginx/mysql input and confirm two messages; change one image to a `hooli.com/` image and confirm one remains.

## Checked

2026-11-04. Confirmed against the OPA docs Kubernetes Primer page. Nothing removed.

Method: documentation only; no commands were run.
