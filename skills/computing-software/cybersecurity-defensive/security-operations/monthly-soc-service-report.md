---
id: computing-software.cybersecurity-defensive.security-operations.monthly-soc-service-report
name: monthly-soc-service-report
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-service-report, soc-management, soc-metrics, reporting, kpis, stakeholder-communication]
level: practitioner
status: draft
description: "Write a monthly SOC service report: volumes and SLAs, notable incidents, detection and coverage changes, risks and asks, with consistent metrics month to month."
sources: ["https://www.ncsc.gov.uk/collection/building-a-security-operations-centre", "https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1", "https://csrc.nist.gov/pubs/sp/800/55/v1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Monthly SOC service report

Audience: CISO, IT leadership, service owners (and the customer for MSSP/MDR). Two pages plus appendix.

## Sections
1. **Summary** (5 bullets): service health, notable incidents, trend, top risk, ask.
2. **Operations**: alerts received, triaged, escalated; incidents by severity and category; SLA
   attainment (acknowledge, triage, notify) with trend vs last 3 months.
3. **Notable incidents**: one paragraph each: what happened, impact, response, status, lessons.
4. **Detection engineering**: detections added/tuned/retired, ATT&CK coverage change, false-positive
   rate trend for top noisy rules.
5. **Visibility**: log source health (outages, coverage of critical assets), EDR coverage.
6. **Threat context**: relevant threats observed or reported for the sector and actions taken.
7. **Risks and asks**: e.g. unpatched VPN appliances, missing logs from a business unit, staffing.
8. **Appendix**: metric definitions, full tables.

## Metric discipline
- Define each metric once (appendix) and never change definitions silently; restate history if you must.
- Prefer rates and percentiles (p90 time to triage) to averages.
- Show trend over 6-13 months; single-month numbers mislead.

## Production
Automate data pulls from SIEM/SOAR/case management into a template; write narrative by the
SOC lead; review with the service owner before distribution.

## Gotchas
- Alert counts going up is not "more security"; explain drivers (new sources, tuning).
- Do not include sensitive incident details beyond the audience's need.

## Verify
Readers can answer: is the SOC meeting SLAs, what were the significant incidents, and what decisions
are needed. Compare one metric to the source system for accuracy each month.
