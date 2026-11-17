---
id: computing-software.cloud-infrastructure-engineering.aws.nat-gateway-connectivity-troubleshooting
name: nat-gateway-connectivity-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-gateway, nat-troubleshooting, nat-idle-timeout, idletimeoutcount, egress-troubleshooting, vpc]
level: practitioner
status: docs-checked
description: "Debug private-subnet egress through a NAT gateway: route and NACL checks, the 350-second idle timeout and keepalives, port allocation errors, and NAT CloudWatch metrics."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-troubleshooting.html", "https://docs.aws.amazon.com/vpc/latest/userguide/metrics-dimensions-nat-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-working-with.html", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html", "https://docs.aws.amazon.com/vpc/latest/userguide/security-vpc-bpa.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT gateway connectivity troubleshooting

## 1. Path checklist (instance cannot reach the internet)
1. **Instance subnet route table**: `0.0.0.0/0 -> nat-...`. Check the table actually
   associated with that subnet (not the main table by assumption):
   `aws ec2 describe-route-tables --filters Name=association.subnet-id,Values=subnet-0priv`.
2. **NAT gateway** state `available`, type `public`, in a **public** subnet, with an EIP.
3. **NAT subnet route table**: `0.0.0.0/0 -> igw-...`. A NAT placed in a private subnet
   by mistake is the most common root cause.
4. **NACLs** on both subnets allow outbound 443/80 and inbound ephemeral 1024-65535 (NAT
   uses that full range).
5. **Security group** on the instance allows the outbound port.
6. **DNS**: name resolution works (`dig example.com`); failures here look like egress failures.
7. VPC Block Public Access in Bidirectional mode blocks all traffic to and from internet gateways; Ingress-only mode still allows NAT gateway and egress-only gateway traffic. An exclusion can exempt a VPC or subnet.
Reachability Analyzer from the instance ENI to the IGW (destination type Internet
Gateway) names the failing hop.

## 2. Metrics that explain intermittent failures
Namespace `AWS/NATGateway`, per `NatGatewayId`:
| Metric | Meaning | Action |
|---|---|---|
| `ErrorPortAllocation` | NAT could not allocate a source port: each IPv4 address supports up to 55,000 simultaneous connections to each **unique destination** (destination IP, port and protocol) | Associate secondary IPv4 addresses (up to 8 per zonal NAT gateway), spread across destinations, or add NAT gateways |
| `IdleTimeoutCount` | Connections moved to idle after 350 s with no activity | Enable TCP keepalive < 350 s on clients |
| `PacketsDropCount` | NAT dropped packets; above 0.01% of total traffic (PacketsDropCount / (PacketsInFromSource + PacketsInFromDestination) x 100) there may be a VPC service issue | Check the AWS Health dashboard |
| `ConnectionAttemptCount` vs `ConnectionEstablishedCount` | SYNs vs established | Gap means destination not answering or blocked |
| `ActiveConnectionCount`, `BytesOutToDestination` | load | capacity planning (5 Gbps, scaling automatically to 100 Gbps; 1 million pps scaling to 10 million) |

## 3. The 350-second idle timeout
A connection that is idle for 350 seconds or more times out. When a client behind the NAT tries to continue it, the NAT gateway returns an RST packet (it does not send a FIN). Symptoms: long-running DB/Kafka/SSH connections through NAT hang or reset
after about 6 minutes idle. Fixes (AWS suggests initiating more traffic on the connection, or enabling TCP keepalive on the instance with a value under 350 seconds):
- Linux: set the kernel TCP keepalive time below 350 seconds, and make sure the application enables keepalive on its sockets.
- Application-level pings (database driver keepalive settings, SSH `ServerAliveInterval`).
- Use VPC endpoints for AWS services so traffic avoids NAT entirely.

## 4. Other causes
- Destination allowlists your **NAT EIP**; after recreating the NAT, the IP changed.
  Keep EIPs as named resources and re-associate.
- Cross-AZ: if resources in several AZs share one NAT gateway and its AZ goes down, they lose internet access, and cross-AZ traffic adds data transfer charges. AWS recommends one NAT gateway per AZ, each private table pointing at its own AZ's NAT.
- MTU: a NAT gateway supports an MTU of 8500; packets larger than 8500 bytes are dropped (or fragmented). For internet traffic through a public NAT gateway the instance MTU should not exceed 1500. Path MTU discovery needs ICMP "fragmentation needed" allowed
  back in (NACL ICMP type 3 code 4).
- Private NAT gateway (no internet) used by mistake for internet egress.

## Verify
- [ ] `curl -sS -m 5 https://checkip.amazonaws.com` from the instance returns the NAT EIP.
- [ ] `ErrorPortAllocation` and `PacketsDropCount` alarms exist and are zero at peak.
- [ ] Long-lived connections survive 10 minutes idle after keepalive tuning (the NAT timeout is 350 seconds).
- [ ] Each AZ's private route table targets the NAT in the same AZ.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (NAT gateway basics, working with NAT gateways, troubleshooting, NAT gateway metrics and dimensions, VPC Block Public Access, compare NAT devices) and the botocore EC2 model.
- 350-second idle timeout, the RST behaviour and the keepalive remedy confirmed on the troubleshooting and comparison pages.
- Metric names and meanings (`ErrorPortAllocation`, `IdleTimeoutCount`, `PacketsDropCount` with the 0.01 percent formula, connection counters) confirmed on the metrics page. 55,000 connections per IP per unique destination, up to 8 addresses, 5 Gbps scaling to 100 Gbps and 1 to 10 million packets per second confirmed on the basics page.
- MTU 8500 and the 1500 MTU advice confirmed; Block Public Access modes confirmed (the API enum names were not needed).
- Removed the exact `sysctl` values (not on a page read) and the claim that the NAT silently fails when the server sends first.

Method: documentation only; no commands were run.
