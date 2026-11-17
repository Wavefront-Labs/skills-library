---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.flow-logs
name: flow-logs
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, flow-logs, vpc-flow-logs, nsg-flow-logs, vnet-flow-logs, network-observability, traffic-analysis]
level: practitioner
status: draft
description: "Enable and use network flow logs (VPC Flow Logs, VNet flow logs, GCP VPC Flow Logs) for troubleshooting, security and cost, with sampling, fields, storage and queries."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html", "https://learn.microsoft.com/azure/network-watcher/vnet-flow-logs-overview", "https://cloud.google.com/vpc/docs/flow-logs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network observability with flow logs

## Setup
- **AWS**: VPC/subnet/ENI flow logs to S3 (Parquet, hourly partitions) or CloudWatch Logs; custom
  format adds fields like `pkt-srcaddr`, `flow-direction`, `traffic-path`, `vpc-id`, `az-id`.
- **Azure**: VNet flow logs (NSG flow logs are being retired - NSG flow logs creation ended June
  2025) to storage, optionally Traffic Analytics in Log Analytics.
- **Google Cloud**: enable per subnet with sampling rate and aggregation interval; export via
  Logging sinks to BigQuery.

## Uses and queries
- Troubleshooting: `REJECT` records for a source/destination pair show security group / NACL drops.
- Security: unexpected outbound destinations, port scans, data exfiltration volumes.
- Cost: top talkers across AZs/regions/NAT gateway (`traffic-path`, bytes by destination).
- Migration: dependency discovery.

Example Athena query (AWS, Parquet):
```sql
SELECT srcaddr, dstaddr, dstport, sum(bytes)/1e9 AS gb
FROM vpc_flow_logs WHERE action='ACCEPT' AND day='2026/10/17'
GROUP BY 1,2,3 ORDER BY gb DESC LIMIT 20;
```

## Gotchas
- Volume and cost: high-traffic VPCs generate large logs; use S3/Parquet over CloudWatch for
  bulk, sampling on GCP, retention policies.
- Flow logs record metadata only (no payloads) and are not real-time (aggregation interval).
- Some traffic is not logged (e.g. instance metadata, DHCP, AWS DNS resolver traffic).

## Verify
- [ ] Flow logs on for all production VPCs/VNets (policy enforced).
- [ ] Saved queries for top talkers and rejects available to on-call.
