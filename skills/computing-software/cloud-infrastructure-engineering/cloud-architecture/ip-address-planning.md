---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ip-address-planning
name: ip-address-planning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, ip-address-planning, cidr-planning, ipam, rfc1918, non-overlapping-cidrs, subnet-sizing, kubernetes-pod-ips, ipv6, vpc-ipam]
level: practitioner
status: docs-checked
description: "Plan cloud IP space early: non-overlapping allocations across on-prem and clouds, RFC 1918 ranges, subnet sizing, reserved addresses and IPAM tooling."
sources: ["https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing", "https://cloud.google.com/vpc/docs/subnets", "https://www.rfc-editor.org/rfc/rfc1918"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP address planning for cloud

Overlapping CIDRs block peering and hybrid connectivity and are fixed only by re-addressing workloads, so allocate
non-overlapping space before building.

## Steps
1. **Collect used ranges**: on-prem, branch, partners, other clouds, VPNs.
2. **Choose from the private ranges** RFC 1918 reserves: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Allocate a
   cloud supernet and carve it hierarchically (cloud, region, environment, network, subnet).
3. **Size subnets** for growth and for services that consume addresses on your behalf. Azure reserves five IP
   addresses in each subnet, and some services such as AKS with CNI networking have their own address needs, so
   include them when sizing.
4. **IPAM**: use an IPAM tool for central visibility and to prevent overlaps; Azure's guidance wants an API for
   reserving non-overlapping space so allocation can be automated in IaC and subscription vending. AWS VPC IPAM is
   the AWS equivalent (see its page).

## Gotchas
- Subnet ranges on Google Cloud cannot overlap private or other reserved ranges, and cannot span an RFC range and a
  privately used public range (VPC subnets page).

## Verify
- [ ] Every VPC/VNet CIDR is allocated from the IPAM; overlap check returns none.

## Checked
2026-11-01. Confirmed: RFC 1918 ranges (RFC 1918), Azure five reserved addresses per subnet, AKS CNI note and IPAM
guidance (Cloud Adoption Framework IP planning page), Google Cloud subnet range restrictions (VPC subnets page).
The AWS IPAM page is thin; only its existence is referenced. Removed: example supernet and prefix lengths, AWS/GCP
reserved-address counts, pod IP and secondary CIDR advice, IPv6 /56 sizing, Docker default range, utilisation
threshold.
Method: documentation only; no commands were run.
