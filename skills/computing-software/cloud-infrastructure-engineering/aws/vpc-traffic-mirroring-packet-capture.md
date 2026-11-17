---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-traffic-mirroring-packet-capture
name: vpc-traffic-mirroring-packet-capture
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, traffic-mirroring, mirror-session, packet-capture, vxlan, ids, network-troubleshooting]
level: practitioner
status: docs-checked
description: "Capture full packets from ENIs with VPC Traffic Mirroring: targets (ENI, NLB, GWLB endpoint), filters, sessions, VXLAN decapsulation and tcpdump/Wireshark analysis."
sources: ["https://docs.aws.amazon.com/vpc/latest/mirroring/what-is-traffic-mirroring.html", "https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-targets.html", "https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-filters.html", "https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-sessions.html", "https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-packet-formats.html", "https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-network-limitations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC Traffic Mirroring for packet capture

**When:** flow logs say traffic flows but you need payloads/handshakes (TLS alerts, TCP
resets, protocol errors), or you feed an IDS (Suricata/Zeek).

## 1. Build
```bash
TGT=$(aws ec2 create-traffic-mirror-target --network-interface-id eni-capturebox \
  --description capture --query TrafficMirrorTarget.TrafficMirrorTargetId --output text)
FLT=$(aws ec2 create-traffic-mirror-filter --query TrafficMirrorFilter.TrafficMirrorFilterId --output text)
aws ec2 create-traffic-mirror-filter-rule --traffic-mirror-filter-id $FLT --traffic-direction ingress \
  --rule-number 100 --rule-action accept --protocol 6 --destination-port-range FromPort=443,ToPort=443 \
  --source-cidr-block 0.0.0.0/0 --destination-cidr-block 0.0.0.0/0
aws ec2 create-traffic-mirror-filter-rule --traffic-mirror-filter-id $FLT --traffic-direction egress \
  --rule-number 100 --rule-action accept --protocol 6 --source-port-range FromPort=443,ToPort=443 \
  --source-cidr-block 0.0.0.0/0 --destination-cidr-block 0.0.0.0/0
aws ec2 create-traffic-mirror-session --network-interface-id eni-source --traffic-mirror-target-id $TGT \
  --traffic-mirror-filter-id $FLT --session-number 1 --packet-length 9001 --virtual-network-id 4242
```
- Targets: an ENI of type `interface` (single capture box), a Network Load Balancer (needs a UDP listener on port 4789, for a fleet of sensors), or
  a Gateway Load Balancer endpoint. AWS recommends an NLB or GWLB endpoint for high availability, but they can deliver mirrored packets out of order; use an ENI target if your appliance cannot cope.
- `--packet-length` truncates each mirrored packet (the packet length cannot be less than 35 bytes for IPv4 or 55 for IPv6).
- Sources are ENIs of type `interface` on supported instance families (not all instance types are supported; the sessions page lists the families). Mirroring is not supported for IPv6-only subnets.
- Filter rules are evaluated from the lowest number up and the first match decides; with no rules nothing is mirrored, and with no egress rules no outbound traffic is mirrored.
- Sessions are evaluated by ascending session number; each packet is mirrored once.

## 2. Capture and decode
Mirrored packets arrive VXLAN-encapsulated on **UDP 4789** at the target; its SG must allow
UDP 4789 from the sources, and the source subnet's route table must route the encapsulated traffic to the target.
```bash
sudo tcpdump -i eth0 -w mirror.pcap udp port 4789
```
The monitoring software on the target must be able to process VXLAN-encapsulated packets (open-source tools or AWS Marketplace solutions). The VXLAN network ID is a label you choose (or a random value if unset); AWS does not validate it, so do not treat it as a trust boundary.
The outer source IP is the source ENI's primary IP and the outer source port comes from a hash of the original flow.

## Gotchas
- Mirrored traffic counts toward the source instance's bandwidth (1 Gbps in plus 1 Gbps out means 4 Gbps of traffic handled). Mirrored packets are dropped first when limits are exceeded, so production traffic has priority — don't treat it as lossless.
- Packets are truncated to the target MTU when the target is a standalone instance; keep the source interface MTU 54 bytes (IPv4) or 74 bytes (IPv6) below the target MTU.
- Not mirrored: ARP, DHCP, the instance metadata service, NTP and Windows activation traffic. VPC Flow Logs do not capture mirrored traffic at the source. Inbound traffic dropped by the source's security group or NACL is not mirrored.
- Encrypted traffic (TLS) shows handshakes and metadata, not content.
- Delete sessions after troubleshooting.
- Filter rules must cover both directions (ingress and egress) or you only see half the conversation.

## Verify
- [ ] `tcpdump` on the target shows UDP 4789 packets while the source handles traffic.
- [ ] Decoded pcap shows full TCP handshakes for the filtered port in both directions.
- [ ] Sessions removed after use (`describe-traffic-mirror-sessions` empty for the source).

## Checked

Checked 2026-10-27 against the Amazon VPC Traffic Mirroring guide (how it works, targets, filters, sessions, packet format, limitations) and the botocore EC2 model.
- Target types and the NLB UDP 4789 listener, VXLAN on UDP 4789, security group and route requirements, filter rule evaluation and the no-egress-rules behaviour, session numbering, supported-source note, packet format fields and the limitations (bandwidth priority, MTU and truncation, unsupported traffic types, flow logs, IPv6-only subnets) confirmed.
- `create-traffic-mirror-target`, `create-traffic-mirror-filter`, `create-traffic-mirror-filter-rule` (both CIDR blocks required) and `create-traffic-mirror-session` (`--packet-length`, `--session-number`, `--virtual-network-id`) confirmed in the service model.
- Corrected the claim that sources must be Nitro-based (the supported families page includes older families) and removed the per-ENI-hour charge statement and the tshark and Suricata/Zeek details, which no page read confirms.

Method: documentation only; no commands were run.
