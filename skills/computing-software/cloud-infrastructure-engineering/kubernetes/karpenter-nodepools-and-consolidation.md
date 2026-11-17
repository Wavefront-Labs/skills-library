---
id: computing-software.cloud-infrastructure-engineering.kubernetes.karpenter-nodepools-and-consolidation
name: karpenter-nodepools-and-consolidation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, karpenter, nodepool, ec2nodeclass, consolidation, drift, disruption-budget, bin-packing, spot, provisioning, aws, just-in-time-nodes]
level: advanced
status: docs-checked
description: "Karpenter's NodePool/NodeClass model, the three disruption reasons (consolidation, drift, expiration), and consolidation policies that actually bin-pack."
sources: ["https://karpenter.sh/docs/concepts/nodepools/", "https://karpenter.sh/docs/concepts/disruption/", "https://karpenter.sh/docs/concepts/nodeclasses/", "https://karpenter.sh/docs/reference/settings/", "https://karpenter.sh/docs/getting-started/migrating-from-cas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Karpenter NodePools and consolidation

**Goal:** get Karpenter's just-in-time node provisioning and consolidation working the way it's
designed — per-pod simulation, not per-node-group — and know which disruption mechanism is firing
when nodes churn.

## 1. The object model
- **NodePool** — replaces Cluster Autoscaler's node groups. Defines `requirements` (instance
  family, capacity type, zone — as Kubernetes-style label selectors, not a fixed list), `limits`
  (total CPU/memory across all nodes it can create), `disruption` policy, and a `weight`: when
  several NodePools match, Karpenter prefers the highest weight and falls back to lower ones if
  it cannot use it (for example its limits are reached).
- **NodeClass** (`EC2NodeClass` on AWS, etc.) — the cloud-specific launch template: AMI, subnet
  selector, security groups, block device mappings, instance profile. A NodePool references one
  NodeClass by name.
- Karpenter provisions **one node per pod-group-that-doesn't-fit**, computed directly from pending
  pods' requests/tolerations/affinity — no pre-defined "shapes" like CA's node groups. It picks
  the cheapest instance type satisfying the NodePool's requirements that fits the batch of pending
  pods it's bin-packing together in that provisioning loop.

## 2. Disruption: three distinct reasons, one mechanism
`spec.disruption` on the NodePool controls when Karpenter voluntarily replaces or removes nodes:
- **Consolidation** (`consolidationPolicy`: `WhenEmptyOrUnderutilized` (default), `Balanced` or
  `WhenEmpty`) — Karpenter simulates whether the pods on a node (or several nodes) could be
  repacked onto fewer or cheaper nodes. `consolidateAfter` is how long to wait after a pod was
  last added to or removed from the node (default `0s`; `Never` disables consolidation). 
  `WhenEmptyOrUnderutilized` is the most aggressive — it will replace a half-used large node with a
  cheaper one; `Balanced` skips marginal consolidations whose savings do not justify the pod
  disruption; `WhenEmpty` only touches nodes with no workload pods.
- **Drift** — the NodeClass or NodePool spec changed (new AMI, new subnet, requirement edit) and
  Karpenter detects the live node no longer matches. It marks the node `Drifted` and replaces it
  on the next disruption cycle — this is how you roll out AMI upgrades: edit the NodeClass, let
  drift do the replacement instead of manually cordoning.
- **Expiration** (`spec.template.spec.expireAfter`, default `720h`, `Never` disables) — a forceful
  method that starts draining once the node exceeds its lifetime, regardless of utilisation. It
  is not rate limited by budgets; PDBs and do-not-disrupt pods can block the drain, so pair it
  with `terminationGracePeriod`.
A pod annotated `karpenter.sh/do-not-disrupt: "true"` blocks voluntary (graceful) disruption of
its node — use for singleton jobs that cannot be interrupted.

## 3. Disruption budgets
`spec.disruption.budgets` caps how many nodes in a NodePool can be disrupted at once (`nodes: "10%"`
or an absolute count; the default is one budget of `10%`), optionally scoped to `reasons` (`Drifted`,
`Underutilized`, `Empty`, `Unhealthy`) and a `schedule` (cron, always UTC) with a `duration` — e.g. 0
nodes during a release window. This is the main lever for "don't let consolidation thrash my
cluster during peak traffic."

## 4. Spot and interruption handling
NodePool `requirements` can allow both `spot` and `on-demand` capacity types; Karpenter's scheduling
simulation treats spot as just another selectable dimension, so a single NodePool can serve both.
Pair with the Karpenter **interruption handling** feature: it is disabled unless you set the SQS
queue name (`INTERRUPTION_QUEUE` / `--interruption-queue`) and wire the queue to the EC2 events.
Karpenter then watches for Spot interruption warnings (a 2 minute notice before EC2 reclaims the
instance), scheduled maintenance, and instance terminating, stopping and status-check-failure
events, and taints, drains and replaces the node ahead of them.

## Gotchas
- Consolidation is evaluated continuously, so a long-running job that cannot be interrupted needs
  `karpenter.sh/do-not-disrupt: "true"`.
- `WhenEmptyOrUnderutilized` consolidation plus a workload with bursty idle periods (e.g. CI
  runners) causes visible node churn in `kubectl get nodes -w`; if that's undesirable, use
  `WhenEmpty` and accept lower bin-packing efficiency.
- NodePool `limits` are a hard ceiling — once exceeded, Karpenter stops creating instances for
  that NodePool, so pods that only fit it stay pending.
- Unlike CA, there is no node group abstraction; ordering between NodePools is via `weight`
  (highest first, falling back when limits are reached).
- Migrating from Cluster Autoscaler: follow the Karpenter migration guide, which runs Karpenter
  first and then disables the cluster autoscaler. See the companion skill on choosing/migrating
  between them for the sequencing.

## Verify
- [ ] `kubectl get nodeclaims` shows nodes tied to the expected NodePool, with the `Drifted`
      condition appearing only when intended.
- [ ] A test AMI bump on the NodeClass produces `Drifted=True` nodes that get replaced within one
      disruption budget window, with pods rescheduled cleanly.
- [ ] A pod with `karpenter.sh/do-not-disrupt: "true"` survives a forced consolidation event that
      would otherwise have replaced its node.
- [ ] Spot interruption test (or AWS Fault Injection Simulator) shows the node draining before
      termination, not pods hard-killed.

## Checked
2026-10-26. Checked against the Karpenter docs source for v1.15 (repository aws/karpenter-provider-aws, latest release v1.15.1). Confirmed: `consolidationPolicy` values WhenEmptyOrUnderutilized (default), Balanced and WhenEmpty; `consolidateAfter` is one duration that restarts when pods are added or removed (default 0s, `Never` disables); drift, expiration (`expireAfter`, default 720h, forceful) and Node Auto Repair; budget reasons Drifted, Underutilized, Empty, Unhealthy, default budget `nodes: 10%`, UTC cron schedules; `weight` prefers the highest-weight NodePool with fallback when limits are reached; NodePool `limits` stop new instances; `karpenter.sh/do-not-disrupt`; interruption handling is disabled unless an SQS queue is configured (setting INTERRUPTION_QUEUE or `--interruption-queue`) and Spot gives a 2 minute notice. Corrected: consolidateAfter is not split by empty versus underutilized, expiration does not simply respect do-not-disrupt, and a newer `Balanced` policy exists. Removed as unconfirmed: the weight tie-break rule, the limits event name, the priority-class expander remark and the memory-growth example.
Method: documentation only; no commands were run.
