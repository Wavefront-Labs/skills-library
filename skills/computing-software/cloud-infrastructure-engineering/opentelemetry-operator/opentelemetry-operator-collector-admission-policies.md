---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-admission-policies
name: opentelemetry-operator-collector-admission-policies
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, validatingadmissionpolicy, kyverno, pod-security-admission, cel-expression, admission-control]
level: advanced
status: docs-checked
description: "Block privileged fields in OpenTelemetryCollector resources with Pod Security Admission, a ValidatingAdmissionPolicy, or Kyverno for untrusted tenants."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/security.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restrict Collector privileges with admission policies

When unprivileged users may create `OpenTelemetryCollector` resources, block the dangerous fields at admission. Three options are documented.

Pod Security Admission. Label the namespace `pod-security.kubernetes.io/enforce: baseline` (or `restricted`) to block hostPath, hostNetwork, hostPID and privileged containers on the resulting pods. Limitation: the CR is still admitted and only the pods are rejected, so the user sees a healthy-looking resource whose DaemonSet produces no pods, with the reason in the DaemonSet events. PSA also does not constrain `spec.serviceAccount`, `tolerations` or `nodeSelector`.

ValidatingAdmissionPolicy (GA since Kubernetes 1.30). Reject the CR at apply time. Match `opentelemetry.io` resources `opentelemetrycollectors` in both `v1alpha1` and `v1beta1` on CREATE and UPDATE, then use CEL validations such as:

```
!has(object.spec.hostNetwork) || !object.spec.hostNetwork
object.spec.volumes.all(v, !has(v.hostPath))
```

Add similar expressions for `hostPID`, `securityContext.privileged`, privileged `additionalContainers` and `initContainers`, and the embedded `targetAllocator.securityContext`. Bind the policy with a `ValidatingAdmissionPolicyBinding` (`validationActions: ["Deny"]`) and a `namespaceSelector` on a label such as `otel-collector-privileged: "false"`, leaving platform namespaces free to run privileged node collectors.

Kyverno. A `ClusterPolicy` can reuse the same CEL expressions and adds an `Audit` mode to discover what a policy would break before enforcing.

## Checked

2026-11-04. Confirmed against docs/collector/security.md: the three options (Pod Security Admission baseline or restricted, ValidatingAdmissionPolicy GA since 1.30 with `v1alpha1` and `v1beta1` match rules and CREATE and UPDATE, Kyverno ClusterPolicy with Audit mode), the PSA limitation for `serviceAccount`, `tolerations` and `nodeSelector`, the example CEL expressions, the `validationActions: ["Deny"]` binding and the `otel-collector-privileged: "false"` namespace label. Nothing removed.

Method: documentation only; no commands were run.
