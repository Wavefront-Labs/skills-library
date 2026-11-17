---
id: computing-software.systems-network-administration.backup-and-recovery.alternate-site-selection-and-geographic-separation
name: alternate-site-selection-and-geographic-separation
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [geographic-separation, site-selection, alternate-sites, disaster-recovery, nist-800-34, risk-assessment]
level: practitioner
status: docs-checked
description: "Select an alternate processing or storage site: hazard separation from primary, accessibility, telecom paths, readiness type and contract terms."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alternate site selection and geographic separation

**Goal:** an alternate site that will not be hit by the same event as the primary and can still meet RTO/RPO.

## What NIST SP 800-34 Rev. 1 says
- A fixed alternate site should be in a geographic area unlikely to be affected by the same hazard as the primary site, and selection should account for the time and mode of transport needed to move people or equipment there (section 3.4.3).
- Offsite storage criteria (section 3.4.2): geographic area (distance and the probability of being hit by the same disaster), accessibility (retrieval time and opening hours), security, environment (temperature, humidity, fire prevention, power management) and cost.
- Appendix E (the SP 800-53 Rev. 3 contingency controls it reproduces): CP-6(1) and CP-7(1) ask for an alternate site separated from the primary so as not to be susceptible to the same hazards; hazards are typically defined in the risk assessment. CP-6(3) and CP-7(2) ask you to identify accessibility problems in an area-wide disruption and outline explicit mitigation actions. The storage example is duplicating backups at a second alternate storage site, or planning physical access if electronic access is disrupted.
- CP-7(3) asks for priority-of-service provisions in alternate processing site agreements; CP-7(5) equivalent security measures at the alternate site; CP-8(3) alternate telecom providers separated from primary providers.
- Redundant communications links should have physical separation and not follow the same path, or one cable cut can disrupt both (chapter 5).

## Site types (section 3.4.3)
| Type | Description in the guide | Sample criteria (Table 3-4) |
|---|---|---|
| Cold | space and infrastructure only | low cost, no hardware, long setup |
| Warm | partially equipped, some or all hardware and software | medium cost, medium setup |
| Hot | sized and configured with hardware, infrastructure and support personnel | medium/high cost, full hardware, short setup |
Mobile and mirrored sites are listed as variations. The guide says to analyse sites against the BIA impacts and downtime, and to confirm the site's security, management, operational and technical controls are compatible.

## Contract points (commercial site)
The guide says to negotiate and state testing time, work space, security, hardware, telecom, support services and recovery days (how long you may occupy the space). Several customers may share one site, so the vendor's policy on priority when many are affected at once must be negotiated.

## Replication versus distance (practice, not from NIST)
Synchronous replication makes every write wait on the remote site, so it constrains distance by latency; asynchronous replication tolerates distance at the cost of an RPO equal to the lag. Measure round-trip time and bandwidth between candidate sites before choosing a design. Where you need both zero loss and regional separation, a two-tier design (synchronous nearby, asynchronous far) is a common answer.

## Gotchas (practice)
- Two data centres on different streets served by the same substation, carrier central office or fibre duct.
- A site so far away nobody can staff it; plan remote hands or remote administration.

## Verify
A site risk assessment comparing primary and alternate hazards side by side and signed off, and a measured latency and bandwidth test supporting the replication design.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (PDF behind the csrc.nist.gov page): sections 3.4.2 and 3.4.3, chapter 5 telecom text and Appendix E CP-6, CP-7 and CP-8. Targeted reads, not the whole 149 pages. Removed: the SP 800-53 and FEMA sources (not read), the "50-150 km" rule of thumb, "under 100 km / 5 ms RTT", the "tier rating" and "NAID"-style specifics, the "two carriers" count, and the claim that the guide specifies a distance. The replication section is labelled practice.

Method: documentation only; no commands were run.
