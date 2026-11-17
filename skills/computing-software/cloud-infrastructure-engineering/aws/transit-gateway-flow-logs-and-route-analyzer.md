---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-flow-logs-and-route-analyzer
name: transit-gateway-flow-logs-and-route-analyzer
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-flow-logs, route-analyzer, network-manager, troubleshooting, packet-loss]
level: practitioner
status: docs-checked
description: "Troubleshoot Transit Gateway paths with Network Manager Route Analyzer and TGW flow logs: enable, key fields (packet-loss reasons), Athena queries and per-attachment metrics."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-flow-logs.html", "https://docs.aws.amazon.com/network-manager/latest/tgwnm/route-analyzer.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-cloudwatch-metrics.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-quotas.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/create-flow-logs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit Gateway flow logs and Route Analyzer

## 1. Route Analyzer first (control plane)
Register the TGW in a Network Manager global network, then:
```bash
aws networkmanager start-route-analysis --global-network-id global-network-0abc \
  --source TransitGatewayAttachmentArn=arn:aws:ec2:<REGION>:<ACCOUNT_ID>:transit-gateway-attachment/att-a,IpAddress=10.1.0.10 \
  --destination TransitGatewayAttachmentArn=arn:aws:ec2:<REGION>:<ACCOUNT_ID>:transit-gateway-attachment/att-b,IpAddress=10.2.0.20 \
  --include-return-path
aws networkmanager get-route-analysis --global-network-id global-network-0abc --route-analysis-id <ID>
```
Reports `CONNECTED` / `NOT_CONNECTED` with a reason code (`ROUTE_NOT_FOUND`, `BLACKHOLE_ROUTE_FOR_DESTINATION_FOUND`,
`CYCLIC_PATH_DETECTED`, `INACTIVE_ROUTE_FOR_DESTINATION_FOUND`, `POSSIBLE_MIDDLEBOX`...). Checks TGW route tables only —
not VPC route tables, customer gateway devices, security groups or network ACLs (use Reachability Analyzer or VPC flow logs
for those). The TGW must be registered in the global network, it does not work with intra-Region peering, and the return path
is reported only if the forward path succeeds.

## 2. TGW flow logs (data plane)
```bash
aws ec2 create-flow-logs --resource-type TransitGateway --resource-ids tgw-123 \
  --log-destination-type s3 --log-destination arn:aws:s3:::net-logs/tgw/ \
  --max-aggregation-interval 60 \
  --log-format '${version} ${resource-type} ${account-id} ${tgw-id} ${tgw-attachment-id} ${tgw-src-vpc-id} ${tgw-dst-vpc-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${log-status} ${type} ${packets-lost-no-route} ${packets-lost-blackhole} ${packets-lost-mtu-exceeded} ${packets-lost-ttl-expired} ${tcp-flags} ${region} ${flow-direction} ${pkt-src-aws-service} ${pkt-dst-aws-service}'
```
Can be scoped to one attachment (`--resource-type TransitGatewayAttachment`). Aggregation interval must be 60 seconds for
transit gateway resource types. Destinations: CloudWatch Logs, S3 or Firehose. Multicast traffic is not captured, and Connect
attachments are logged under their transport attachment. The **packets-lost-*** fields say why the TGW dropped traffic.

## 3. Athena query
```sql
SELECT tgw_attachment_id, srcaddr, dstaddr, dstport,
       sum(packets_lost_no_route) no_route, sum(packets_lost_blackhole) blackhole,
       sum(packets_lost_mtu_exceeded) mtu
FROM tgw_flow_logs
WHERE day = '<YYYY/MM/DD>'
GROUP BY 1,2,3,4
HAVING sum(packets_lost_no_route + packets_lost_blackhole + packets_lost_mtu_exceeded) > 0
ORDER BY 5 DESC LIMIT 50;
```

## 4. Metrics
`AWS/TransitGateway`: `PacketDropCountBlackhole`, `PacketDropCountNoRoute`, `BytesIn/Out`
per TGW and per attachment — alarm on drop counts rising.

## Gotchas
- MTU: the TGW supports 8500 bytes between VPC, Direct Connect, Connect and peering attachments, and 1500 over VPN;
  PMTUD is supported only for traffic entering on VPC and Connect attachments, so `mtu-exceeded` drops from other paths
  need MSS or MTU alignment.
- Flow logs record traffic seen by the TGW only; if `packets` are present but replies absent,
  look at the destination VPC (SG/NACL/VPC route table).

## Verify
- [ ] Route analysis between two attachments returns the expected status with return path.
- [ ] Flow log objects arrive in S3 (it can take several minutes to start); Athena query returns rows.
- [ ] A deliberately blackholed CIDR shows up in `packets_lost_blackhole`.

## Checked

Checked 2026-10-27 against the AWS Transit Gateway documentation (flow logs, CloudWatch metrics, quotas), the Network Manager Route Analyzer guide, the aws-cli ec2 create-flow-logs reference and the botocore networkmanager and ec2 models.
- Corrected: Route Analyzer reason codes are `ROUTE_NOT_FOUND`, `BLACKHOLE_ROUTE_FOR_DESTINATION_FOUND`, `CYCLIC_PATH_DETECTED`; MTU is 8500 for VPC, Direct Connect, Connect and peering attachments (1500 over VPN) and PMTUD works only on VPC and Connect attachments; aggregation interval must be 60 seconds for transit gateway resources; Route Analyzer does not work with intra-Region peering.
- Confirmed: flow log field names (`packets-lost-no-route`, `-blackhole`, `-mtu-exceeded`, `-ttl-expired`, `tcp-flags`, `flow-direction`, `pkt-src-aws-service`), destinations CloudWatch Logs/S3/Firehose, metrics `PacketDropCountBlackhole` and `PacketDropCountNoRoute`.
- Removed: the "within ~10 minutes" delivery figure (the docs say several minutes) and a fixed example date.

Method: documentation only; no commands were run.
