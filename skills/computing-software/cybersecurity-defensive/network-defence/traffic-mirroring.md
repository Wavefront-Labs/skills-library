---
id: computing-software.cybersecurity-defensive.network-defence.traffic-mirroring
name: traffic-mirroring
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [traffic-mirroring, vpc-traffic-mirroring, azure-vnet-tap, gcp-packet-mirroring, cloud-nsm, network-security-monitoring]
level: practitioner
status: docs-checked
description: "Mirror cloud network traffic to IDS/NSM sensors: AWS VPC Traffic Mirroring, GCP Packet Mirroring, Azure virtual network TAP, filters, cost and gaps."
sources: ["https://docs.aws.amazon.com/vpc/latest/mirroring/what-is-traffic-mirroring.html", "https://cloud.google.com/vpc/docs/packet-mirroring", "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-tap-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud traffic mirroring

## AWS VPC Traffic Mirroring
- Copies traffic from an elastic network interface of type interface, to out-of-band security and monitoring
  appliances. Only certain instance families work as a source (the docs list them; bare metal sources must be
  Nitro v2), so check the supported instance types page before designing.
- Four concepts: source (the network interface), filter (rules defining what is mirrored), target (the
  destination), and session (ties one source, filter and target together).
- Appliances can be individual instances or a fleet behind a Network Load Balancer or Gateway Load Balancer
  with a UDP listener. Filters and packet truncation let you mirror only the traffic of interest.
- Create and manage resources via console, CLI, SDKs or the Query API; look up the CLI and encapsulation
  details in the Traffic Mirroring user guide, as the overview page does not state them. Sensors must be able
  to handle the encapsulated mirror traffic.

## GCP Packet Mirroring
A packet mirroring policy names the mirrored sources and a collector destination.
- Sources are Compute Engine VMs selected by subnets, network tags or instance names (a subnet mirrors all
  existing and future instances in it).
- The collector is an instance group behind an internal passthrough Network Load Balancer; you give the name
  of its forwarding rule, which must be configured for Packet Mirroring.
- By default all IPv4 traffic of mirrored instances is collected. Filters can add IPv6 and narrow by protocol,
  CIDR range (IPv4, IPv6 or both) and direction (ingress, egress, both). To mirror all IPv4 and IPv6 use the
  filter `0.0.0.0/0,::/0`.
- The collector must be in the same region as the sources (same VPC network or a peered one). One policy
  references a single collector destination.
- Mirroring consumes bandwidth on the mirrored instance, and if two mirrored VMs talk to each other you
  collect two copies of the packet unless you restrict to ingress or egress only. VPC Flow Logs does not log
  mirrored packets.

## Azure
Virtual network TAP streams VM network traffic to a collector provided by a partner network virtual
appliance (partner list on the overview page). It was in public preview in select regions when checked. The
destination is a virtual network IP in the same or a peered virtual network; the collector can sit behind an
Azure Internal Load Balancer. Documented limitations include: VM network interfaces only as sources, mirrored
traffic goes only to a load balancer or a VM network interface, no IPv6, and no virtual networks with
encryption enabled. If it does not fit, use sensor-in-path designs (a network virtual appliance in a hub
inspecting routed traffic) or host agents.

## Design
- Mirror at chokepoints (NAT/egress instances, hub inspection network, key servers), not every interface.
- Automate session creation for autoscaling groups.
- Combine with flow logs (metadata for all traffic); mirroring gives payload for selected traffic.

## Gotchas
- Cost: AWS charges hourly for each active mirror session even after the source is stopped or detached, plus
  data transfer, and load balancer data processing when targets sit behind one; see the vendor pricing pages.
- TLS everywhere means mostly metadata (SNI, certificates) unless you decrypt.

## Verify
- [ ] Sensor sees expected flows (for example Zeek conn.log entries for a test connection).
- [ ] Autoscaled instances get sessions automatically.

## Checked
Checked 2026-11-09. Read in full or by section: AWS "What is Traffic Mirroring?" (concepts, targets,
supported instance note, pricing), GCP Packet Mirroring overview (sources, collector, filtering, constraints,
bandwidth, flow logs), Azure virtual network TAP overview (preview status, limitations, partner solutions).
Removed as unconfirmed: the CLI example and its flags, VXLAN on UDP 4789 and the Suricata and Zeek decap
settings, the claim that mirrored traffic is dropped first under congestion, and the "Nitro instance"
requirement (the page lists many families and only restricts bare metal to Nitro v2).
Method: docs-checked 2026-11-09 against the AWS, GCP and Azure pages named above.
