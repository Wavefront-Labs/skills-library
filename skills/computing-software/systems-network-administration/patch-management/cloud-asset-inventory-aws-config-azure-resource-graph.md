---
id: computing-software.systems-network-administration.patch-management.cloud-asset-inventory-aws-config-azure-resource-graph
name: cloud-asset-inventory-aws-config-azure-resource-graph
category: computing-software
field: systems-network-administration
product: patch-management
tags: [aws-config-inventory, azure-resource-graph, asset-inventory, software-inventory, ssm-inventory, cloud]
level: practitioner
status: docs-checked
description: "Build a patch-ready cloud server inventory with AWS Config/SSM Inventory and Azure Resource Graph queries, find unmanaged instances, and reconcile against the patch tool."
sources:
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html
  - https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud asset inventory for patching

Cloud estates change daily; the patch tool only covers what has its agent. Inventory from
the control plane, then subtract what the patch tool sees = unmanaged gap.

## AWS
All instances across accounts/regions (AWS Config aggregator or Resource Explorer):
```sh
aws configservice select-aggregate-resource-config --configuration-aggregator-name org-agg \
  --expression "SELECT resourceId, accountId, awsRegion, configuration.instanceType, tags WHERE resourceType = 'AWS::EC2::Instance'"
```
Which are SSM-managed (needed for Patch Manager and SSM Inventory):
```sh
aws ssm describe-instance-information --query "InstanceInformationList[].[InstanceId,PingStatus,PlatformName,PlatformVersion,AgentVersion]" --output table
```
Unmanaged = EC2 list minus SSM list. Common causes: no instance profile with
`AmazonSSMManagedInstanceCore`, no route to SSM endpoints (add VPC endpoints), agent missing
on custom AMIs.
Installed software: enable SSM Inventory (a State Manager association),
query via Resource Data Sync to S3 + Athena, or per instance with
`aws ssm list-inventory-entries --instance-id <INSTANCE_ID> --type-name AWS:Application`
(both `--instance-id` and `--type-name` are required).

## Azure
Resource Graph (KQL) across subscriptions:
```kusto
resources
| where type =~ 'microsoft.compute/virtualmachines'
| project name, subscriptionId, resourceGroup, location, tags
```
Arc-enabled servers (on-prem/other clouds): `type =~ 'microsoft.hybridcompute/machines'`.
Patch state from Azure Update Manager:
```kusto
patchassessmentresources
| where type =~ 'microsoft.compute/virtualmachines/patchassessmentresults'
| project id, counts = properties.availablePatchCountByClassification, rebootPending = properties.rebootPending
```
Run in portal Resource Graph Explorer or `az graph query -q "<kql>" --first 1000`.
Update Manager keeps assessment history for 7 days and installation history for 30 days in Resource Graph.

## Reconcile
Join control-plane inventory with patch-tool inventory on instance ID; report (a) missing
agent, (b) agent not reporting recently, (c) no owner tag. Feed to the CMDB and to the
maintenance-group assignment (via tags).

## Verify
Unmanaged count trends to zero; every running instance has an owner and patch group tag;
spot-check a new instance appears in both inventories within a day.

## Checked
2026-11-01. Confirmed: SSM `ListInventoryEntries` requires InstanceId and TypeName (botocore model); `DescribeInstanceInformation` operation; Config aggregate query fields and `patchassessmentresources` table, `availablePatchCountByClassification`, `rebootPending` and the 7/30-day history (Learn Update Manager page); Arc `microsoft.hybridcompute/machines` type (Resource Graph tables reference). Removed: unconfirmed VM property paths, `status`, association name, fixed staleness threshold.
Method: documentation only; no commands were run.
