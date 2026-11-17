---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodepool-limits
name: karpenter-nodepool-limits
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [limits, cpu, memory, gpu, nodepool, resource-quota, status-resources]
level: practitioner
status: docs-checked
description: "NodePool spec.limits: cpu, memory, GPU and nodes limits, unspecified means cloud quotas, eventual consistency overrun, DecimalSI string advice and checking consumption."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePool limits

`spec.limits` caps the total resources a NodePool may provision. When exceeded, new provisioning stops until nodes are terminated. If unspecified, only the cloud provider quotas limit you.

```yaml
spec:
  limits:
    cpu: "1000"
    memory: 1000Gi
    nvidia.com/gpu: 2
    nodes: 20
```

Notes:
- CPU uses a `DecimalSI` value. The Kubernetes API coerces it to a string, so quote it rather than using an integer to avoid GitOps drift.
- Memory uses `BinarySI`, such as `1000Gi`.
- `limits.nodes` caps node count during scaling or drift replacement (the only limit allowed on static NodePools).
- Provisioning is highly parallel, so limit checking is eventually consistent and can overrun during rapid scale-outs.
- Limits are behavioural: changing them does not cause drift.

Check current consumption from the status:

```bash
kubectl get nodepool -o=jsonpath='{.items[0].status}'
```

`status.nodes` shows the managed node count and `status.resources` shows cpu, memory and ephemeral-storage totals.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Added the Disruption page as a source for the claim that limits are behavioural fields that do not cause drift; other claims matched.
