---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-cloudformation-node-role-and-overview
name: karpenter-cloudformation-node-role-and-overview
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [cloudformation, iam, node-role, managed-policies, eksctl, irsa, pod-identity]
level: practitioner
status: docs-checked
description: "The Getting Started cloudformation.yaml: KarpenterNodeRole with four managed policies, the three section groups, naming by ClusterName, and reusing an existing node role."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/cloudformation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cloudformation.yaml overview and node role

The Getting Started guide uses `cloudformation.yaml` to prepare an EKS cluster for Karpenter. It sets up three areas:
- Node Authorization: IAM permissions for nodes Karpenter launches. The template creates a role and related resources but not the IAM identity mapping that authorises nodes to the cluster; the guide has `eksctl` do that.
- Controller Authorization: six managed IAM policies for the controller, attached to the controller service account's role (`eksctl` creates the service account).
- Interruption Handling: an SQS queue and EventBridge rules so the controller receives EC2 interruption and health events.

Names are built from the cluster name, substituted as `${ClusterName}` (cluster `bob-karpenter-demo` gives `KarpenterNodeRole-bob-karpenter-demo`). ARNs use a partition, usually `aws` but possibly `aws-cn` or `aws-us-gov`. The page documents no Parameters section.

## KarpenterNodeRole
Defines the IAM role attached to generated instance profiles; its trust policy allows EC2 to assume it. Four AWS managed policies are attached:
- `AmazonEKS_CNI_Policy`: Amazon VPC CNI plugin permissions.
- `AmazonEKSWorkerNodePolicy`: lets worker nodes connect to EKS clusters.
- `AmazonEC2ContainerRegistryPullOnly`: pull images from Amazon ECR.
- `AmazonSSMManagedInstanceCore`: Systems Manager core functions.

To reuse an existing node role, skip this resource, pass that role to your EC2NodeClasses, and grant `iam:PassRole` on it in the controller's IAM Integration policy.

## Controller policies
Six managed policies, each suffixed `-${ClusterName}`: NodeLifecycle, IAMIntegration, EKSIntegration, Interruption, ZonalShift and ResourceDiscovery (named `KarpenterController<Name>Policy`). On an existing cluster you create them yourself and attach them to the controller's role using IRSA or EKS Pod Identity.

The page does not cover EKS access entries or the `aws-auth` ConfigMap, nor how to download a specific version of the template.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 cloudformation.md reference page; removed the curl download command as not in the page and added the controller policy names. Node role policies, trust and reuse guidance unchanged.
