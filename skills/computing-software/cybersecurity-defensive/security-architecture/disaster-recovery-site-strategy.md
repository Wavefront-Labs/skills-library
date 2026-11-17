---
id: computing-software.cybersecurity-defensive.security-architecture.disaster-recovery-site-strategy
name: disaster-recovery-site-strategy
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, disaster-recovery-sites, hot-site, warm-site, cold-site, pilot-light, multi-region, geographic-dispersion, failover]
level: practitioner
status: draft
description: "Choose and design a DR site strategy (hot, warm, cold, pilot light, multi-region) that meets RTO/RPO at acceptable cost, with failover and failback."
sources: ["CompTIA Security+ SY0-701 objective 3.4 (hot/cold/warm sites, geographic dispersion)", "NIST SP 800-34 Rev. 1 Contingency Planning Guide", "AWS Whitepaper - Disaster Recovery of Workloads on AWS"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disaster recovery site strategy

**Goal:** the business can run critical services from somewhere else within the recovery time
it has agreed to, at a cost it has accepted.

## Options
| Strategy | Description | Typical RTO | Cost |
|---|---|---|---|
| Backup and restore / cold site | Space and power, or cloud account with backups only | Days | Low |
| Pilot light | Core data replicated, minimal infra running, rest provisioned on demand (IaC) | Hours | Low-medium |
| Warm standby | Scaled-down full copy running, scaled up on failover | Minutes to an hour | Medium |
| Hot site / active-active multi-region | Full capacity running in both, traffic split | Near zero | High |

Pick per service tier from the business impact analysis, not one strategy for everything.

## Design points
- **Geographic dispersion:** far enough apart to avoid shared disasters (power grid, flood
  plain, regional cloud outage), close enough for replication latency if synchronous.
- **Replication:** synchronous (zero RPO, latency limited) vs asynchronous (RPO of seconds to minutes).
- **Dependencies:** identity, DNS, certificates, secrets, third-party APIs, licences, network
  links and firewall rules must exist at the DR site.
- **IaC:** with pilot light and warm standby, infrastructure is code that has been run, not code that should work.
- **Cyber scenario:** replication also copies ransomware and deletions; DR sites need point-in-time restore and immutable backups too.

## Failover and failback
Documented runbook with decision authority (who declares disaster), DNS/traffic switch method
and TTLs, data consistency checks, and the failback plan (often harder: reverse replication,
reconciling changes made at DR).

## Gotchas
- Capacity reservations: in a regional cloud outage everyone fails over to the same region.
- DR environments drift from production unless deployed by the same pipelines.
- Staff access: VPNs, PAWs and MFA tokens must work when the primary site is down.

## Verify
- [ ] Annual failover test of each tier-1 service, with measured RTO/RPO.
- [ ] Dependency list reviewed and present at the DR site.
