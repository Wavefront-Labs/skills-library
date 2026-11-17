---
id: computing-software.cloud-infrastructure-engineering.aws.fis-rds-failover-and-network-disruption-actions
name: fis-rds-failover-and-network-disruption-actions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fault-injection-service, fis, rds-failover-action, network-disruption, disrupt-connectivity, aurora-failover]
level: practitioner
status: docs-checked
description: "Test DB and network resilience with FIS actions: Aurora cluster failover, Multi-AZ reboot with failover, disrupt-connectivity on subnets and cross-region network disruption."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html", "https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIS RDS failover and network disruption actions

## Database actions
| Action | Effect |
|---|---|
| `aws:rds:failover-db-cluster` | runs FailoverDBCluster on an Aurora (or DocumentDB) cluster, resource type `aws:rds:cluster` |
| `aws:rds:reboot-db-instances` with `forceFailover=true` | runs RebootDBInstance on `aws:rds:db` targets; forces failover to another AZ for Multi-AZ instances (default false) |
```json
"actions": {"failover": {"actionId": "aws:rds:failover-db-cluster", "targets": {"Clusters": "ordersDb"}}},
"targets": {"ordersDb": {"resourceType": "aws:rds:cluster",
  "resourceTags": {"fis-target": "orders"}, "selectionMode": "ALL"}}
```
What to observe: application error duration, connection pool recovery, DNS caching (JVM TTL),
RDS Proxy behaviour, writes retried idempotently.

## Network actions
| Action | Effect |
|---|---|
| `aws:network:disrupt-connectivity` | blocks traffic for target subnets; `scope`: `all`, `availability-zone`, `dynamodb`, `prefix-list`, `s3`, `s3express`, `vpc` (`prefix-list` also needs `prefixListIdentifier`) |
| `aws:network:route-table-disrupt-cross-region-connectivity` | removes routes to other regions' CIDRs |
| `aws:network:transit-gateway-disrupt-cross-region-connectivity` | blocks TGW peering traffic |
| `aws:ec2:api-insufficient-instance-capacity-error` | injects an insufficient-capacity error into EC2 API calls made by a target IAM role |
| `aws:network:disrupt-vpc-endpoint` | disrupts VPC endpoint connectivity |
```json
"actions": {"isolateAz": {"actionId": "aws:network:disrupt-connectivity",
  "parameters": {"duration": "PT10M", "scope": "all"}, "targets": {"Subnets": "azA"}}}
```
- `disrupt-connectivity` clones the subnet's network ACL, adds deny rules (tagged `managedByFIS=true`), associates the clone for the duration, and restores the original at the end. Duration is 1 minute to 12 hours (ISO 8601). With `scope=all`, intra-subnet traffic is still allowed; for any other scope the network ACL entry maximum is 20, and at most 30 subnets per VPC can be targeted with `availability-zone`.
- Keep an access path to your instances that does not depend on the disrupted subnets.

## Safety
- Stop conditions on SLO alarms; short durations first (2-5 minutes).
- Make sure the experiment role has the network ACL permissions the action lists.

## Verify
- [ ] Measured failover impact (seconds of errors) recorded and within SLO.
- [ ] Network disruption shows services in other AZs continue; alarms fire as expected.

## Checked
2026-10-28: Confirmed against the FIS User Guide actions reference: aws:rds:failover-db-cluster (FailoverDBCluster, Aurora and DocumentDB, resource type aws:rds:cluster), aws:rds:reboot-db-instances (forceFailover default false, aws:rds:db), aws:network:disrupt-connectivity (cloned network ACL, managedByFIS tag, scope values all/availability-zone/dynamodb/prefix-list/s3/s3express/vpc, duration 1 minute to 12 hours, limits of 20 ACL entries and 30 subnets), the cross-region route table and transit gateway actions, disrupt-vpc-endpoint, and the EC2 insufficient capacity API error action. Read end to end. Error fixed: the skill listed rds stop actions that are not in the reference and an incomplete scope list. Removed: the 30-60 s failover expectation, the claim that SSM/bastion access is lost, NACL statelessness remark, the aws:ec2:api-* wildcard row, and the maintenance-window advice. Sources now point to the FIS User Guide.

Method: documentation only; no commands were run.
