---
id: computing-software.it-support-helpdesk.servicenow.experience-level-agreements-and-dex-scores
name: experience-level-agreements-and-dex-scores
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, metrics, kpi, xla, experience-level-agreement, digital-employee-experience, dex-score, endpoint-analytics]
level: practitioner
status: draft
description: "Move from SLAs to experience level agreements: sentiment plus telemetry (Intune Endpoint Analytics, DEX tools) to define XLA targets, report them, and act on poor experience."
sources:
  - "https://learn.microsoft.com/en-us/mem/analytics/overview"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# experience-level-agreements-and-dex-scores
Goal: measure how IT feels to employees (not only whether tickets met
SLA) and set targets on that experience.

## Why XLAs
Watermelon effect: SLAs green, users unhappy (fast ticket closure, but the
laptop still takes 8 minutes to log in). XLAs combine:
- **Sentiment**: short pulse surveys, CSAT, comments.
- **Operational telemetry**: boot/logon time, app crashes, Wi-Fi drops,
  Teams call quality, device health.
- **Outcome**: productive time lost.

## Telemetry sources
- **Intune Endpoint Analytics**: startup performance score, application
  reliability score, work from anywhere score, battery health; baselines
  against your org and the "all organisations" median.
- DEX platforms (ServiceNow DEX, Nexthink, 1E, ControlUp) for per-device
  and per-app experience scores.
- Teams Call Quality Dashboard for meeting experience.

## Defining an XLA
- Pick 3-5 experience indicators users care about, e.g.:
  - Median logon to usable desktop < 60 s on standard laptops.
  - < 1 app crash per user per week for core apps.
  - Quarterly pulse "IT helps me do my job" ≥ 4.0/5.
- Set baseline first (one quarter of data), then targets.
- Agree with the business, not just IT.

## Acting on it
- Devices below threshold → proactive remediation (Intune remediation
  scripts, hardware refresh queue) before users call.
- Worst apps by crash rate → vendor/packaging fixes.
- Report XLA alongside SLA in service reviews.

## Gotchas
- Telemetry without sentiment misses process pain (approval delays).
- Sentiment without telemetry is hard to act on; combine both.
- Privacy: tell staff what is collected; aggregate in reports; involve
  works council/HR where required.

## Verify
An XLA scorecard exists with baselines, at least one telemetry and one
sentiment measure, and a proactive action list driven by it.
