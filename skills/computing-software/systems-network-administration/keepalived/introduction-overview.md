---
id: computing-software.systems-network-administration.keepalived.introduction-overview
name: introduction-overview
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, overview, load-balancing, high-availability, ipvs, vrrp, health-checking]
level: intro
status: docs-checked
description: "What Keepalived is for: IPVS layer-4 load balancing, real-server health checking and VRRPv2 director failover, usable separately or together."
sources:
  - https://keepalived.readthedocs.io/en/latest/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keepalived overview

Keepalived keeps load-balanced services available. It spreads IP traffic over a pool of real servers and protects both the pool and the load balancer (also called a director or LVS router).

Three framework pieces:
- **Load balancing:** uses the Linux Virtual Server (IPVS) kernel module for layer-4 balancing.
- **Health checking:** watches each real server and adjusts the pool to match its condition.
- **High availability:** VRRPv2 provides failover between load balancers. VRRP hooks into the state machine for fast, low-level protocol interaction.

Each framework can be used independently or together.

## Checked

2026-11-04: confirmed against the Introduction page. Removed daemon-option advice the page does not give, a claim about system requirements, and the Verify line.
Method: documentation only; no commands were run.
