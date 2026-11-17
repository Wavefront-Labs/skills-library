---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.network-flow-analysis
name: network-flow-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, network-flow-analysis, dependency-discovery, netflow, vpc-flow-logs, move-groups, connection-analysis]
level: practitioner
status: draft
description: "Derive application dependencies from network flows (agent-based discovery, NetFlow/IPFIX, firewall logs) to build move groups and firewall rules before migration."
sources: ["https://learn.microsoft.com/azure/migrate/concepts-dependency-visualization", "https://docs.aws.amazon.com/application-discovery/latest/userguide/what-is-appdiscovery.html", "https://datatracker.ietf.org/doc/html/rfc7011"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network dependency analysis from traffic flows

## Data sources
- **Agent-based discovery** (Azure Migrate dependency agent, AWS Application Discovery agents):
  process-level connections (process, port, remote host).
- **Agentless** dependency analysis (Azure Migrate for VMware) - connection data without agents.
- **NetFlow/IPFIX/sFlow** from switches/routers; **firewall logs**; packet brokers.
- **APM** traces for application-level calls.

## Steps
1. Collect for at least 2-4 weeks to cover month-end and batch cycles (30 days preferred).
2. Normalise endpoints to servers/apps using the CMDB/IP plan.
3. Filter noise: monitoring, backup, AV, DNS, NTP, domain controllers (shared services - plan
   separately).
4. Build a graph; find connected components = candidate **move groups**.
5. Annotate each edge: protocol/port, volume, latency sensitivity.
6. Decide: move together, keep apart with hybrid connectivity (check latency budget), or decouple.
7. Export required flows as firewall/security group rules for the target.

## Gotchas
- Too short a window misses quarterly jobs.
- NAT and load balancer VIPs hide real endpoints; correlate with LB configs.
- Everything connects to AD; treat identity as a platform dependency, not an app link.

## Verify
- [ ] Move groups reviewed with app owners.
- [ ] Target security rules derived from observed flows, not "allow any".
