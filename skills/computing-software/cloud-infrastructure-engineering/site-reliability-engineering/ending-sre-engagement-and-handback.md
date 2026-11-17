---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.ending-sre-engagement-and-handback
name: ending-sre-engagement-and-handback
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [service-handback, ending-sre-engagement, give-back-the-pager, sre-engagement, operational-overload]
level: advanced
status: docs-checked
description: "When and how SRE ends an engagement or hands a service back, per the SRE Workbook: value-based triggers, workload self-regulation, and two case studies (Ares, data pipeline)."
sources: ["https://sre.google/workbook/engagement-model/", "https://sre.google/workbook/team-lifecycles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ending the engagement and handback

## Engagements are not perpetual
The Workbook chapter "SRE Engagement Model" (section "Ending the Relationship") says SRE engagements are not necessarily indefinite. SREs provide value through impactful engineering work. If that work is no longer impactful (the value proposition goes away), or most of the work is no longer on the engineering side versus operations, revisit the engagement. Individual SREs tend to move away from toil-heavy teams.

At team level the Workbook gives these examples for handing a service back because SRE no longer provides enough business value to merit its cost:
- the service has been optimised to the point that ongoing SRE engagement is no longer necessary;
- the service's importance or relevance has diminished;
- the service is reaching end of life.

## Self-regulating workload (SRE Team Lifecycles)
Principle #3 in the "Performing" stage: an SRE team regulates its own workload. For a team with a distinct product development partner, the chapter says:
- the SRE team chooses if and when to onboard a service;
- in operational overload it can reduce toil by lowering the SLO or transferring operational work to another team such as product development;
- if it becomes impossible to operate a service at SLO within agreed toil constraints, the SRE team can hand back the service;
- if the team has solved all the problems at scale for a service, either find other reliability challenges for it or intentionally decide to hand the service back, otherwise attrition risks production.
Teams with no partner to hand back to (for example those packaging third-party software) are told to stop feature work in favour of reliability work when the SLO is missed, or to reduce SLOs unless management adds capacity.

## Case studies in the chapter
- **Ares (positive ending):** Abuse SRE and the Common Abuse Tool (CAT) team ran a multiyear project to create a dedicated infrastructure team inside CAT, with an exchange programme to transfer production management knowledge. At the end Abuse SRE disengaged from directly supporting CAT and focused on the underlying infrastructure, without compromising CAT reliability or overburdening CAT with operations work.
- **Data analysis pipeline (nuanced ending):** the cost of maintaining the SRE relationship exceeded the value, and the SRE team was disbanded. The chapter says it is extremely difficult to identify when to end such a relationship, describes a three-year lead-up in which work shifted to a replacement system and a gap in communication broke down the relationship between the teams, and stresses regular, open, cooperative communication throughout.

## Related lifecycle phases (same chapter)
- Deprecation: SRE operates the existing system mostly without developer involvement and supports the transition, effectively supporting two full systems, so headcount should be adjusted.
- Abandoned: the developer team typically resumes operational support, SRE supports incidents on a best-effort basis, and internal-user services are handed to remaining users.
- Unsupported: no users remain; SRE helps delete references to the service from production configuration and documentation.

## Checked
- 2026-11-08: all points were confirmed on the Workbook Engagement Model and Team Lifecycles pages.
- Removed: the handback agreement template, re-engagement criteria (such as SLO met for two quarters, fewer than 2 incidents per shift), shadow-shift counts, the 50% ops-load trigger, and the SRE Book operational-overload and introduction pages from sources (the operational-overload page covers embedding an SRE in an overloaded team and does not describe handback).
Method: docs-only read of cited pages, 2026-11-08
