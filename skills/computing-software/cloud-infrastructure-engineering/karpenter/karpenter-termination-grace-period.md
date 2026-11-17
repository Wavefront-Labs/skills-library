---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-termination-grace-period
name: karpenter-termination-grace-period
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [terminationgraceperiod, drain, do-not-disrupt, pdb, drift, node-lifetime]
level: advanced
status: docs-checked
description: "terminationGracePeriod behaviour: countdown at drain start, forced pod deletion, max node lifetime, drift past blocking PDBs, and pod terminationGracePeriodSeconds pre-deletion."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter terminationGracePeriod

Set on the NodePool at `spec.template.spec.terminationGracePeriod` and copied to NodeClaims as `spec.terminationGracePeriod`. Changing the NodePool value does not touch existing NodeClaims; it causes drift and replacements carry the new value.

The countdown starts when draining begins (after either graceful or forceful disruption). When it elapses, remaining pods are force-deleted and the instance is terminated. The node ends earlier if all disruptable pods drain first.

With `expireAfter`, maximum node lifetime is the sum of the two.

Drift eligibility changes: when configured, a node can drift even if it hosts pods with blocking PDBs or `karpenter.sh/do-not-disrupt`, so CVE-driven AMI updates cannot be blocked by badly configured apps.

Pod deletion is scheduled early so each pod still gets its own `terminationGracePeriodSeconds`. Example: a node with a 1 hour `terminationGracePeriod` draining a do-not-disrupt pod with `terminationGracePeriodSeconds: 300` deletes that pod at 55 minutes. If a pod's `terminationGracePeriodSeconds` exceeds the node's value, the node wins and the pod is deleted as soon as drain begins, without its full period.

```yaml
spec:
  template:
    spec:
      terminationGracePeriod: 1h
```

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
