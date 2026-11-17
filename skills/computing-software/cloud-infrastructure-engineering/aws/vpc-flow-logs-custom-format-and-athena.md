---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-flow-logs-custom-format-and-athena
name: vpc-flow-logs-custom-format-and-athena
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-flow-logs, flow-log-format, custom-fields, aggregation-interval, flow-logs-athena, flow-log-queries, rejected-traffic]
level: practitioner
status: docs-checked
description: "Create VPC flow logs with custom fields and 1-minute aggregation to S3 as Parquet, then query them in Athena and Logs Insights for rejects and top talkers."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-path.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-athena.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html", "https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs-create-table-statement.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-examples.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC flow logs: custom format and Athena queries

## 1. Create with the fields you will actually need
The default format only has the version 2 fields and cannot be changed. To capture newer fields use a custom format:
```bash
aws ec2 create-flow-logs --resource-type VPC --resource-ids vpc-123 --traffic-type ALL \
  --log-destination-type s3 --log-destination arn:aws:s3:::org-flow-logs/ \
  --max-aggregation-interval 60 \
  --destination-options FileFormat=parquet,HiveCompatiblePartitions=true,PerHourPartition=true \
  --log-format '${version} ${account-id} ${vpc-id} ${subnet-id} ${instance-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr} ${region} ${az-id} ${flow-direction} ${traffic-path} ${pkt-src-aws-service} ${pkt-dst-aws-service}'
```
- `pkt-srcaddr`/`pkt-dstaddr`: original IPs behind NAT gateways and load balancers.
- `flow-direction`, `traffic-path` (egress traffic only; 1 = through another resource in the same VPC, 2 = internet gateway or gateway endpoint, 3 = virtual private gateway, 4 = intra-region peering, 5 = inter-region peering, 6 = Local or Wavelength Zone, 7 = gateway endpoint, 8 = internet gateway): where traffic went.
- `pkt-*-aws-service`: identifies S3, DynamoDB, EC2 etc. — great for NAT cost analysis.
- `tcp-flags`: SYN-only flows = connection attempts never answered.
- Aggregation 60 s instead of the default 10 minutes (600 s) for troubleshooting accuracy, at the cost of more records; ENIs on Nitro-based instances aggregate at 1 minute or less anyway.
- The configuration and record format can't be changed after creation; create a new flow log.

## 2. Athena
Use the **Athena integration** (it generates a CloudFormation template that creates the required resources and predefined queries; a Lambda loads new partitions on a schedule), or define a table yourself
(AWS documents partitioning by year/month/day or partition projection for the Athena table). Column names follow the field names with underscores, such as `interface_id`, `pkt_srcaddr`, `flow_direction`.

Rejected traffic by destination port (last hour):
```sql
SELECT dstaddr, dstport, protocol, count(*) flows, sum(packets) pkts
FROM vpc_flow_logs
WHERE action = 'REJECT' AND year='2026' AND month='10' AND day='16' AND hour='14'
GROUP BY 1,2,3 ORDER BY flows DESC LIMIT 25;
```
Top talkers through NAT to the internet:
```sql
SELECT pkt_srcaddr, pkt_dst_aws_service, sum(bytes)/1e9 gb
FROM vpc_flow_logs
WHERE interface_id = 'eni-natgw' AND flow_direction = 'egress' AND day='16'
GROUP BY 1,2 ORDER BY gb DESC LIMIT 20;
```

## 3. Logs Insights (if sent to CloudWatch Logs)
```
filter action = "REJECT"
| stats count(*) as rejects by srcAddr, dstAddr, dstPort
| sort rejects desc | limit 20
```
(Fields are auto-discovered for the default format; custom formats need `parse`.)

## Gotchas
- Flow logs don't capture: traffic to the Amazon DNS server (unless you use your own DNS server), Windows license activation, instance metadata (169.254.169.254), Amazon Time Sync (169.254.169.123),
  DHCP, mirrored traffic at the source, and traffic to the default VPC router's reserved address.
- A REJECT on the return path usually means NACL (stateless): AWS's example shows an ACCEPT for the request and a REJECT for the reply when the NACL has no outbound rule.
- Delivery is best effort: typically about 5 minutes to CloudWatch Logs and about 10 minutes to S3; S3 log files are published every 5 minutes.

## Verify
- [ ] `aws ec2 describe-flow-logs` shows the custom format and `MaxAggregationInterval: 60`.
- [ ] Parquet objects appear under `AWSLogs/aws-account-id=<ACCOUNT_ID>/aws-service=vpcflowlogs/aws-region=<REGION>/year=.../month=.../day=.../hour=.../` (Hive-compatible, hourly).
- [ ] A test blocked connection shows as REJECT in the Athena query after the typical S3 delivery delay (about 10 minutes, best effort).

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (flow log records, flow log files, limitations, flow log examples, Athena), the Athena User Guide (VPC flow log table) and the CloudWatch Logs Insights query examples, plus the botocore EC2 model.
- Default format, aggregation interval defaults, `traffic-path` values 1 to 8 (egress only), field names (`pkt-srcaddr`, `pkt-src-aws-service`, `flow-direction`, `tcp-flags`, `az-id`, `region`) and the not-captured list confirmed.
- Hive-compatible hourly S3 prefix layout confirmed on the flow log files page; the verify path was corrected.
- Athena column names (`interface_id`, `pkt_srcaddr`, `pkt_dst_aws_service`, `flow_direction`) and the partitioning options confirmed on the Athena guide; CloudWatch Logs Insights VPC flow log field names confirmed on the query examples page.
- Removed the claim that security groups reject only inbound traffic (replaced with the documented example) and the per-GB cost statement.

Method: documentation only; no commands were run.
