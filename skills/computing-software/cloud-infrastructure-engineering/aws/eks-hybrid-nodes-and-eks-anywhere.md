---
id: computing-software.cloud-infrastructure-engineering.aws.eks-hybrid-nodes-and-eks-anywhere
name: eks-hybrid-nodes-and-eks-anywhere
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eks, hybrid-nodes, eks-anywhere, on-premises-kubernetes]
level: advanced
status: docs-checked
description: "Join on-premises servers to an EKS cluster with EKS Hybrid Nodes (remote networks, CNI, credentials) and know when EKS Anywhere fits instead."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-overview.html", "https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-networking.html", "https://anywhere.eks.amazonaws.com/docs/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EKS Hybrid Nodes and EKS Anywhere

## 1. Hybrid Nodes: AWS control plane, your servers
Prerequisites:
- Private connectivity (Site-to-Site VPN or Direct Connect) between on-prem and the cluster VPC.
- Non-overlapping **remote node** and **remote pod** CIDRs, declared on the cluster:
```bash
aws eks create-cluster --name hybrid --role-arn <ROLE> --resources-vpc-config subnetIds=subnet-a,subnet-b \
  --remote-network-config '{"remoteNodeNetworks":[{"cidrs":["10.80.0.0/16"]}],"remotePodNetworks":[{"cidrs":["10.85.0.0/16"]}]}'
```
- The CIDRs must not overlap each other, the cluster VPC CIDR or the Kubernetes service CIDR; routes in the VPC and on-prem for both.
- Node credentials: SSM hybrid activations or IAM Roles Anywhere (the networking page lists the endpoints each needs).

## 2. Join a node
Install the hybrid node tooling on each host and register it with the cluster using the steps in the EKS hybrid nodes guide.
- CNI: Cilium or Calico on hybrid nodes (VPC CNI stays on cloud nodes); AWS recommends making on-prem pod CIDRs routable.
- Webhooks can run on hybrid nodes only when the control plane can reach the pod IPs; otherwise run them on cloud nodes.
- Not for disconnected or intermittent-link (DDIL) sites; hybrid nodes must not run on cloud infrastructure.
- Billed per hour for hybrid node vCPU while attached; see the EKS pricing page.

## 3. EKS Anywhere: everything on-prem
User-managed clusters on VMware vSphere, Bare Metal, Nutanix or AWS Snow, built on Cluster API. Can run
air-gapped; optional Enterprise Subscription for support and Curated Packages.

## 4. Choosing
| Situation | Choose |
|---|---|
| Reliable link to AWS, want managed control plane | Hybrid Nodes |
| Air-gapped or no dependency on AWS Region | EKS Anywhere |
| Edge with intermittent link | EKS Anywhere |

## Checked
2026-11-01: confirmed against the EKS hybrid nodes overview and networking pages and the EKS Anywhere overview (CIDR rules, Cilium/Calico, webhooks, DDIL limit, SSM and IAM Roles Anywhere, infrastructure list, air-gapped, subscription); create-cluster flags checked against the botocore model. Removed: access-entry type, CloudStack, BGP, pinned versions and nodeadm specifics.
Method: documentation only; no commands were run.

## Verify
- [ ] `kubectl get nodes -o wide` lists hybrid nodes `Ready` with on-prem IPs.
- [ ] A pod on a hybrid node can reach a ClusterIP service backed by cloud pods.
