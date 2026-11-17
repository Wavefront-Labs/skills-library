---
id: computing-software.cloud-infrastructure-engineering.aws.tracing-traffic-through-nat-with-flow-log-pkt-fields
name: tracing-traffic-through-nat-with-flow-log-pkt-fields
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-flow-logs, pkt-srcaddr, nat-traffic-tracing, flow-direction, traffic-path, top-talkers]
level: advanced
status: docs-checked
description: "Find which instance is behind NAT, load balancer or EKS pod traffic using flow log pkt-srcaddr/pkt-dstaddr, flow-direction and traffic-path fields, with Athena queries."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-athena.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracing traffic through NAT and intermediaries with flow logs

**Problem:** the default flow log format records the packet's IP header at the ENI. On a NAT
gateway ENI the source is the NAT's private IP; on an EKS node the source may be the node
IP even though a pod sent it. The `pkt-*` fields show the original addresses.

## 1. Fields to add (custom format; `pkt-*` need version 3, `flow-direction` and `traffic-path` version 5, `ecs-*` version 7)
| Field | Meaning |
|---|---|
| `pkt-srcaddr` / `pkt-dstaddr` | Original source/destination of the packet, before NAT or for traffic through an intermediate ENI |
| `srcaddr` / `dstaddr` | Addresses as seen on this ENI |
| `flow-direction` | `ingress` or `egress` relative to the ENI |
| `traffic-path` | For egress: 1 through another resource in the same VPC, 2 internet gateway or gateway VPC endpoint, 3 virtual private gateway, 4 intra-region peering, 5 inter-region peering, 6 Local Zone or Wavelength Zone, 7 gateway VPC endpoint, 8 internet gateway; `-` if none apply |
| `pkt-src-aws-service` / `pkt-dst-aws-service` | e.g. `S3`, `AMAZON`, `EC2` when the other end is an AWS service range |
| `instance-id`, `subnet-id`, `az-id`, `vpc-id` | locating the ENI |
| `ecs-*` fields | ECS cluster, service, task, container fields when the traffic is from a running ECS task |

## 2. Who is using the NAT gateway?
On the NAT gateway's ENI, outbound internet traffic appears twice: client ENI to NAT
(`srcaddr` = client private IP), and NAT to internet (`srcaddr` = NAT private IP).
Use the **ingress** records on the NAT ENI from VPC
sources, or the client side:
```sql
SELECT pkt_srcaddr AS client, sum(bytes)/1e9 AS gb
FROM vpc_flow_logs
WHERE interface_id = 'eni-0nat...'       -- the NAT gateway ENI
  AND flow_direction = 'ingress'
  AND NOT (dstaddr LIKE '10.%')         -- destined outside the VPC
  AND day = '2026/10/17'
GROUP BY pkt_srcaddr ORDER BY gb DESC LIMIT 20;
```
Map client IPs to ENIs/instances with `describe-network-interfaces` and a filter on the private IP. Top talkers to S3 or DynamoDB through NAT
(`pkt_dst_aws_service = 'S3'`) are free wins for a gateway endpoint.

## 3. Load balancers and EKS
- EKS: a pod's IP can differ from the IP of the node's network interface (for communication
  within a VPC); compare `srcaddr` with `pkt-srcaddr` to separate the node ENI from the pod.
- Other intermediate layers (load balancers, other managed ENIs): the docs only state that
  `pkt-srcaddr`/`pkt-dstaddr` give the original addresses; test on your own traffic.

## 4. Logs Insights version (CloudWatch destination)
```
parse @message "* * * * * * * * * * * * * * * * * *" as version, account, eni, src, dst, sport, dport, proto, pkts, bytes, start, end, action, status, pktsrc, pktdst, dir, path
| filter eni = "eni-0nat" and dir = "ingress"
| stats sum(bytes)/1000000000 as gb by pktsrc | sort gb desc | limit 20
```
(the field order must match your custom format exactly).

## Gotchas
- Fields must be in the format at creation; existing flow logs with the default format
  lack them. Create a new flow log with a custom format.
- Flow logs record `instance-id` as `-` for requester-managed ENIs such as a NAT gateway's.
- The aggregation interval (maximum 10 minutes by default, optionally 1 minute) groups packets of a flow; bytes are summed over
  the window, so short spikes are smoothed.
- Flow logs do not capture payloads; for packet-level evidence use Traffic Mirroring.

## Verify
- [ ] Custom format includes `pkt-srcaddr`, `pkt-dstaddr`, `flow-direction`, `traffic-path`.
- [ ] The top-talker query identifies the instances behind NAT and matches the NAT gateway's CloudWatch byte totals roughly.
- [ ] Remediation (gateway endpoint for S3) reduces NAT bytes for the identified sources.

## Checked
2026-10-31. Confirmed in the flow-log-records page (available fields): pkt-srcaddr/pkt-dstaddr purpose (NAT gateway and EKS pod examples), flow-direction values, traffic-path values 1-8, pkt-src/dst-aws-service, ecs-* fields and their versions, 10-minute default and optional 1-minute aggregation interval, instance-id `-` for requester-managed ENIs. Corrected: traffic-path 6 meaning, version gates. Removed as unconfirmed: the AWS_VPC_K8S_CNI_EXTERNALSNAT behaviour, ALB/NLB pkt-srcaddr claims, Transit Gateway pkt-src fields, a pkt-srcaddr claim for NAT egress records, the NAT metric name and the describe-network-interfaces filter name.
Method: documentation only; no commands were run.
