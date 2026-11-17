---
id: computing-software.cloud-infrastructure-engineering.kubernetes.operator-framework-selection
name: operator-framework-selection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, build-vs-buy, kubebuilder, operator-sdk, helm-operator, metacontroller, kudo, kopf, kubebuilder-vs-operator-sdk, vendor-operator, operatorhub, crossplane, total-cost-of-ownership]
level: sme
status: docs-checked
description: "Decide whether an operator is the right tool at all, and which toolchain to build it with — kubebuilder vs operator-sdk vs Helm/metacontroller vs a vendor operator off the shelf."
sources: ["https://sdk.operatorframework.io/docs/overview/", "https://book.kubebuilder.io/", "https://github.com/metacontroller/metacontroller", "https://github.com/nolar/kopf", "https://github.com/kudobuilder/kudo"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator framework selection — don't build one before checking if you should, or with what

**Goal:** answer "do we need a custom operator" honestly before answering "which
framework," and pick the lightest tool that actually fits — writing a Go
controller is the most expensive point on this spectrum, not the default.

## 1. Do you need an operator at all?
An operator earns its cost when the thing you're automating needs **ongoing,
continuous reconciliation against live cluster/external state** — not just
templated install. Signals you don't need one:
- The workflow is "render YAML from parameters, apply once, maybe `helm upgrade`
  later" — that's a Helm chart or Kustomize overlay, full stop. See
  `computing-software.cloud-infrastructure-engineering.kubernetes.helm-chart-authoring`.
- There's no meaningful "day 2" logic (backup orchestration, failover detection,
  schema migration on upgrade, scaling decisions based on custom metrics) — if
  the object, once created, never needs anything watched or reacted to, a
  one-shot Job or a chart is cheaper to build and operate than a long-running
  controller process you now own forever.
- A vendor already publishes an operator for the exact thing (a database, a
  message queue, a cert authority) — install theirs from OperatorHub or their
  repo and contribute fixes upstream rather than re-deriving years of edge-case
  handling (failover timing, backup consistency) they've already paid for.
Signals you probably do need one: the thing has its own lifecycle events
(primary/replica failover, rolling schema migration, cert rotation) that must
react to cluster or external state continuously, and no existing operator fits
your constraints (licensing, support model, feature gaps) after a real evaluation.

## 2. If building: kubebuilder vs operator-sdk
Both use `controller-runtime` for Go operators —
this is not a "different engines" choice, it's "different scaffolding and
packaging conveniences" on top of the same engine.
- **kubebuilder**: hosted under kubernetes-sigs and scaffolds Go projects. Best default when
  you're writing Go and don't need OLM bundle generation built into the CLI.
- **operator-sdk**: provides workflows for Go, Ansible and Helm operators and adds `operator-sdk generate bundle`/`bundle
  validate` for OLM packaging (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.operator-lifecycle-manager-packaging`),
  plus **Helm-based** and **Ansible-based** operator types for teams that want
  reconciliation driven by an existing Helm chart or Ansible playbook instead of
  Go — genuinely useful if your team's deepest expertise is Helm/Ansible, not Go,
  and the reconciliation logic is mostly "apply this chart with these values,"
  not bespoke state machines. The Operator SDK docs note that each operator type has a different set of
  capabilities (its capability-level documentation lists the limits per type), so check them before choosing.
- Practical default: start with kubebuilder for a Go operator; reach for
  operator-sdk specifically when OLM distribution is a known requirement, or for
  the Helm/Ansible operator types when that fits the team better than Go.

## 3. Lighter-weight alternatives worth knowing exist
- **Metacontroller**: write reconciliation logic as a webhook that returns desired
  child object state as JSON/YAML — your controller can be a small Python/any-language
  HTTP service, not a compiled Go binary with its own CRD scaffolding. Good fit
  for simple "compose these children from this spec" patterns; weaker for complex
  finalizer/status/leader-election needs you'd get for free from controller-runtime.
- **kopf** (the Kubernetes Operator Pythonic Framework) / similar language-specific frameworks: lower
  barrier if the team is Python-first and the operator's complexity is modest. envtest and the OLM
  bundle commands belong to the Go and operator-sdk toolchains, so budget for your own testing and
  packaging tooling.
- **KUDO**: declarative, YAML-driven operator toolkit (plans/phases/steps instead
  of Go code). The `kudobuilder/kudo` repository's last push was on 2023-08-22 (as seen on 2026-10-26), so
  treat it as inactive and check the project's current status before adopting it.
- **Crossplane**: not a generic operator framework but a specific pattern
  (composite resources + providers) purpose-built for provisioning external
  cloud infrastructure through Kubernetes APIs — the right tool if "the operator"
  is really "manage cloud resources declaratively," not a bespoke app lifecycle.

## 4. The cost side of the ledger, stated plainly
A custom Go operator is a long-lived service you now run in every environment
that installs the CRD: it needs HA (leader election), RBAC maintenance, a release
process, monitoring, on-call ownership, and a testing tier (envtest/e2e) — not a
one-time build cost. Before committing, estimate: who owns this in a year, what
happens if the maintainer leaves, and whether the "day 2" logic it automates is
actually exercised often enough to justify a standing service versus a documented
manual runbook or a scheduled Job.

## Gotchas
- Choosing operator-sdk purely for OLM and then never actually publishing through
  OLM carries its extra surface area (bundle generation code, CSV templates) for
  no benefit — drop to kubebuilder-equivalent scaffolding if OLM distribution
  gets deprioritized.
- Metacontroller/webhook-based approaches re-fetch and re-render on every
  relevant event just like a Go controller — "lighter weight to write" does not
  mean "no reconciliation-loop discipline needed"; idempotency rules still apply.
- A vendor operator's upgrade cadence and CRD versioning discipline become your
  risk the moment you depend on it in production — vet its release notes and CRD
  version history before adopting, same scrutiny you'd apply to any dependency.

## Verify
- [ ] A one-paragraph answer exists for "what day-2 behavior does this operator
      provide that a chart + runbook couldn't" before any code is written.
- [ ] The chosen framework's testing story (envtest availability, community
      examples) was checked against the team's actual language/tooling comfort,
      not assumed.
- [ ] If adopting a vendor/OSS operator instead of building: its CRD versioning
      history and maintenance cadence were reviewed, not just its feature list.
- [ ] A named owner and on-call path exists for the operator before it reaches
      production, regardless of which framework was chosen.

## Checked

Checked on 2026-10-26 against `operator-framework/operator-sdk` (website docs: overview, CLI reference), `kubernetes-sigs/kubebuilder` README and book, `metacontroller/metacontroller` README, `nolar/kopf` README, and GitHub repository metadata for `kudobuilder/kudo`.
Confirmed: operator-sdk uses controller-runtime and offers Go, Ansible and Helm workflows; `generate bundle` and `bundle validate` exist; capability level differs per operator type; Metacontroller controllers are webhooks in any language; kopf is a Python framework; KUDO's last push was 2023-08-22.
Removed as unconfirmed: "Go-only", "SIG-maintained leaner" wording, `controller-gen` as a shared foundation, and the claim that Helm and Ansible operators have a lower ceiling in specific ways.

Method: documentation only; no commands were run.
