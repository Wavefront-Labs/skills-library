---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-status-conditions
name: karpenter-ec2nodeclass-status-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [status, conditions, ready, subnetsready, amisready, validationsucceeded, troubleshooting, ec2nodeclass]
level: practitioner
status: docs-checked
description: "Reading EC2NodeClass status conditions (SubnetsReady, SecurityGroupsReady, InstanceProfileReady, AMIsReady, ValidationSucceeded and more) to see why a NodeClass is not Ready."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass status conditions

An EC2NodeClass is `Ready` when Karpenter discovers AMIs, instance profile, subnets, security groups and (AL2023 only) the cluster CIDR. NodePools referencing a NotReady class are not considered for scheduling.

| Condition | Meaning |
|---|---|
| SubnetsReady | subnets discovered |
| SecurityGroupsReady | security groups discovered |
| InstanceProfileReady | instance profile discovered |
| AMIsReady | AMIs discovered |
| ValidationSucceeded | EC2NodeClass validation passed |
| PlacementGroupReady | referenced placement groups discovered |
| CapacityReservationsReady | only when the capacity reservation feature is enabled |
| Ready | top level; False if any dependency is False, and its `message` names the unresolved one |

Inspect:

```bash
kubectl get ec2nodeclass default -o jsonpath='{.status.conditions}'
kubectl describe ec2nodeclass default
```

Resolved results in status: `subnets` (id, zone; sorted by free IPs), `securityGroups` (id, name), `amis` (id, name, requirements, `deprecated`), `capacityReservations`, `instanceProfile`. Check these first when nodes will not launch: an empty list means the selector terms matched nothing, for example a missing `karpenter.sh/discovery` tag.

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
