---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodepool-taints-and-startup-taints
name: karpenter-nodepool-taints-and-startup-taints
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [taints, startuptaints, cilium, gpu, nodepool, tolerations]
level: practitioner
status: docs-checked
description: "NodePool taints vs startupTaints: tolerations needed for taints but not startup taints, a GPU isolation example, and the Cilium agent-not-ready pitfall."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePool taints and startupTaints

- `spec.template.spec.taints`: applied to nodes; pods must tolerate them or Karpenter will not use that NodePool for them.
- `spec.template.spec.startupTaints`: applied on launch but pods do not need to tolerate them; Karpenter assumes they are temporary and another system (for example a DaemonSet) removes them.

Isolating expensive hardware:

```yaml
spec:
  template:
    spec:
      requirements:
      - key: node.kubernetes.io/instance-type
        operator: In
        values: ["p3.8xlarge", "p3.16xlarge"]
      taints:
      - key: nvidia.com/gpu
        value: "true"
        effect: NoSchedule
```

Cilium: put `node.cilium.io/agent-not-ready=true:NoExecute` in `startupTaints` so Cilium configures networking before other pods start.

```yaml
spec:
  template:
    spec:
      startupTaints:
      - key: node.cilium.io/agent-not-ready
        value: "true"
        effect: NoExecute
```

Pitfall: if a taint is added by another system but not declared as a startup taint, Karpenter sees the pending pod as unschedulable on the new node and keeps provisioning additional nodes.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
