---
id: computing-software.cybersecurity-defensive.cloud-security.vpc-flow-logs
name: vpc-flow-logs
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-detection, vpc-flow-logs, flow-log-analysis, nsg-flow-logs, vnet-flow-logs, gcp-vpc-flow-logs, athena, custom-log-format, network-forensics]
level: practitioner
status: docs-checked
description: "Enable and use AWS VPC flow logs with custom fields, S3 Parquet storage and known limits, with Azure virtual network flow log notes, for investigations."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-create-flow-log.html", "https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC flow logs

**Goal:** a record of network connections in cloud networks for investigations and detection,
centrally stored and queryable.

## AWS setup
Enable at VPC level, publish to a central S3 bucket in the log archive account, Parquet format
(columnar; the docs say queries are 10 to 100 times faster than plain text), hourly partitions,
with a custom format including useful fields:
```
aws ec2 create-flow-logs --resource-type VPC --resource-ids vpc-0abc --traffic-type ALL \
  --log-destination-type s3 --log-destination arn:aws:s3:::org-flowlogs/ \
  --destination-options FileFormat=parquet,HiveCompatiblePartitions=true,PerHourPartition=true \
  --log-format '${version} ${account-id} ${vpc-id} ${subnet-id} ${instance-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${pkt-srcaddr} ${pkt-dstaddr} ${flow-direction} ${traffic-path}'
```
- With a custom format the record version is the highest version among the fields you pick.
- `pkt-srcaddr` and `pkt-dstaddr` capture the original packet-level addresses: for egress traffic whose source is not one of the interface's addresses, `srcaddr` shows the primary private IPv4 address instead.
- `action` is `ACCEPT` or `REJECT`; a REJECT can be traffic blocked by security groups or network ACLs.
- Resource types accepted include VPC, Subnet, NetworkInterface, TransitGateway and TransitGatewayAttachment.

## Azure
Virtual network flow logs are written to a storage account that must be in the same region as the virtual network and use the standard performance tier (premium is not supported). Traffic analytics is optional and billed per GB processed. Traffic is not recorded at a private endpoint itself; capture it at the source VM.

## Investigation questions
Outbound connections from a suspect instance (group by destination address and port, sum bytes), rejected inbound traffic to sensitive subnets (scanning), unusual ports from workloads and large egress to new destinations. Query the S3 data with Athena or your SIEM.

## Gotchas
- A flow is aggregated over a maximum interval of 10 minutes by default; set `--max-aggregation-interval 60` (1 minute) for faster visibility, at the cost of more records.
- Delivery is best effort: typically about 5 minutes to CloudWatch Logs and about 10 minutes to S3.
- Records carry no payload and no DNS names.
- Not logged: traffic to the Amazon DNS server (if you use your own DNS server it is logged), instance metadata traffic to 169.254.169.254, and Amazon Time Sync traffic to 169.254.169.123. The limitations page lists other exclusions.
- Cost: `ALL` traffic on busy VPCs is large; S3 with Parquet and lifecycle rules keeps it manageable.

## Verify
- [ ] Every VPC in every account has flow logs to the central bucket.
- [ ] A query for a known test connection returns the expected record.

## Checked
Checked 2026-11-09 against the AWS VPC User Guide pages (flow log records, limitations, publishing to S3) and the Azure virtual network flow logs overview; the `create-flow-logs` options, `DestinationOptions` members and the `MaxAggregationInterval` parameter were checked against the botocore EC2 model. Removed unconfirmed claims: GuardDuty consuming flow logs, Config rules and Control Tower enforcement, GCP VPC flow log settings, the NSG retirement statement, the Athena SQL sample, and the CIS control reference.
Method: documentation only; no commands were run.
