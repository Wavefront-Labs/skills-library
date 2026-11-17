---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-troubleshooting-nodes-not-deprovisioned
name: karpenter-troubleshooting-nodes-not-deprovisioned
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [troubleshooting, deprovisioning, initialized, pdb, do-not-disrupt, consolidation]
level: practitioner
status: docs-checked
description: "Why Karpenter will not disrupt a node: missing karpenter.sh/initialized label, blocking PDBs, active do-not-disrupt annotation, and consolidation scheduling constraints."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/troubleshooting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting nodes that are not deprovisioned

Four causes to check, in order:

1. Initialization. Only nodes carrying the `karpenter.sh/initialized` label are considered for automatic disruption. Fix the init problem first (see the nodes-not-initialized skill).
2. PDBs. Karpenter evicts with backoff retry and never force-deletes pods, so a PDB such as `minAvailable: 4` on `app: myapp` blocks drain when eviction would drop below it. `minAvailable` and `maxUnavailable` accept integers or percentages.
3. `karpenter.sh/do-not-disrupt` pod annotation. Active when set to `"true"` (permanent) or to a duration such as `"30m"` while the pod has run for less than that. Karpenter will not drain or delete such a node, and will not consolidate it, though its spare capacity can host pods from other consolidating nodes. Remove the annotation or wait for the duration to elapse.
4. Scheduling constraints, consolidation only. If the scheduling simulation shows the node's pods cannot fit elsewhere because of inter-pod affinity or anti-affinity, topology spread constraints or other restrictions, consolidation skips it.

## Checked

2026-11-08. Confirmed against the Troubleshooting page (v1.13), section "Nodes not deprovisioned". Removed the unsupported claim that `karpenter_nodepools_allowed_disruptions` of 0 means NodePool budgets are blocking; the page does not say this. The section also gives the PDB example with `minAvailable: 4` for label `myapp`.

Method: documentation only; no commands were run.

