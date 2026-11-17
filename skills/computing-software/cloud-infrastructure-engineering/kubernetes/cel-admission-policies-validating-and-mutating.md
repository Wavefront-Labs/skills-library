---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cel-admission-policies-validating-and-mutating
name: cel-admission-policies-validating-and-mutating
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, admission-control, validatingadmissionpolicy, validatingadmissionpolicybinding, paramkind, cel-expressions, mutatingadmissionpolicy, cel-mutation]
level: advanced
status: docs-checked
description: "Write in-process CEL admission policies: ValidatingAdmissionPolicy with bindings, params and audit actions, and MutatingAdmissionPolicy with ApplyConfiguration and JSONPatch."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/", "https://kubernetes.io/docs/reference/access-authn-authz/mutating-admission-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CEL admission policies: validating and mutating

No webhook server, no TLS, no availability risk: policies run inside kube-apiserver.

## ValidatingAdmissionPolicy (GA 1.30)
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata: {name: replica-limit}
spec:
  failurePolicy: Fail
  paramKind: {apiVersion: v1, kind: ConfigMap}
  matchConstraints:
    resourceRules:
    - {apiGroups: [apps], apiVersions: [v1], operations: [CREATE, UPDATE], resources: [deployments]}
  variables:
  - {name: maxReplicas, expression: "int(params.data.maxReplicas)"}
  validations:
  - expression: "object.spec.replicas <= variables.maxReplicas"
    messageExpression: "'replicas must be <= ' + string(variables.maxReplicas)"
    reason: Invalid
  - expression: "object.spec.template.spec.containers.all(c, !c.image.endsWith(':latest'))"
    message: "no :latest images"
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata: {name: replica-limit-prod}
spec:
  policyName: replica-limit
  validationActions: [Deny]            # Deny | Warn | Audit (combine Warn+Audit for dry runs)
  paramRef: {name: replica-limits, namespace: policy-params, parameterNotFoundAction: Deny}
  matchResources:
    namespaceSelector: {matchLabels: {env: prod}}
```
A policy does nothing without a binding. Roll out with `[Warn, Audit]`, watch audit annotations
`validation.policy.admission.k8s.io/validation_failure`, then switch to `Deny`.
Useful CEL bits: `has(object.spec.foo)`, `object.?metadata.labels['team'].orValue('')`,
`oldObject` on UPDATE (null on CREATE), `request` (the AdmissionRequest, so
`request.userInfo.username`), `params`, `namespaceObject`, `authorizer` checks,
`matchConditions` to pre-filter cheaply. `object` is null on DELETE.

## MutatingAdmissionPolicy (beta 1.34, stable 1.36)
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingAdmissionPolicy
metadata: {name: default-pull-policy}
spec:
  matchConstraints:
    resourceRules: [{apiGroups: [""], apiVersions: [v1], operations: [CREATE], resources: [pods]}]
  failurePolicy: Fail
  reinvocationPolicy: IfNeeded
  mutations:
  - patchType: ApplyConfiguration
    applyConfiguration:
      expression: >
        Object{ spec: Object.spec{ containers: object.spec.containers.map(c,
          Object.spec.containers{ name: c.name, imagePullPolicy: "IfNotPresent" }) } }
  # - patchType: JSONPatch  (expression returns a list of JSONPatch{op, path, value})
---
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingAdmissionPolicyBinding
metadata: {name: default-pull-policy}
spec: {policyName: default-pull-policy}
```
The `MutatingAdmissionPolicy` feature gate is on by default from 1.36 (stable); during beta
(1.34 and 1.35) it defaults to off. Mutating admission runs before validating admission; keep
mutations idempotent. Policies mutate with `ApplyConfiguration` (server-side-apply merge) or `JSONPatch`.

## Verify
```bash
kubectl create deploy t --image=nginx:latest --replicas=50 -n prod --dry-run=server   # expect denial messages
kubectl get validatingadmissionpolicy replica-limit -o jsonpath='{.status.typeChecking}'   # type-check warnings
```
- [ ] Policies have bindings; type checking shows no warnings; Deny only after an Audit period.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes API types.
Confirmed: ValidatingAdmissionPolicy stable v1.30; `validationActions` values, `reason` values (Invalid is valid),
`parameterNotFoundAction` field, `status.typeChecking`; MutatingAdmissionPolicy feature gate stages (beta 1.34-1.35 default off,
stable 1.36 default on), `admissionregistration.k8s.io/v1` in the docs example and API types, `reinvocationPolicy`,
`ApplyConfiguration` and `JSONPatch` patch types. Wrong in the original: MutatingAdmissionPolicy shown as v1beta1 when it is stable
in 1.36. Removed the unconfirmed "cost limits at creation" claim and the alpha dates.
Method: documentation only; no commands were run.
