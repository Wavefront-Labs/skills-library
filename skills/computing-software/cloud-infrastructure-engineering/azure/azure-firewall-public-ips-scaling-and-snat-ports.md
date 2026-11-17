---
id: computing-software.cloud-infrastructure-engineering.azure.azure-firewall-public-ips-scaling-and-snat-ports
name: azure-firewall-public-ips-scaling-and-snat-ports
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-firewall, firewall-public-ips, firewall-snat-ports, nat-gateway, autoscale, throughput]
level: advanced
status: docs-checked
description: "Size Azure Firewall egress: SNAT ports per public IP per instance, adding IPs vs attaching a NAT gateway, scale-out behaviour and throughput by SKU."
sources: ["https://learn.microsoft.com/azure/firewall/firewall-performance", "https://learn.microsoft.com/azure/firewall/integrate-with-nat-gateway", "https://learn.microsoft.com/azure/firewall/firewall-faq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall public IPs, scaling and SNAT ports

**Goal:** the hub firewall never becomes the bottleneck for outbound connections or throughput.

## SNAT capacity
- Each firewall public IP provides **2,496 SNAT ports per backend instance** (minimum of two instances); up to 250 public IPs can be associated, giving 1,248,000 ports.
- The firewall reuses a closed connection's source port immediately (no idle wait time).
- Azure Firewall cannot attach a public IP prefix itself, but it can use individual Standard SKU public IPs provisioned from a prefix. With several IPs, downstream filters must allow all of them (or the prefix range).
- **NAT gateway on AzureFirewallSubnet** gives 64,512 SNAT ports per public IP, up to 16 IPv4 public IPs, allocated dynamically per subnet. Microsoft calls it the better option for scale; multiple public IPs suit cost-sensitive, moderate needs.
```bash
az network public-ip create --name public-ip-1 --resource-group nat-rg --sku standard
az network nat gateway create --name firewall-nat --resource-group nat-rg --public-ip-addresses public-ip-1 --sku standard
az network vnet subnet update --name AzureFirewallSubnet --vnet-name nat-vnet --resource-group nat-rg --nat-gateway firewall-nat
```
- No extra UDR is needed for firewall egress through the NAT gateway, and there is no double NAT (instances send to the NAT gateway from their private IPs). Keep workload routes pointing at the firewall's private IP. The NAT gateway picks among its IPs randomly; you cannot choose.
- Zones: a Standard NAT gateway does not support zone-redundant firewalls; use a StandardV2 NAT gateway with a zone-redundant firewall. NAT gateway is not supported inside a secured virtual hub (vWAN): put it on the spoke VNets instead.
- Remedy for exhaustion per the FAQ: add public IPs (lower cost) or a NAT gateway (more scalable).

## Throughput and scale-out
- Documented maximums (autoscale cap of 20 instances): Basic 0.25 Gbps, Standard 30 Gbps, Premium 100 Gbps; Premium with TLS inspection and IDPS in Deny mode up to 22 Gbps. Prescaling raises the cap to 50 instances (figures then differ).
- Out of the box: Standard up to 3 Gbps, Premium up to 18 Gbps. Scale-out starts when average throughput and CPU reach 60% or connections reach 80%, takes five to seven minutes; scale-in when below 20%. Basic does not autoscale.
- Single TCP connection: Standard up to 1.5 Gbps, Premium up to 9 Gbps (up to 600 Mbps with IDPS), Basic up to 250 Mbps. Large single-stream transfers do not speed up with more instances.
- Per-VM limit of 250k active connections; the firewall starts with two VMs.
- When load testing, run 10 to 15 minutes and start new connections so they reach new nodes.

## Metrics
Alert on SNAT port utilisation, throughput against the SKU figure, and firewall health. Take thresholds from your own load test; the Learn pages cited do not prescribe values.

## Gotchas
- A firewall without a public IP on the data NIC needs forced tunnelling mode, which adds a management interface with its own public IP.
- Traffic to RFC 1918 and RFC 6598 destinations is not SNATed; application-rule traffic always is.

## Verify
- [ ] Egress IPs (NAT gateway IPs or firewall IPs) documented and allow-listed downstream; load test shows scale-out without drops.

## Checked
2026-10-31. Confirmed against firewall-performance, integrate-with-nat-gateway and firewall-faq Learn pages: SNAT ports per IP and 250 IP cap, NAT gateway 64,512 ports and 16 IPs, zone-redundant StandardV2 note, vWAN limitation, throughput figures, scale thresholds, 250k connections per VM. Removed: metric alert thresholds (80%, 90%, 50%), the metric table, DNAT and "random SNAT among firewall IPs" gotchas, "Standard NAT gateway is zonal", the `--idle-timeout` CLI example (swapped for the documented example).
Method: documentation only; no commands were run.
