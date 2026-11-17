---
id: computing-software.cloud-infrastructure-engineering.calico.eks-install-with-vpc-cni-or-calico-networking
name: eks-install-with-vpc-cni-or-calico-networking
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [eks, aws, aws-node, vpc-cni, installation, kubernetesprovider, eksctl, bgp-disabled]
level: practitioner
status: docs-checked
description: "Install Calico on EKS for policy over the AWS VPC CNI, or as the full CNI after deleting aws-node, with the control-plane limit."
sources:
  - https://docs.tigera.io/calico/latest/getting-started/kubernetes/managed-public-cloud/eks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two modes. In both, `kubernetesProvider: EKS` and `bgp: Disabled` are set, and the CRDs (the v3 manifest; a `v1beta1` variant for Kubernetes 1.34 or 1.35) and `tigera-operator.yaml` are created first.

**1. Amazon VPC networking, Calico policy** (IPAM and CNI from AWS).
- `eksctl create cluster --name <my-calico-cluster>`. Do **not** enable network policy for the AWS VPC CNI; it conflicts with Calico.
- Make AWS VPC CNI annotate pods with their IPs so they propagate quickly to Calico. Grant `aws-node` the `patch` permission on pods (append a rule to the `aws-node` ClusterRole), then `kubectl set env -n kube-system daemonset/aws-node ANNOTATE_POD_IP=true`.
- Installation:

```yaml
spec:
  kubernetesProvider: EKS
  cni:
    type: AmazonVPC
  calicoNetwork:
    bgp: Disabled
```

Limitation: policy on IPv6 pods is not enforced when `ENABLE_V4_EGRESS` is `true`.

**2. Calico networking** (Calico CNI and IPAM).
- `eksctl create cluster --name my-calico-cluster --without-nodegroup`, then `kubectl delete daemonset -n kube-system aws-node`. Add nodes afterwards.
- Installation as above but `cni.type: Calico`.

Limitation: Calico networking cannot run on the EKS control plane nodes, so they cannot initiate connections to Calico pods. Webhook pods that the control plane must reach can set `hostNetwork: true`.

The page's Installation block also creates `APIServer`, `Goldmane` and `Whisker` resources.

## Checked

Read in full on 2026-11-08: the Amazon Elastic Kubernetes Service (EKS) page. Both procedures, the Installation fields and both limitations match it. Remarks on overlay type that the page text does not state were removed.

Method: documentation only; no commands were run.
