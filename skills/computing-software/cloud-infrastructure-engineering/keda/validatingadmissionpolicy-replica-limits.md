---
id: computing-software.cloud-infrastructure-engineering.keda.validatingadmissionpolicy-replica-limits
name: validatingadmissionpolicy-replica-limits
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [validatingadmissionpolicy, cel, replica-limit, validatingadmissionpolicybinding, maxreplicacount, guardrails]
level: advanced
status: docs-checked
description: "Cap KEDA scaling cluster-side with Kubernetes ValidatingAdmissionPolicy CEL rules for ScaledObjects, Deployments, ReplicaSets and HPAs."
sources:
  - https://keda.sh/docs/2.17/operate/admission-webhooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The examples match the `keda.sh` group at `v1alpha1` with the operations CREATE and UPDATE, so both new objects and edits are checked.
Beyond KEDA's built-in webhooks, Kubernetes `ValidatingAdmissionPolicy` (stable in v1.30) lets you add declarative rules in the Common Expression Language. The KEDA page shows a policy plus a binding that denies ScaledObjects with more than 10 replicas in the `default` namespace:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: "limit-keda-replicas.example.com"
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
    - apiGroups:   ["keda.sh"]
      apiVersions: ["v1alpha1"]
      operations:  ["CREATE", "UPDATE"]
      resources:   ["scaledobjects"]
  validations:
    - expression: "object.spec.maxReplicaCount <= 10"
      message: "The maximum allowed number of pod replicas is 10."
```

The binding sets `policyName` and `validationActions: [Deny]`, with a `namespaceSelector` matching label `kubernetes.io/metadata.name: default`.

Because KEDA manages an HPA behind the scenes, the page adds a complementary set of policies that deny more than 10 replicas on `deployments` and `replicasets` (apiGroup `apps`, `object.spec.replicas <= 10`) and on `horizontalpodautoscalers` (apiGroup `autoscaling`, version `v2`), each with its own binding.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Admission Webhooks page: the ValidatingAdmissionPolicy and binding examples for ScaledObjects, Deployments, ReplicaSets and HPAs.

Method: documentation only; no commands were run.
