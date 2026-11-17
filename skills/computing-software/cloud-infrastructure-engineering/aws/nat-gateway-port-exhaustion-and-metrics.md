---
id: computing-software.cloud-infrastructure-engineering.aws.nat-gateway-port-exhaustion-and-metrics
name: nat-gateway-port-exhaustion-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-gateway, nat-metrics, errorportallocation, nat-port-exhaustion, cloudwatch, packetsdropcount, troubleshooting]
level: practitioner
status: docs-checked
description: "Monitor NAT gateways with CloudWatch (ErrorPortAllocation, PacketsDropCount, IdleTimeoutCount), diagnose port exhaustion and fix it with secondary IPs or traffic offload."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html", "https://docs.aws.amazon.com/vpc/latest/userguide/metrics-dimensions-nat-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/creating-alarms-nat-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT gateway port exhaustion and metrics

**Symptom:** intermittent connection timeouts to one external API under load while
everything else works.

## 1. Limits behind it
- Each NAT IP supports up to **55,000 simultaneous connections to each unique destination**
  (destination IP + port + protocol). Many workers hitting one API endpoint IP exhaust it.
- Bandwidth starts at 5 Gbps and scales automatically to 100 Gbps; packet rate starts at 1 million pps and
  scales to 10 million pps, beyond which the gateway drops packets.
- Idle TCP timeout 350 s: the NAT drops idle flows; clients keeping pooled connections longer
  see resets.

## 2. Metrics (namespace `AWS/NATGateway`, dimension `NatGatewayId`; Regional NAT gateways also use `AvailabilityZone`)
| Metric | Meaning |
|---|---|
| `ErrorPortAllocation` | **> 0 = port exhaustion** to some destination |
| `ConnectionAttemptCount` / `ConnectionEstablishedCount` | gap = failed attempts |
| `ActiveConnectionCount` | concurrent flows |
| `PacketsDropCount` | drops; if PacketsDropCount / (PacketsInFromSource + PacketsInFromDestination) x 100 exceeds 0.01 percent the docs point to a possible VPC service issue |
| `IdleTimeoutCount` | flows killed by 350 s idle timeout |
| `BytesOutToDestination`, `BytesInFromSource` etc. | volume; an out value below the matching in value can mean data loss or blocked traffic |
```bash
aws cloudwatch put-metric-alarm --alarm-name nat-a-port-exhaustion --namespace AWS/NATGateway \
  --metric-name ErrorPortAllocation --dimensions Name=NatGatewayId,Value=nat-0abc \
  --statistic Sum --period 60 --evaluation-periods 1 --threshold 0 --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:<REGION>:<ACCOUNT_ID>:netops --treat-missing-data notBreaching
```

## 3. Fixes, in order
1. **Add secondary IPs** to the NAT gateway (up to 8 IPv4 addresses: 1 primary and 7 secondary; a public NAT
   gateway is limited to 2 Elastic IP addresses by default, adjustable):
   `aws ec2 assign-private-nat-gateway-address` (private) /
   `aws ec2 associate-nat-gateway-address --allocation-ids eipalloc-...` (public).
   Each IP adds 55k connections per destination.
2. **Reuse connections**: HTTP keep-alive / connection pooling in clients; fewer, longer
   flows instead of one connection per request.
3. **Keepalive below 350 s** (`net.ipv4.tcp_keepalive_time=300` or app-level) for long-lived
   idle connections that otherwise get silently dropped.
4. **Take AWS traffic off the NAT**: gateway endpoints for S3/DynamoDB, interface endpoints
   for heavy services (ECR, CloudWatch Logs, STS).
5. Spread load across NAT gateways (per-AZ design).

## Gotchas
- `ErrorPortAllocation` only says the gateway could not allocate a source port; it does not name the destination.
  Flow logs on the NAT gateway's network interface can help find the busiest destination.
- Adding EIPs changes the set of source IPs — update partner allow-lists first.

## Verify
- [ ] Alarm exists per NAT gateway on `ErrorPortAllocation` and `PacketsDropCount`.
- [ ] After adding IPs/pooling, a load test at peak shows `ErrorPortAllocation` = 0 and attempts ≈ established.
- [ ] S3/ECR traffic no longer appears in `BytesOutToDestination` after endpoints added.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "NAT gateway basics", "NAT gateway metrics and dimensions", "Create CloudWatch alarms for NAT gateway" and "Troubleshoot NAT gateways"; botocore EC2 model (AssociateNatGatewayAddress AllocationIds, AssignPrivateNatGatewayAddress).
Confirmed: 55,000 simultaneous connections per IPv4 address per unique destination; up to 8 addresses; 5 to 100 Gbps; 1 to 10 million pps; 350-second idle timeout and keepalive below 350 s; metric names and meanings for ErrorPortAllocation, ConnectionAttemptCount, ConnectionEstablishedCount, ActiveConnectionCount, PacketsDropCount, IdleTimeoutCount; NatGatewayId dimension.
Corrected: the 8-address limit is 1 primary plus 7 secondary with a default of 2 Elastic IPs for public gateways; the 0.01 percent drop threshold is a formula against total packets and indicates a possible service issue.
Removed: the claim that the pkt-dstaddr flow-log field is the way to find the hot destination.

Method: documentation only; no commands were run.
