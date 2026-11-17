---
id: computing-software.cloud-infrastructure-engineering.azure.choose-outbound-method-nat-gateway-lb-or-instance-ip
name: choose-outbound-method-nat-gateway-lb-or-instance-ip
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, outbound-method, outbound-choice, nat-gateway, outbound-rules, instance-level-public-ip, firewall-egress]
level: practitioner
status: docs-checked
description: "Choose an Azure outbound connectivity method: NAT gateway, Load Balancer outbound rules, instance public IPs or firewall egress, using Microsoft's precedence and SNAT guidance."
sources: ["https://learn.microsoft.com/azure/load-balancer/load-balancer-outbound-connections", "https://learn.microsoft.com/azure/nat-gateway/nat-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose NAT gateway vs LB outbound rules vs instance IPs

**Goal:** one deliberate egress method per subnet, with enough SNAT ports and the IP stability partners need.

## Precedence
- NAT gateway takes precedence over every other outbound method: load balancer, instance-level public IP and Azure Firewall.
- Next is an instance-level public IP on the NIC's IP configuration; the instance has all ephemeral ports, and this
  takes precedence over the remaining scenarios.
- Then a load balancer's outbound rules (or load balancing rules with outbound SNAT enabled).
- Default outbound access is last and should be avoided for production; new virtual networks created with the API
  released after 31 March 2026 use private subnets by default.

## Pick a method
| Method | SNAT behaviour | When |
|---|---|---|
| NAT gateway | Dynamic SNAT port allocation; up to 16 IPv4 public IPs (Standard) | Default choice for internet egress |
| Azure Firewall / NVA via UDR 0.0.0.0/0 | Depends on the appliance | Inspection or FQDN filtering required |
| Instance-level public IP | All ephemeral ports of the IP | A single VM that also needs inbound |
| Load balancer outbound rules | Each frontend IP offers 64,000 SNAT ports, split across backend instances | VMs already behind a Standard public LB |

## LB outbound sizing (if you must)
Each frontend IP gives 64,000 ports eligible for SNAT; each port used in a load balancing or inbound NAT rule consumes
a range of eight ports from them. Spreading the ports across many backend instances causes SNAT exhaustion: new
outbound connections to a destination fail until a port frees up. To use explicit outbound rules, disable
outbound SNAT on the load balancing rules (`disableOutboundSnat`).

## Gotchas
- NAT gateway can't be used with subnets that have Basic resources (Basic load balancer or Basic public IPs).
- Windows Activation and Windows Updates need an explicit outbound method on private subnets.

## Verify
- [ ] Each subnet has a documented outbound method.
- [ ] SNAT failure metrics stay at zero under a peak load test.

## Checked
2026-10-31. Confirmed against Learn "Source Network Address Translation for outbound connections" and "What is Azure
NAT Gateway": NAT gateway precedence incl. over Azure Firewall, instance-level IP precedence, 64,000 ports and eight-port
blocks, exhaustion behaviour, `disableOutboundSnat`, Basic restriction. Corrected: the old precedence list that ranked a
UDR/firewall above NAT gateway. Removed: 64,512 ports per IP, firewall 2,496-port figure, AKS `outboundType` guidance,
App Service pattern, the `allocatedOutboundPorts` formula, and the "mixing" claim.
Method: documentation only; no commands were run.
