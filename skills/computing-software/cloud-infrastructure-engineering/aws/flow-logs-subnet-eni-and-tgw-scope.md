---
id: computing-software.cloud-infrastructure-engineering.aws.flow-logs-subnet-eni-and-tgw-scope
name: flow-logs-subnet-eni-and-tgw-scope
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-flow-logs, eni-flow-logs, subnet-flow-logs, transit-gateway-flow-logs, troubleshooting]
level: practitioner
status: docs-checked
description: "Pick the right VPC flow log scope (VPC, subnet, ENI, Transit Gateway or attachment), traffic type and interval, and know which traffic is never logged."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-basics.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html", "https://docs.aws.amazon.com/vpc/latest/userguide/working-with-flow-logs.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-flow-logs.html", "https://docs.aws.amazon.com/vpc/latest/tgw/flowlog-s3-create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow log scope: VPC, subnet, ENI, Transit Gateway

## 1. Scope choices
| Resource type | Use for |
|---|---|
| `VPC` | baseline security record of everything |
| `Subnet` | one tier (DMZ, data) at lower volume |
| `NetworkInterface` | a single instance, or an interface created by another service (Elastic Load Balancing, RDS, ElastiCache, Redshift, WorkSpaces, NAT gateways) while debugging |
| `TransitGateway` / `TransitGatewayAttachment` | inter-VPC and hybrid traffic through the TGW |
A resource can have several flow logs (for example VPC-wide to S3 plus a short-lived ENI log to CloudWatch).

## 2. Create targeted logs
```bash
aws ec2 create-flow-logs --resource-type NetworkInterface --resource-ids eni-0abc \
  --traffic-type REJECT --max-aggregation-interval 60 \
  --log-destination-type cloud-watch-logs --log-group-name /flowlogs/debug-eni \
  --deliver-logs-permission-arn arn:aws:iam::<ACCOUNT_ID>:role/flowlogs-to-cwl
aws ec2 create-flow-logs --resource-type TransitGateway --resource-ids tgw-0abc \
  --log-destination-type s3 --log-destination arn:aws:s3:::flowlogs-<ACCOUNT_ID>/tgw/
```
- `--traffic-type` ACCEPT, REJECT or ALL (the documented Transit Gateway example passes no traffic type).
- Maximum aggregation interval: 60 s for debugging, 600 s (the default, 10 minutes) for volume; on Nitro-based
  instances the interval is always 1 minute or less.
- For an interface owned by another AWS service, use the EC2 console or EC2 API to create the interface-level flow log.
  A flow log on a subnet or VPC covers every network interface in it, including ones launched later.

## 3. Never logged
Traffic to the Amazon DNS server (queries to your own DNS server are logged), instance metadata (169.254.169.254),
Time Sync (169.254.169.123), DHCP, Windows license activation, the default VPC router reserved IP, mirrored source
traffic (you see the mirror target only), ARP, and traffic between an endpoint network interface and a Network Load
Balancer network interface. Flow logs cannot be enabled for a peered VPC unless that VPC is in your account. Transit
Gateway flow logs do not support multicast traffic; Connect traffic appears under the transport attachment.

## 4. Remove debug logs
```bash
aws ec2 delete-flow-logs --flow-log-ids fl-0abc
```

## Verify
- [ ] Records for the ENI appear within the aggregation interval plus delivery delay (a few minutes).
- [ ] TGW flow log records show the `tgw-attachment-id` and `tgw-pair-attachment-id` fields for the inter-VPC path.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "Flow logs basics", "Flow log records", "Flow log limitations" and "Work with flow logs"; Transit Gateways Guide pages "AWS Transit Gateway Flow Logs" and "Create a Transit Gateway Flow Logs record that publishes to Amazon S3"; botocore EC2 model (FlowLogsResourceType, CreateFlowLogs).
Confirmed: resource types VPC, Subnet, NetworkInterface, TransitGateway, TransitGatewayAttachment; default 10-minute and optional 1-minute aggregation interval; the not-logged traffic list; TGW create command shape; tgw-attachment-id and tgw-pair-attachment-id record fields; flow logs on subnet or VPC cover every interface.
Corrected: interfaces owned by other AWS services can have interface-level flow logs through the EC2 console or API (the skill implied VPC or subnet scope only); the Resolver query logs hint was removed because the pages do not say it.

Method: documentation only; no commands were run.
