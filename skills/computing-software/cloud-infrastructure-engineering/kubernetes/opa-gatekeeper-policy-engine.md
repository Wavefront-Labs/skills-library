---
id: computing-software.cloud-infrastructure-engineering.kubernetes.opa-gatekeeper-policy-engine
name: opa-gatekeeper-policy-engine
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, opa, gatekeeper, rego, constrainttemplate, constraint, policy-as-code, audit-mode, dryrun, sync, mutation-webhook, gator, admission-control, opa-constraint-framework, referential-constraints]
level: advanced
status: docs-checked
description: "OPA Gatekeeper's ConstraintTemplate/Constraint split, Rego authoring, audit vs enforce modes, the data sync cache, and testing policy with gator."
sources: ["https://open-policy-agent.github.io/gatekeeper/website/docs/constrainttemplates/", "https://open-policy-agent.github.io/gatekeeper/website/docs/violations/", "https://open-policy-agent.github.io/gatekeeper/website/docs/sync/", "https://open-policy-agent.github.io/gatekeeper/website/docs/exempt-namespaces/", "https://open-policy-agent.github.io/gatekeeper/website/docs/gator/", "https://open-policy-agent.github.io/gatekeeper/website/docs/audit/", "https://open-policy-agent.github.io/gatekeeper/website/docs/workload-resources/", "https://github.com/open-policy-agent/gatekeeper-library"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OPA Gatekeeper — Rego policy as an admission webhook

**Goal:** write and operate Gatekeeper constraints that enforce org policy at
admission without the two classic failure modes: policies that silently never
fire because the sync cache is empty, and policies that block the entire cluster
because they were pushed straight to `enforce`. General webhook mechanics
(failurePolicy, HA, cert rotation) are in
`computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhooks-validating-and-mutating`;
Kyverno, the YAML-native alternative, is in
`computing-software.cloud-infrastructure-engineering.kubernetes.kyverno-policy-engine`.

## 1. The two-object model
- **ConstraintTemplate** defines the Rego logic and a CRD schema for its
  parameters (reusable, like a function).
- **Constraint** is an instance of that CRD: which resources it applies to
  (`match`) and what parameters to pass.
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata: {name: k8srequiredlabels}
spec:
  crd:
    spec: {names: {kind: K8sRequiredLabels}, validation: {openAPIV3Schema: {type: object, properties: {labels: {type: array, items: {type: string}}}}}}
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8srequiredlabels
      violation[{"msg": msg}] {
        provided := {label | input.review.object.metadata.labels[label]}
        required := {label | label := input.parameters.labels[_]}
        missing := required - provided
        count(missing) > 0
        msg := sprintf("missing required labels: %v", [missing])
      }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata: {name: require-team-label}
spec:
  enforcementAction: dryrun       # start here, always
  match: {kinds: [{apiGroups: [""], kinds: [Pod]}], excludedNamespaces: [kube-system, gatekeeper-system]}
  parameters: {labels: [team]}
```

## 2. Enforcement lifecycle — never skip `dryrun`
- `enforcementAction: dryrun` logs violations to the Constraint's `status` without
  blocking anything. Run every new constraint here for at least one full
  deploy/traffic cycle (covers CronJobs, rolling restarts, batch jobs that don't
  run daily) before flipping to `deny`.
- `kubectl get k8srequiredlabels require-team-label -o jsonpath='{.status.totalViolations}'`
  / `.status.violations[]` — review the hit list, not just the count, before enforcing. Only the first
  `--constraint-violations-limit` violations (default 20) are listed in status; `totalViolations` still
  counts them all. A dryrun that only ran for an hour has not seen your weekly batch jobs yet.
- The supported `enforcementAction` values are `deny` (the default), `dryrun` and `warn`. `warn` sits
  between the other two: it returns an admission warning to `kubectl` without blocking.

## 3. The sync cache — referential policies need replicated data
Rego in the admission path only sees the object under review *unless* you
replicate other objects into Gatekeeper's data cache. `SyncSet` resources are the recommended way;
the singleton `Config` resource (it must be named `config`, in `gatekeeper-system`) works too, and the
union of both is synced:
```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata: {name: config, namespace: gatekeeper-system}
spec:
  sync:
    syncOnly:
    - {group: "", version: v1, kind: Namespace}
    - {group: "", version: v1, kind: Pod}
```
Replicated data is read from `data.inventory`: `data.inventory.cluster[<groupVersion>][<kind>][<name>]`
for cluster-scoped objects and `data.inventory.namespace[<namespace>][<groupVersion>][<kind>][<name>]` for
namespaced ones. A Kind that was never added to `syncOnly` (or a SyncSet) is simply not there to be
referenced, so test uniqueness-style policies against real data. Always
`kubectl get constrainttemplates <t> -o yaml` and grep the Rego for `data.inventory`
to know what to sync.

## 4. Mutation (separate CRDs, separate webhook)
Gatekeeper mutation uses `Assign`/`AssignMetadata`/`ModifySet`/`AssignImage` — not Rego —
applied via a **mutating** webhook that runs before the validating one, same
ordering caveat as any mutating webhook (see the webhooks skill, §5
reinvocation). See `gatekeeper-mutation-assign-assignmetadata`.

## 5. Testing before it ever reaches a cluster
- `gator test --filename=policy/` runs ConstraintTemplates + Constraints against
  example manifests locally (no cluster; `--filename` takes a file or directory, is repeatable, and
  input can also come from stdin). `gator verify` runs suite-based unit tests (it was originally named
  `gator test`) — do this in CI before merging any policy change.
- `gator expand` previews the resources an `ExpansionTemplate` generates from a workload, optionally
  applying mutators.

## Gotchas
- `excludedNamespaces` on a Constraint is separate from the `Config` resource's
  `spec.match[].excludedNamespaces`, which applies per process (`audit`, `webhook`, `sync`,
  `mutation-webhook` or `*`); excluding a namespace from enforcement does not exclude it from the `sync`
  process unless you list it there too. Check both.
- Rego's default-deny instinct does not apply here: a `violation[]` rule that
  never matches **allows** the object — Gatekeeper constraints are
  allow-unless-violation, the inverse of how Rego policies work in other OPA
  deployments.
- Syncing many objects (e.g. all Pods cluster-wide for one uniqueness check) costs memory in the
  Gatekeeper pods; sync only the Kinds your Rego reads.
- A Constraint on `Pod` is evaluated for the Pods a Deployment creates, not for the Deployment itself,
  and the denial message appears on the ReplicaSet, so test with the workload object you actually deploy.

## Verify
- [ ] Every new/changed Constraint spent at least one full deploy cycle in
      `dryrun`, and `status.violations` was reviewed, before `deny`.
- [ ] `Config.sync.syncOnly` includes every Kind any installed ConstraintTemplate's
      Rego references via `data.inventory`.
- [ ] `gator test` runs in CI against representative manifests for every policy
      change.
- [ ] The audit pod is run as a singleton (it is designed that way)
      (it writes results to Constraint status). `--audit-interval` (default 60 seconds) matches how fast
      you need to detect drift.
- [ ] A known-bad manifest is confirmed rejected in a non-prod cluster after
      flipping a constraint to `deny`.

## Checked

Documentation release: Gatekeeper website docs (open-policy-agent/gatekeeper website/docs, latest release v3.23.1, repo commit 2026-10-22).
Confirmed: ConstraintTemplate `v1` (since 3.6) and Constraint `v1beta1` examples, default `enforcementAction: deny` and the supported values `deny`/`dryrun`/`warn`, `--constraint-violations-limit` default 20, `totalViolations`, SyncSet vs Config sync (Config named `config`), `data.inventory` layout, Config `spec.match[]` with `processes`, Rego v0 default with opt-in v1, audit singleton design and `--audit-interval` default 60, `gator test`/`verify`/`expand` flags, and the workload-resource behaviour.
Removed because the docs do not state them: "fails open silently / most common bug", the Kyverno comparison, the "Rego change picks up immediately" bullet, the Envoy ext_authz example, and the audit replica count claim (the docs say the opposite).

Method: documentation only; no commands were run.
