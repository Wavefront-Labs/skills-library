---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gatekeeper-mutation-assign-assignmetadata
name: gatekeeper-mutation-assign-assignmetadata
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, policy-engines, assignmetadata, gatekeeper, mutation, opa]
level: practitioner
status: docs-checked
description: "Mutate resources with Gatekeeper Assign, AssignMetadata, ModifySet and AssignImage, including location paths, pathTests and ordering."
sources: ["https://open-policy-agent.github.io/gatekeeper/website/docs/mutation/", "https://open-policy-agent.github.io/gatekeeper/website/docs/mutation-background/", "https://open-policy-agent.github.io/gatekeeper/website/docs/gator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gatekeeper mutation

Mutators are CRDs in `mutations.gatekeeper.sh/v1` (`AssignImage` is documented as `v1alpha1`); the
mutating webhook applies them before validation.

## AssignMetadata: labels and annotations only
```yaml
apiVersion: mutations.gatekeeper.sh/v1
kind: AssignMetadata
metadata: {name: owner-label}
spec:
  match:
    scope: Namespaced
    namespaces: ["team-*"]
  location: "metadata.labels.owner"
  parameters:
    assign: {value: "unknown"}
```
AssignMetadata is limited to labels and annotations, and may only add them: pre-existing labels and
annotations cannot be modified. It has no `applyTo` field. To copy the object's own name or namespace use
`parameters.assign.fromMetadata.field` (`name` or `namespace`) instead of `value`.

## Assign: any field outside metadata
```yaml
apiVersion: mutations.gatekeeper.sh/v1
kind: Assign
metadata: {name: default-pull-policy}
spec:
  applyTo: [{groups: [""], kinds: [Pod], versions: [v1]}]
  match: {scope: Namespaced, kinds: [{apiGroups: ["*"], kinds: [Pod]}]}
  location: "spec.containers[name:*].imagePullPolicy"
  parameters:
    pathTests:
    - {subPath: "spec.containers[name:*].imagePullPolicy", condition: MustNotExist}
    assign: {value: IfNotPresent}
```
`[name:*]` iterates list entries keyed by `name` (wildcards are allowed for list element values); `pathTests`
with `MustNotExist` avoids overwriting user values. `applyTo` is required for every mutator except
AssignMetadata and does not accept globs; its optional `operations` field takes `CREATE`, `UPDATE` or `*`
(the webhook only handles those two, and `DELETE` or `CONNECT` are rejected).

## Others
- `ModifySet`: add or remove items in a list treated as a set (for example `args`).
- `AssignImage`: change the domain, path or tag of an image string (`assignDomain`, `assignPath`,
  `assignTag`; at least one is required, for example `assignDomain: "my.registry.io"`).

## Behaviour
- Mutators can run more than once (for example because of the webhook reinvocation policy), so they must
  converge on a stable result; `applyTo` lets Gatekeeper detect mutators that disagree about a kind's schema.
- Pods created by a controller pass through the webhook individually, so match `Pod` to mutate what a
  Deployment creates.
- `gator expand` takes a resource, its `ExpansionTemplate`s and optional mutators and prints the expanded
  resources, so you can preview them offline; `gator test` checks objects against templates and constraints.

## Verify
```bash
kubectl run t --image=nginx -n team-a --dry-run=server -o yaml | grep -E 'owner|imagePullPolicy'
```

## Checked

Documentation release: Gatekeeper website docs (open-policy-agent/gatekeeper website/docs, latest release v3.23.1, repo commit 2026-10-22).
Confirmed in mutation.md, mutation-background.md and gator.md: the four mutator kinds and their apiVersions (AssignImage is `v1alpha1` in the docs), AssignMetadata restrictions (labels and annotations only, add only, no `applyTo`), `fromMetadata`, `applyTo` rules and `operations`, `pathTests` with `MustExist`/`MustNotExist`, list wildcard syntax, `assignDomain`/`assignPath`/`assignTag`, the convergence requirement, and the `gator expand` inputs.
Removed: the alphabetical-order claim (not in the docs), the `registry.internal` example value, and the claim that `gator test` exercises mutators.

Method: documentation only; no commands were run.
