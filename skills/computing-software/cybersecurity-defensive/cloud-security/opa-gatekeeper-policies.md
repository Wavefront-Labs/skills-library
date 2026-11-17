---
id: computing-software.cybersecurity-defensive.cloud-security.opa-gatekeeper-policies
name: opa-gatekeeper-policies
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-workload-protection, opa-gatekeeper, rego, constraint-templates, admission-control, policy-as-code, gatekeeper-library]
level: advanced
status: gated
description: "Enforce Kubernetes admission policy with OPA Gatekeeper: Rego ConstraintTemplates, scoped Constraints, dryrun-to-deny rollout, audit, the library, and gator tests."
sources: ["https://open-policy-agent.github.io/gatekeeper/website/docs/", "https://open-policy-agent.github.io/gatekeeper-library/website/", "https://open-policy-agent.github.io/gatekeeper/website/docs/gator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPA Gatekeeper policies

Gatekeeper is a validating (and mutating) admission webhook that evaluates Rego policies against
Kubernetes objects, plus an audit loop that reports violations in existing resources.

## Install
`helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts` then
`helm install gatekeeper gatekeeper/gatekeeper -n gatekeeper-system --create-namespace`
Exempt system namespaces (`--set 'controllerManager.exemptNamespaces={kube-system}'`, which renders `--exempt-namespace=kube-system`; or Config `match` exclusions; the chart already exempts `gatekeeper-system`)
so policies cannot break kube-system.

## ConstraintTemplate (the policy logic)
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata: {name: k8sallowedrepos}
spec:
  crd:
    spec:
      names: {kind: K8sAllowedRepos}
      validation:
        openAPIV3Schema:
          type: object
          properties: {repos: {type: array, items: {type: string}}}
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sallowedrepos
        violation[{"msg": msg}] {
          c := input.review.object.spec.containers[_]
          not startswith_any(c.image, input.parameters.repos)
          msg := sprintf("image %v not from an allowed registry", [c.image])
        }
        startswith_any(s, prefixes) { startswith(s, prefixes[_]) }
```
(Also cover `initContainers` and `ephemeralContainers` in real policies.) This Rego (v0 syntax, Gatekeeper's default) was run through `gator` v3.23.1 and produced the expected message.

## Constraint (where and how strictly)
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata: {name: prod-registries}
spec:
  enforcementAction: dryrun        # dryrun -> warn -> deny
  match:
    kinds: [{apiGroups: [""], kinds: ["Pod"]}]
    namespaceSelector: {matchLabels: {env: prod}}
  parameters: {repos: ["registry.example.com/"]}
```
Check audit results: `kubectl get k8sallowedrepos prod-registries -o yaml` (`status.violations`; the audit docs say individual violations are stored there unless `--constraint-violations-limit=0`). Default `enforcementAction` is `deny`; others are `dryrun` and `warn`. (Applying to a live cluster: gated: unconfirmed, no cluster available here.)

## Use the library
gatekeeper-library (`library/general`, `library/pod-security-policy`) has vetted templates: privileged-containers, host-namespaces, host-filesystem, capabilities,
read-only-root-filesystem, requiredlabels, allowedrepos, disallowedtags, and more PSP-equivalents. Start there.

## Test
`gator verify <dir>` with a `Suite` (`apiVersion: test.gatekeeper.sh/v1alpha1`: `tests[].template`, `constraint`, `cases[].object`,
`assertions: [{violations: yes|no, message: ...}]`) in CI; `gator test --filename=pol/ --filename=pod.yaml` against manifests
before deploy, so developers see violations pre-merge (note the long flag: `-f` is not accepted and the command then waits on stdin).
Run on this skill's policy: a Pod with `docker.io/nginx` was reported, `gator test` exits 0 under `dryrun` and 1 under `deny`.
Trap: a constraint with `namespaceSelector` matches nothing unless the Namespace object (with its labels) is supplied too: pass it
in the `gator test` inputs, or as `inventory: [ns.yaml]` on a `verify` case; otherwise verify fails with
"namespace selector for namespace-scoped object but missing Namespace".

## Gotchas
- Policies on Pods also need to consider Deployments etc. (or rely on pod-level admission, which reports
  failures on ReplicaSet events rather than at `kubectl apply`). Many teams validate workload controllers too.
- Webhook failure policy: `failurePolicy: Ignore` (chart default `validatingWebhookFailurePolicy: Ignore`) fails open when Gatekeeper is down; monitor its
  availability, or choose Fail with high availability replicas.
- Kyverno is the YAML-native alternative; Pod Security Admission covers the PSS basics natively.

## Verify
Apply a non-compliant test pod in a prod-labelled namespace: denied with the message once in deny mode;
audit shows zero violations before switching from dryrun.
