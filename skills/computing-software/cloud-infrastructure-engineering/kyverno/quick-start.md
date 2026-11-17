---
id: computing-software.cloud-infrastructure-engineering.kyverno.quick-start
name: quick-start
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [quick-start, helm-install, require-labels, sync-secrets, generator-apply, rbac-aggregation]
level: intro
status: docs-checked
description: "Run the Kyverno quick start: Helm install, a require-labels ValidatingPolicy, a MutatingPolicy label and a GeneratingPolicy that syncs a secret."
sources:
  - https://kyverno.io/docs/introduction/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The guides are for labs and proof of concept, not production.

Install: `helm repo add kyverno https://kyverno.github.io/kyverno/`, `helm repo update`, `helm install kyverno kyverno/kyverno -n kyverno --create-namespace`.

Validate: a `policies.kyverno.io/v1` `ValidatingPolicy` named `require-labels` with `validationActions: [Deny]`, `matchConstraints.resourceRules` (apiGroups `['']`, apiVersions `['v1']`, operations CREATE and UPDATE, resources `pods`) and a `validations[]` entry whose `expression` checks `has(object.metadata.labels.team)` is non-empty. `kubectl create deployment nginx --image=nginx` is denied by webhook `validate.kyverno.svc-fail` (auto-generated rule `autogen-check-team`); `kubectl run nginx --image nginx --labels team=backend` passes. Check results with `kubectl get policyreport -o wide`.

Mutate: a `MutatingPolicy` with `matchConditions` (`!has(object.metadata.labels) || !has(object.metadata.labels.team)`) and `mutations[]` using `patchType: ApplyConfiguration` and an `applyConfiguration.expression` building `Object{metadata: Object.metadata{labels: Object.metadata.labels{team: "bravo"}}}`. A pod labelled `team=alpha` is left alone.

Generate: a `GeneratingPolicy` `sync-secrets` with `evaluation.synchronize.enabled: true`, matching namespace CREATE, variables `targetNs` (`object.metadata.name`) and `sourceSecret` (`resource.Get("v1", "secrets", "default", "regcred")`), and `generate[].expression` `generator.Apply(variables.targetNs, [variables.sourceSecret])`. Default RBAC has no Secret access. Add ClusterRoles `kyverno:secrets:view` (get, list, watch) and `kyverno:secrets:manage` (create, update, delete) carrying the label `rbac.kyverno.io/aggregate-to-background-controller: "true"` (view also gets the admission and reports aggregation labels).

Test in a user namespace: system namespaces such as `kube-system` and `kyverno` may be excluded by config.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/introduction/quick-start/.

Method: documentation only; no commands were run.
