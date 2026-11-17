---
id: computing-software.cloud-infrastructure-engineering.rancher.hosted-eks-cluster-create-prerequisites
name: hosted-eks-cluster-create-prerequisites
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [eks, hosted-clusters, iam, vpc, cloud-credentials, aws]
level: practitioner
status: docs-checked
description: "Create an EKS cluster from Rancher: the VPC, a minimal-permission IAM user and access keys, and the cluster creation flow."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-clusters-in-rancher-setup/set-up-clusters-from-hosted-kubernetes-providers/eks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher can create and manage clusters on Amazon EKS, where AWS runs the control plane across multiple Availability Zones. Deploying to AWS incurs charges.

**Prerequisites in AWS**

- An **Amazon VPC**. You can create and supply one at cluster creation; if you do not, Rancher creates one.
- An IAM user for Rancher with programmatic access, plus an IAM policy granting it the minimum permissions required for an EKS cluster (the page lists them in a Minimum EKS Permissions section). Keep access minimal, then create an access key and secret key for that user.
- Rotate those keys regularly; the page links AWS guidance on rotation.

**Create the cluster:** **Cluster Management > Create > Amazon EKS**, enter a cluster name, set **Member Roles** for access, fill in the rest of the form and click **Create**. The cluster shows as **Provisioning** until it becomes **Active**, and then receives two projects: `Default` (containing the `default` namespace) and `System` (containing `cattle-system`, `traefik`, `kube-public` and `kube-system`).

The full list of options lives in the separate EKS cluster configuration reference.

## Checked

2026-11-09. Read the cited Creating an EKS Cluster page in full and checked every claim against it (VPC, IAM user and policy, key rotation, creation steps, Default and System projects). Removed the managed node group and ingress controller constraints, which came from other pages.

Method: documentation only; no commands were run.
