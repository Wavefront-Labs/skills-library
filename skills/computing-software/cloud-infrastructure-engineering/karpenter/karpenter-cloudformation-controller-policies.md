---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-cloudformation-controller-policies
name: karpenter-cloudformation-controller-policies
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [cloudformation, iam, controller-policy, sid, passrole, sqs, zonal-shift, ssm, pricing]
level: advanced
status: docs-checked
description: "The six KarpenterController* managed policies and their Sids: tag-scoped EC2 actions, instance profile management, EKS discovery, SQS queue, zonal shift and read-only discovery."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/cloudformation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter controller IAM policies

Six managed policies, each named `KarpenterController<Name>Policy-${ClusterName}`:

1. NodeLifecycle: EC2 instance and launch template operations, scoped by tags.
   - `AllowScopedEC2InstanceAccessActions`, `AllowScopedEC2LaunchTemplateAccessActions`, `AllowScopedEC2InstanceActionsWithTags` (run instances/fleet/launch template requiring request tags).
   - `AllowScopedResourceCreationTagging` and `AllowScopedResourceTagging` (CreateTags only at creation, or on instances with the cluster and `karpenter.sh/nodepool` tags).
   - `AllowScopedDeletion`: `ec2:TerminateInstances` and `ec2:DeleteLaunchTemplate` only where `karpenter.sh/nodepool` and `kubernetes.io/cluster/${ClusterName}` tags exist.
2. IAMIntegration: `AllowPassingInstanceRole` (`iam:PassRole` on the node role, `iam:PassedToService` ec2), `AllowScopedInstanceProfileCreationActions`, `AllowScopedInstanceProfileTagActions`, `AllowScopedInstanceProfileActions` (AddRoleToInstanceProfile, RemoveRoleFromInstanceProfile, DeleteInstanceProfile). Creation and tagging require request tags for the cluster (`owned`), `eks:eks-cluster-name`, region and a `karpenter.k8s.aws/ec2nodeclass` tag; the add/remove/delete actions require the resource tags for the cluster, region and ec2nodeclass.
3. EKSIntegration: `AllowAPIServerEndpointDiscovery` (`eks:DescribeCluster` on the cluster).
4. Interruption: `AllowInterruptionQueueActions` (`sqs:DeleteMessage`, `GetQueueUrl`, `ReceiveMessage` on the queue).
5. ZonalShift: `AllowZonalShiftStatusReadOnly` (`arc-zonal-shift:GetManagedResource` for the cluster).
6. ResourceDiscovery: `AllowRegionalReadActions` (Describe* for capacity reservations, images, instances, instance status, instance types and offerings, launch templates, placement groups, security groups, spot price history, subnets), `AllowSSMReadActions` (`ssm:GetParameter` on `/aws/service/*`), `AllowPricingReadActions` (`pricing:GetProducts`), `AllowUnscopedInstanceProfileListAction` and `AllowInstanceProfileReadActions`.

Adding a new node role means adding it to the PassRole resource list.

## Checked

2026-11-08. Confirmed against the CloudFormation reference (v1.13): policy names, Sids, actions and conditions. Corrected the IAMIntegration condition summary and added DescribeInstanceStatus to the regional read list; nothing else removed.

Method: documentation only; no commands were run.
