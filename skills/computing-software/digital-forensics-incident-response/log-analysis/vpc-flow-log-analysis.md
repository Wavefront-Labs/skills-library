---
id: computing-software.digital-forensics-incident-response.log-analysis.vpc-flow-log-analysis
name: vpc-flow-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [vpc-flow-logs, cloud-logs, netflow, dfir]
level: advanced
status: docs-checked
description: "Investigate with AWS VPC, Azure virtual network and GCP VPC flow logs: record fields, aggregation and sampling limits, and what each cannot show."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview", "https://cloud.google.com/vpc/docs/flow-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC flow log analysis

**Goal:** flow logs record who talked to whom, on what port, how much, and whether it was
accepted or rejected. They are often the only network evidence for cloud workloads. They are
not payload captures.

## AWS VPC Flow Logs
- A record is a space-separated string describing a flow (5-tuple, per network interface)
  within an aggregation interval. Fields that do not apply show `-`; metadata fields that do not
  come from the packet header are best-effort and may be missing or inaccurate.
- **Default format** is the version 2 fields in this order and cannot be changed:
  `version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status`.
  A custom format (at least one field, any order) can add fields from later versions, such as
  `vpc-id`, `subnet-id`, `instance-id`, `tcp-flags`, `type`, `pkt-srcaddr`, `pkt-dstaddr`
  (version 3), `region`, `az-id` (4), `pkt-src-aws-service`, `pkt-dst-aws-service`,
  `flow-direction`, `traffic-path` (5), and later ECS, `reject-reason`, `resource-id` and
  `next-hop-*` fields.
- `pkt-srcaddr`/`pkt-dstaddr` are the packet-level (original) addresses; compare them with
  `srcaddr`/`dstaddr` to tell an intermediate layer, such as a NAT gateway interface or an EKS
  pod's node, from the original address.
- `action` is ACCEPT or REJECT (REJECT includes traffic denied by security groups or network
  ACLs, or packets arriving after the connection closed). `log-status` is OK, NODATA or
  SKIPDATA (records skipped because of capacity or an internal error).
- `tcp-flags` is a bitmask of FIN (1), SYN (2), RST (4), SYN-ACK (18); flags can be OR-ed over
  the interval, and unsupported flags such as ACK or PSH alone give 0.
- `start` and `end` are Unix seconds and may be up to 60 seconds off the packet times.
- Maximum aggregation interval is 10 minutes by default, or 1 minute if specified; on Nitro
  instances it is always 1 minute or less. Delivery typically takes about 5 minutes to
  CloudWatch Logs and about 10 minutes to S3, best effort.
- `flow-direction` is ingress or egress; `traffic-path` codes describe the egress route, for
  example 2 through an internet gateway or gateway endpoint and 3 through a virtual private gateway.

## Azure
Virtual network flow logs are written in JSON, to a storage account in the same region as the
virtual network. Microsoft compares them with network security group flow logs and recommends
disabling NSG flow logs before enabling virtual network flow logs on the same workloads to
avoid duplicate recording and cost. Traffic analytics is available as an add-on; see the
overview for regional support.

## GCP
VPC Flow Logs samples packets (the primary sampling rate is dynamic and cannot be adjusted),
aggregates by 5-tuple over a configurable interval (5 seconds default; 30 seconds, 1, 5, 10 or
15 minutes) and applies a configurable secondary sampling rate. It estimates total traffic from
sampled packets, so short or low-volume connections can be missed unless you enable TCP
connection logging. Entries go to Cloud Logging in the project of the VPC network.

## Investigative patterns (analyst judgement)
Large outbound byte totals to new destinations, regular small flows to one external address,
and internal flows between workloads that do not normally communicate are worth pivoting on.
Always compare against a baseline for the same workload.

## Gotchas
- Flow logs must be enabled; record the coverage (which VPCs, since when, sampling settings)
  next to every conclusion.
- No payload and no DNS names; join with DNS logs from the platform.
- Aggregation and sampling mean small or short flows may be missing.

## Checked
2026-11-09. Confirmed on the AWS flow-log-records page (read in full), the Azure virtual network flow logs overview (searched for JSON, NSG comparison, storage location; not read in full) and the GCP flow logs page (searched for sampling and aggregation; not read in full). Removed: Athena query, NTANetAnalytics and BigQuery field names, NSG retirement date, crypto-mining ports, exfiltration/C2 thresholds, Route 53 resolver log reference.
Method: documentation only; no commands were run.
