---
id: computing-software.devops-ci-cd.kustomize.namespace-transformer-options
name: namespace-transformer-options
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [namespacetransformer, unsetonly, setrolebindingsubjects, builtin]
level: advanced
status: docs-checked
description: "Configure NamespaceTransformer directly to only fill unset namespaces and control RoleBinding subject namespaces."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/builtins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Using the built-in through the `transformers` field exposes options the plain `namespace:` field leaves at defaults:

```yaml
apiVersion: builtin
kind: NamespaceTransformer
metadata:
  name: not-important-to-example
  namespace: test
setRoleBindingSubjects: none
unsetOnly: true
fieldSpecs:
- path: metadata/name
  kind: Namespace
  create: true
```

Arguments: `types.ObjectMeta`, `setRoleBindingSubjects`, `unsetOnly` and `fieldSpecs`.

- `unsetOnly` is false by default. When true, only namespace fields that are currently unset (empty string or missing) are set. Available in kustomize v4.5.6+.
- `setRoleBindingSubjects` controls `subjects[].namespace` in RoleBinding and ClusterRoleBinding objects (v4.5.6+). Values: `defaultOnly` (default) updates subjects named `default`; `allServiceAccounts` updates every subject with `kind: ServiceAccount`; `none` updates no subjects.

The example above updates `metadata/name` of all Namespace objects and `metadata/namespace` of all other objects, only if they have no value yet.

Use `unsetOnly: true` when some resources deliberately live in a different namespace and must not be moved. Use `allServiceAccounts` when a RoleBinding binds service accounts that move with the namespace. Check the build output for RoleBinding subjects after any namespace change.

## Checked

2026-11-08: confirmed against the Kustomize Built-Ins page, read in full (NamespaceTransformer arguments, unsetOnly, setRoleBindingSubjects values, v4.5.6+, example). The last paragraph is practical advice, not a documented claim.

Method: documentation only; no commands were run.
