---
id: computing-software.cloud-infrastructure-engineering.aws.security-group-connection-tracking-and-conntrack-limits
name: security-group-connection-tracking-and-conntrack-limits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, connection-tracking, conntrack-allowance, untracked-connections, ena-express-metrics, idle-timeout-tcp]
level: advanced
status: docs-checked
description: "Understand security group connection tracking: tracked vs untracked flows, idle timeouts, conntrack_allowance_exceeded drops on busy instances, and how to fix them."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-network-performance-ena.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-network-performance.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security group connection tracking

## 1. Why it matters
Security groups are stateful because each ENI keeps a connection-tracking table: return
traffic is allowed because the flow is tracked. The table has a per-instance-size limit.
High-connection-rate workloads (NAT instances, proxies, DNS servers, load generators,
UDP-heavy apps) can exhaust it, and packets are dropped silently with no error to the app.

## 2. Tracked vs untracked
A TCP or UDP flow is **untracked** (no table entry) when one rule permits it for all addresses
(`0.0.0.0/0` or `::/0`) and a rule in the other direction permits all response traffic
(`0.0.0.0/0` or `::/0`) for any port (0-65535). ICMP is always tracked. A narrower rule makes the flow tracked.
For protocols other than TCP, UDP and ICMP only the IP address and protocol number are tracked.

**Automatically tracked** regardless of rules: connections made through egress-only internet gateways,
Global Accelerator, NAT gateways, Network Firewall endpoints, Network Load Balancers, PrivateLink
(interface VPC endpoints), Lambda Hyperplane ENIs and DynamoDB gateway endpoints (each DynamoDB
connection uses 2 conntrack entries).

The response to an untracked flow is allowed by the rule that permits it, not by tracking information, and an
untracked flow is cut immediately when that rule is removed or modified.

## 3. Idle timeouts
Default idle timeouts: TCP established **432,000 s (5 days)** for most instance types, but 350 s on Nitro v6
instance types (excluding P6e-GB200); UDP 30 s; UDP stream (more than one request-response) 180 s. Test
long-lived connections (database pools, persistent HTTP, streaming) on Nitro v6 types, set an appropriate
`TcpEstablishedTimeout` at launch and use TCP keepalives under 5 minutes. Connections through a Network Load
Balancer use their own idle timeouts (350 s TCP, 120 s UDP). Long timeouts fill the table on servers that
see many clients that disappear without FIN. Tune per ENI (Nitro-based instances only):
```bash
aws ec2 modify-network-interface-attribute --network-interface-id eni-0abc \
  --connection-tracking-specification TcpEstablishedTimeout=3600,UdpStreamTimeout=60,UdpTimeout=30
```
(valid ranges: TCP 60-432000 s, UDP 30-60 s, UDP stream 60-180 s.) Also settable when you create a network
interface, launch an instance, or create a launch template (`ConnectionTrackingSpecification`). For asymmetric
routing AWS recommends a TCP established timeout of 60 seconds; for UDP-heavy services (DNS, SIP, SNMP,
Syslog, Radius) a UDP stream timeout of 60 s.

## 4. Detecting exhaustion
The ENA driver (version 2.2.10 or later) exposes allowance counters:
```bash
ethtool -S eth0 | grep -E 'allowance_exceeded|conntrack'
#   bw_in_allowance_exceeded, bw_out_allowance_exceeded, pps_allowance_exceeded,
#   conntrack_allowance_exceeded, linklocal_allowance_exceeded
#   conntrack_allowance_available  (remaining entries, newer drivers)
```
Any increase in `conntrack_allowance_exceeded` means packets were dropped for this
reason. Push these to CloudWatch with the CloudWatch agent `ethtool` plugin (CloudWatch names carry an
`ethtool_` prefix, for example `ethtool_conntrack_allowance_exceeded`):
```json
"metrics": {"metrics_collected": {"ethtool": {"interface_include": ["eth0"],
  "metrics_include": ["conntrack_allowance_exceeded", "conntrack_allowance_available",
                      "pps_allowance_exceeded", "linklocal_allowance_exceeded"]}}}
```
`linklocal_allowance_exceeded` counts packets dropped because traffic to local proxy services exceeded the
per-interface packets-per-second maximum: it affects the Amazon DNS service, the Instance Metadata Service
and the Amazon Time Sync Service, not custom DNS resolvers. The VPC quotas page lists 1024 packets per
second per network interface to the Route 53 Resolver (cannot be increased); cache DNS locally on DNS-heavy hosts.

## 5. Fixes, in order
1. Make the high-volume flow untracked: e.g. a public DNS/UDP service with inbound
   `0.0.0.0/0` on 53 and outbound all `0.0.0.0/0`. Accept the security trade-off
   consciously (the SG is wide; rely on NACLs/host firewall).
2. Shorten idle timeouts (section 3), especially TCP established for client-heavy servers.
3. Scale instance size or count: with load balancing, AWS recommends scaling the number or the size of
   registered instances when the per-instance tracked-connection maximum is exceeded.
4. Reduce connection churn: keep-alive/pooling in clients.

## Gotchas
- Removing or narrowing the rule behind an **untracked** flow drops it immediately; a **tracked**
  connection is not interrupted when its rule changes.
- Security groups have no effect on DNS traffic to or from the Route 53 Resolver (VPC+2 address); use
  Route 53 Resolver DNS Firewall to filter it.
- Removing an SG rule does not cut existing tracked connections; they continue until idle
  timeout. To kill them, use NACLs (stateless, immediate).
- Host OS `nf_conntrack` limits (iptables) are separate from the EC2 allowance; check the kernel log for
  conntrack table-full messages.

## Verify
- [ ] `ethtool -S` counters for conntrack and linklocal stay flat under peak load.
- [ ] CloudWatch alarm on `conntrack_allowance_exceeded` increase exists for proxy/NAT/DNS fleets.
- [ ] Connection tracking timeouts on busy ENIs set deliberately and recorded in the launch template.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide "Amazon EC2 security group connection tracking" and "Monitor network performance for ENA settings on your EC2 instance"; CloudWatch agent ethtool plugin page; VPC quotas page; botocore EC2 model (ConnectionTrackingSpecificationRequest members, ModifyNetworkInterfaceAttribute).
Corrected: the automatically tracked list (Gateway Load Balancer, Transit Gateway and ENA Express are not in the documented list; egress-only internet gateways and DynamoDB gateway endpoints are); default TCP timeout is 350 s on Nitro v6 types; an untracked flow is cut immediately when its rule changes (the reverse was stated).
Confirmed: timeout minimum, maximum and UDP defaults; ENA driver 2.2.10; metric names; CloudWatch agent ethtool section; NACLs break existing connections immediately.
Removed: the claim that larger instance sizes have larger allowances in general and the dmesg message text.

Method: documentation only; no commands were run.
