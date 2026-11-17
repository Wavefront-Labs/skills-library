---
id: computing-software.cloud-infrastructure-engineering.kubernetes.karpenter-drift-and-expiry
name: karpenter-drift-and-expiry
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, karpenter, karpenter-drift, consolidation, disruption-budget, nodepool]
level: practitioner
status: docs-checked
description: "Control Karpenter node replacement from drift (AMI or NodePool changes) and expireAfter, with reason-scoped disruption budgets and maintenance windows."
sources: ["https://karpenter.sh/docs/concepts/disruption/", "https://karpenter.sh/docs/concepts/nodepools/", "https://karpenter.sh/docs/concepts/nodeclasses/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Karpenter drift and expiry

## Drift
Karpenter marks a NodeClaim `Drifted` when its node no longer matches the desired spec:
- EC2NodeClass AMI selection now resolves to a different AMI (new EKS optimised AMI release with
  an alias like `al2023@latest`), or subnet or security group selector results change.
- NodePool or EC2NodeClass template field changes (the docs hash the template spec, and list
  `requirements`, `subnetSelectorTerms`, `securityGroupSelectorTerms` and `amiSelectorTerms` as
  resolved fields that can drift without a CRD edit).
- Behavioral fields (`weight`, `limits`, `disruption.*`) do not cause drift.
Drifted nodes are replaced (new node first, then drain old), respecting PDBs and budgets.

Pin AMIs (`amiSelectorTerms: [{alias: al2023@v20261001}]`) in production so drift happens when
you bump the pin, not when AWS publishes.

## Expiry
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
spec:
  template:
    spec:
      expireAfter: 720h          # default 720h (30 days); "Never" to disable
      terminationGracePeriod: 48h  # hard cap on how long a drain may block
```
Expiration is a forceful method: it starts draining as soon as the node exceeds its lifetime and
is not rate limited by disruption budgets. Misconfigured PDBs and `karpenter.sh/do-not-disrupt` pods
can block the drain indefinitely, so the docs advise setting `terminationGracePeriod` if you use
that annotation. `expireAfter` is a maximum lifetime; drift or consolidation can replace nodes earlier.

## Budgets per reason
```yaml
spec:
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 5m
    budgets:
    - nodes: "10%"                                   # default for all reasons
    - nodes: "0"
      reasons: [Drifted, Underutilized]
      schedule: "0 8 * * mon-fri"                    # cron, always UTC (no timezone support): no drift or consolidation
      duration: 10h
    - nodes: "1"
      reasons: [Drifted]
```

## Opt-outs
- Pod annotation `karpenter.sh/do-not-disrupt: "true"` blocks voluntary disruption of its node
  (until terminationGracePeriod on expiry).

## Observe
```bash
kubectl get nodeclaims -o 'custom-columns=NAME:.metadata.name,DRIFTED:.status.conditions[?(@.type=="Drifted")].status,AGE:.metadata.creationTimestamp'
```

## Checked
2026-10-26. Checked against the Karpenter docs source for v1.15 (repository aws/karpenter-provider-aws, latest release v1.15.1, docs under website/content/en/v1.15). Confirmed: drift covers NodePool `spec.template.spec.requirements` and EC2NodeClass `subnetSelectorTerms`, `securityGroupSelectorTerms` and `amiSelectorTerms`, with other template and class fields detected by hash; `expireAfter` defaults to 720h and accepts `Never`; expiration is forceful and not rate limited by budgets, and PDBs or `karpenter.sh/do-not-disrupt` pods can block the drain, so set `terminationGracePeriod` as the upper bound; budget `reasons` are Drifted, Underutilized, Empty and Unhealthy, the default budget is `nodes: 10%`, schedules are cron in UTC with no timezone support; `alias: al2023@<version>` and `al2023@latest` in `amiSelectorTerms`. Removed as unconfirmed: the events command and the claim that userData changes are a named drift trigger.
Method: documentation only; no commands were run.
