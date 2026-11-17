---
id: computing-software.systems-network-administration.network-design.network-dr-site-rpo-rto
name: network-dr-site-rpo-rto
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, high-availability, disaster-recovery-site, rpo, rto, dr-network-failover]
level: practitioner
status: gated
description: "Design the network side of disaster recovery: RPO/RTO targets, hot/warm/cold sites, replication bandwidth, IP strategy (same vs new subnets), DNS and testing failover."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html
  - https://www.iso.org/standard/75106.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network DR sites and RPO/RTO

## Terms
- **RPO** (recovery point objective): max data loss in time -> drives replication method and bandwidth.
- **RTO** (recovery time objective): max time to restore service -> drives site type and automation.
- Site types: **hot**, **warm** and **cold** sites (NIST SP 800-34 uses these terms; their exact
  definitions are unconfirmed here) (gated: unconfirmed, source is paywalled or blocked). The AWS DR page lists backup and
  restore, pilot light, warm standby and multi-site active/active as cloud equivalents.

## Replication bandwidth
Bandwidth >= daily changed data / replication window, plus headroom. 500 GB/day changed replicated
continuously over 24 h ~ 46 Mbps average; size for peaks and initial seeding (ship disks or
seed before cutover). Async replication RPO grows when the link saturates.

## IP strategy
| Strategy | How | Trade-off |
|---|---|---|
| Same subnets at DR | stretch L2 (risky) or advertise the subnets from DR via routing on failover | no re-IP; must withdraw from primary to avoid split brain |
| New subnets at DR | apps re-IP on failover, DNS updated | simpler routing, requires app readiness, low DNS TTLs |
| Global load balancing / anycast | GSLB health-based DNS or BGP anycast | automatic, more components |

## Network checklist for DR
- WAN/VPN to DR from all sites and partners (and their firewall rules referencing DR IPs).
- Internet: DR public IPs or BGP announcement of the same prefix; certificates for DR names.
- DNS: authoritative servers reachable if the primary site is gone; TTLs set to meet RTO.
- AD/DHCP/NTP available at DR.
- Firewall policy replicated (config sync or same templates).
- Out-of-band access to DR gear.

## Test
Annual (at least) failover test with documented timings vs RTO; tabletop for scenarios. Record
gaps and fix.

## Verify
- [ ] Last test achieved measured RTO/RPO within targets for tier-1 services; results filed.

## Checked

- Date: 2026-10-28
- Confirmed: the AWS DR options page lists backup and restore, pilot light, warm standby and multi-site active/active; the 500 GB/day over 24 h example is arithmetic (about 46 Mbps).
- Removed: hot/warm/cold hour and day durations. Gated: NIST SP 800-34 content was behind a frame-redirect page and the ISO standard returned 403, so the site-type definitions stay unconfirmed.

Method: documentation only; no commands were run.
