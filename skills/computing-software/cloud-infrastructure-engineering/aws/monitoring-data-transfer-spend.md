---
id: computing-software.cloud-infrastructure-engineering.aws.monitoring-data-transfer-spend
name: monitoring-data-transfer-spend
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transfer-monitoring, data-transfer, cur-athena, flow-logs, cross-az-transfer, egress-cost]
level: advanced
status: draft
description: "Monitor and attribute AWS data transfer costs: CUR queries by usage type and resource, flow-log based traffic attribution, budgets and anomaly monitors for transfer."
sources: ["https://docs.aws.amazon.com/cur/latest/userguide/cur-data-transfers-charges.html", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2.html", "https://aws.amazon.com/blogs/architecture/overview-of-data-transfer-costs-for-common-architectures/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitoring data transfer spend

## 1. Find it in the bill
Data transfer is spread across services (EC2-Other, S3, CloudFront, RDS, ELB, NAT). In
CUR 2.0 (Athena):
```sql
SELECT line_item_usage_account_id AS acct,
       product_region_code AS region,
       line_item_usage_type AS usage_type,
       line_item_resource_id AS resource,
       SUM(line_item_usage_amount) AS gb,
       SUM(line_item_unblended_cost) AS cost
FROM cur2
WHERE billing_period = '2026-10'
  AND (line_item_usage_type LIKE '%DataTransfer%' OR line_item_usage_type LIKE '%-Out-Bytes'
       OR line_item_usage_type LIKE '%-In-Bytes' OR line_item_usage_type LIKE '%NatGateway-Bytes')
GROUP BY 1,2,3,4 ORDER BY cost DESC LIMIT 50;
```
Key usage types: `DataTransfer-Out-Bytes` (internet), `DataTransfer-Regional-Bytes`
(cross-AZ, VPC peering in-region), `<REG1>-<REG2>-AWS-Out-Bytes` (inter-region),
`NatGateway-Bytes`, `VpcEndpoint-Bytes`, `TransitGateway-Bytes`, CloudFront
`DataTransfer-Out-Bytes` by edge region.
`line_item_resource_id` attributes many transfer lines to the instance/ENI/LB/bucket.

## 2. Who is talking to whom
The bill says "cross-AZ bytes on instance i-..." but not to what. VPC Flow Logs with
`az-id`, `pkt-srcaddr`, `pkt-dstaddr`, `flow-direction`, `traffic-path` fields in Athena:
```sql
SELECT srcaddr, dstaddr, az_id, SUM(bytes)/1e9 AS gb
FROM vpc_flow_logs
WHERE day BETWEEN '2026/10/01' AND '2026/10/17' AND flow_direction = 'egress'
GROUP BY 1,2,3 ORDER BY gb DESC LIMIT 50;
```
Join IPs to ENIs/services (ENI descriptions show ELB, RDS, EKS) to find chatty pairs in
different AZs, traffic hairpinning through NAT to AWS services, or replication streams.
Network Flow Monitor (CloudWatch) gives TCP flow metrics between workloads without
querying flow logs yourself.

## 3. Alerts
- AWS Budgets with a filter on usage type group "EC2: Data Transfer - Inter AZ", "Internet"
  or usage types `*DataTransfer*`, monthly threshold with forecast alerts.
- Cost Anomaly Detection monitor on services or a cost category "Data transfer".
- CloudWatch on `NatGateway BytesOutToDestination`, ELB `ProcessedBytes`, CloudFront
  `BytesDownloaded` for operational early warning.

## 4. Typical findings and fixes
- NAT bytes to S3/DynamoDB: add gateway endpoints (free).
- Cross-AZ: AZ-aware routing (topology aware hints in EKS, ALB cross-zone off where safe,
  same-AZ read replicas), consolidate chatty services in one AZ only if availability allows.
- Internet egress: put CloudFront in front (cheaper egress tiers, caching).
- Inter-region replication more frequent than RPO requires.

## Verify
- [ ] Monthly CUR query lists top data transfer resources by cost with owners.
- [ ] Budgets/anomaly monitors cover data transfer.
- [ ] Top cross-AZ and NAT flows identified and remediated or accepted.
