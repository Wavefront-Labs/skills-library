---
id: computing-software.devops-ci-cd.deployment-strategies.aws-vpc-traffic-mirroring
name: aws-vpc-traffic-mirroring
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, vpc-traffic-mirroring, traffic-mirroring, packet-capture, eni-mirroring, vxlan, network-monitoring]
level: practitioner
status: draft
description: "Copy packet-level traffic from EC2 ENIs with AWS VPC Traffic Mirroring: sessions, targets and filters, VXLAN decapsulation, supported instance types, costs and pre-release use."
sources:
  - https://docs.aws.amazon.com/vpc/latest/mirroring/what-is-traffic-mirroring.html
  - https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-considerations.html
  - https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-packet-format.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AWS VPC Traffic Mirroring

Packet-level (L3/L4) copies of traffic from an elastic network interface (ENI), delivered over VXLAN to a target. Unlike Envoy mirroring it doesn't replay HTTP requests to a new service version; it feeds IDS, packet capture, protocol analysis, or a replay tool that rebuilds sessions.

## Components
- **Source**: an ENI on a Nitro-based instance (most current types; some small burstable types are not supported).
- **Target**: another ENI, a Network Load Balancer (UDP 4789 listener), or a Gateway Load Balancer endpoint, for scale-out appliances.
- **Filter**: inbound/outbound rules (protocol, CIDR, ports, accept/reject) - mirror only what you need.
- **Session**: source + target + filter + session number (priority) + optional packet truncation length + VNI.

## Set up
```bash
aws ec2 create-traffic-mirror-target --network-load-balancer-arn arn:aws:elasticloadbalancing:...:loadbalancer/net/mirror-nlb/...
aws ec2 create-traffic-mirror-filter --description "http only"
aws ec2 create-traffic-mirror-filter-rule --traffic-mirror-filter-id tmf-123 --traffic-direction ingress \
  --rule-number 100 --rule-action accept --protocol 6 --destination-port-range FromPort=443,ToPort=443 \
  --source-cidr-block 0.0.0.0/0 --destination-cidr-block 10.0.0.0/16
aws ec2 create-traffic-mirror-session --network-interface-id eni-src --traffic-mirror-target-id tmt-123 \
  --traffic-mirror-filter-id tmf-123 --session-number 1 --packet-length 256   # truncate to headers to save bandwidth
```
Terraform: `aws_ec2_traffic_mirror_target/filter/filter_rule/session`.

## Receiving
Packets arrive VXLAN-encapsulated (UDP 4789); target security group must allow it from sources. Decapsulate:
- Suricata/Zeek handle VXLAN natively (Suricata `decoder.vxlan.enabled: yes`).
- Packet capture: `tcpdump -i eth0 udp port 4789 -w mirror.pcap`, then Wireshark decodes VXLAN.
- Linux: create a `vxlan` interface with the VNI to see inner frames.

## Considerations
- Mirrored traffic counts toward the source instance's network bandwidth; under load, mirrored packets are dropped first (production traffic wins).
- Sessions per ENI and per account are limited; ENIs get replaced in autoscaling - automate session creation on instance launch (EventBridge + Lambda).
- Encrypted traffic (TLS) is mirrored encrypted; useful for flow/metadata analysis, not payload, unless the target can decrypt.
- Pricing: per ENI-hour with an active session plus data transfer if cross-AZ.
- Fargate, Lambda and managed services don't expose ENIs for mirroring; use service-level logs instead.

## Pre-release testing use
Capture real traffic patterns with mirroring, then replay HTTP sessions (GoReplay from pcap) against a staging stack - never against production dependencies.

## Verify
- [ ] Target receives VXLAN packets from the session; IDS/pcap shows inner traffic matching the filter.
- [ ] Source instance network metrics show no impact on production throughput.
