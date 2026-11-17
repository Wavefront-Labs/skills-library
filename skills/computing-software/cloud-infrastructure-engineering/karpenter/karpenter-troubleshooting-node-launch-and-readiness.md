---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-troubleshooting-node-launch-and-readiness
name: karpenter-troubleshooting-node-launch-and-readiness
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [troubleshooting, node-launch, initialization, notready, kubelet, startup-taints, gpu, pod-eni]
level: practitioner
status: docs-checked
description: "Debugging nodes that fail to launch, initialize or become Ready: launch errors in controller logs, three initialization factors, unregistered resources, and kubelet logs via SSM."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/troubleshooting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting node launch and readiness

Node not created: read the controller logs, for example `kubectl logs karpenter-XXXX -c controller -n karpenter | less`. Typical error: `InvalidBlockDeviceMapping: Invalid device name /dev/xvda` from a wrong device name in block device mappings.

Nodes not initialized. Karpenter needs three things before it trusts real allocatable values and starts consolidating:
1. Node `Ready` condition is `True`.
2. Every resource expected from the instance type registers with a non-zero value in `.status.allocatable`. Common offenders: `nvidia.com/gpu` when the device plugin daemonset is missing, and `vpc.amazonaws.com/pod-eni` when `ENABLE_POD_ENI` is `false` in vpc-cni.
3. All `spec.template.spec.startupTaints` of the NodePool are removed from the node.

Node NotReady (node started but did not join). Causes: permissions, security groups, networking. Debug:

```bash
kubectl get node -l karpenter.sh/nodepool
INSTANCE_ID=$(kubectl get node <node-name> -ojson | jq -r ".spec.providerID" | cut -d \/ -f5)
aws ssm start-session --target $INSTANCE_ID
sudo journalctl -u kubelet
```

On Bottlerocket run `enter-admin-container` first and use `journalctl -D /.bottlerocket/rootfs/var/log/journal -u kubelet.service`.

`NetworkReady=false ... cni plugin not initialized` usually means the node IAM role lacks `AmazonEKS_CNI_Policy` (or the IRSA setup for vpc-cni is broken); check `kubectl logs aws-node-xxxxx -n kube-system`.

## Checked

2026-11-04. Confirmed against the Troubleshooting page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
