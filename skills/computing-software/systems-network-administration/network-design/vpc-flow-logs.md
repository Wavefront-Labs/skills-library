---
id: computing-software.systems-network-administration.network-design.vpc-flow-logs
name: vpc-flow-logs
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, vpc-flow-logs, nsg-flow-logs, traffic-analysis, security-monitoring]
level: practitioner
status: docs-checked
description: "Enable and use cloud flow logs (AWS VPC, Azure VNet, GCP VPC) to troubleshoot rejected traffic, find top talkers and feed security analytics, with cost control."
sources:
  - https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
  - https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview
  - https://cloud.google.com/vpc/docs/flow-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC flow logs

## What they capture
5-tuple metadata with byte and packet counts and timestamps, no payload. Google Cloud flow logs
sample packets and aggregate them by 5-tuple; each provider documents its own aggregation interval.

| Cloud | Feature | Destination |
|---|---|---|
| AWS | VPC Flow Logs | see the AWS flow-logs page for destinations |
| Azure | VNet flow logs | storage account in the same region as the VNet, optionally traffic analytics |
| GCP | VPC Flow Logs | Cloud Logging (exportable) |

## Troubleshooting with them
- Connection fails: compare a rejected-flow record on the destination interface with no record at
  all (the traffic never arrived: look at routing).
- Find who talks to a database: filter by dstport and dst ENI.
- NAT gateway cost spikes: top talkers through the NAT ENI.

## Cost and retention
Flow logs add storage and processing cost (Azure bills flow-log volume and traffic analytics
processing separately; see the vendor pricing pages). Enable on critical networks first and set
retention by compliance need. Google's page says flow logs are stored in Cloud Logging for 30 days.

## Verify
- [ ] Flow logs enabled on production VPCs with retention defined; a test denied connection shows up as a denied flow within the provider's aggregation interval.

## Checked

- Date: 2026-10-28
- Confirmed: GCP flow logs sample packets, aggregate by 5-tuple, go to Cloud Logging and are stored for 30 days; Azure VNet flow logs need a storage account in the same region and can feed traffic analytics, with billing for volume (vnet-flow-logs-overview, flow-logs pages).
- Removed: AWS 1 or 10 minute windows, custom field names, CloudWatch/S3/Firehose destinations, NSG-retirement remark, BigQuery, Athena query, the NACL ephemeral-port remark (AWS page too short to confirm).

Method: documentation only; no commands were run.
