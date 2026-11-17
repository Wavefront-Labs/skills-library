---
id: computing-software.cybersecurity-defensive.threat-intelligence.sector-threat-landscape-assessment
name: sector-threat-landscape-assessment
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [threat-landscape, adversary-profiling, strategic-intelligence, threat-assessment, risk-assessment, intelligence-reporting]
level: advanced
status: draft
description: "Produce a sector threat landscape assessment: relevant actors and motivations, top techniques and vulnerabilities, trends, likelihood and impact, and recommended priorities."
sources: ["https://www.enisa.europa.eu/topics/cyber-threats/threats-and-trends", "https://www.verizon.com/business/resources/reports/dbir/", "https://www.cisa.gov/topics/cyber-threats-and-advisories"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sector threat landscape assessment

Strategic intelligence for leadership and risk owners, typically annual with quarterly updates.

## Inputs
- Your incident and alert data (what actually hit you), ISAC reporting for the sector, government
  assessments (ENISA Threat Landscape, NCSC/CISA annual reviews), DBIR sector breakdowns, vendor
  reports, leak site statistics for sector victims, regulator publications.

## Structure
1. **Key judgements** (3-6) with estimative language and confidence: e.g. "Ransomware will likely
   (55-80%) remain the most disruptive threat to EU logistics in 2027".
2. **Threat actors**: categories (state, criminal, hacktivist, insider) and named groups with
   motivation, capability, intent toward the sector, recent activity.
3. **Top techniques and initial access vectors**, with ATT&CK references.
4. **Exploited technologies/vulnerabilities** relevant to the sector's common stack.
5. **Trends and drivers**: geopolitics, regulation, technology changes (AI-enabled phishing, cloud).
6. **Implications for the organisation**: likelihood and impact against our profile; scenarios.
7. **Recommendations**: prioritised investments and actions; intelligence gaps.

## Method
- Tie each judgement to evidence; use analysis of competing hypotheses where contentious.
- Separate global trends from sector-specific signals; avoid copying vendor hype.
- Peer review with risk management for consistent likelihood/impact language.

## Gotchas
- Vendor reports reflect their telemetry and sales motives; triangulate.
- Long reports go unread; executive summary on one page.

## Verify
Key judgements reviewed after 12 months for accuracy; recommendations tracked in the risk register.
