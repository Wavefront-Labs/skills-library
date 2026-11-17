---
id: computing-software.digital-forensics-incident-response.log-analysis.intelligence-driven-threat-hunts
name: intelligence-driven-threat-hunts
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [intel-driven-hunting, threat-hunting, cyber-threat-intelligence, ttp-hunting, dfir]
level: practitioner
status: draft
description: "Run intelligence-driven threat hunts: turn a threat report into testable hypotheses at the TTP level, map to your telemetry, hunt, and feed results back to intel and detection."
sources: ["https://www.sans.org/white-papers/37172/", "https://attack.mitre.org/resources/", "https://www.cisa.gov/news-events/cybersecurity-advisories", "https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intelligence-driven threat hunts

An intelligence-driven hunt starts from external or internal intelligence (a vendor report, a CISA advisory, an ISAC alert, a peer's incident) and asks: has this happened here? The value is in hunting behaviours, not just sweeping the report's IOCs.

## From report to hypotheses
1. **Relevance**: does the actor target our sector, region or technology? Is the vulnerability or product in our estate?
2. **Extract** at every level of the Pyramid of Pain: hashes, IPs, domains (sweep quickly), then tools and TTPs (hunt properly).
3. **Map TTPs to ATT&CK** and to concrete procedures: not "T1003" but "used `comsvcs.dll MiniDump` via rundll32 against LSASS".
4. **Write hypotheses**: "If actor X compromised our VPN appliances, we would see web requests to `/dana-na/` paths with anomalous parameters followed by new local accounts on the appliance".
5. **Check visibility**: which data sources can test each hypothesis, and for what retention period? Note gaps.

## Hunting
- IOC sweep first across the full retention (cheap, fast closure if hit).
- Procedure hunts with tuned queries for each hypothesis; stack and baseline results.
- Look one step either side of the documented behaviour (what would precede and follow it in your environment).
- Time-box per hypothesis.

## Outcomes
| Result | Action |
|---|---|
| Malicious activity found | Escalate to incident; preserve evidence |
| Nothing found, good visibility | Record as negative finding with data sources and time range |
| Nothing found, visibility gap | Log the gap as a finding for the logging backlog |
| Benign but noisy patterns | Document as baseline knowledge |
Convert durable hunts into detections (Sigma rules with ADS docs) and share new indicators or procedure insights back to intel (under TLP).

## Gotchas
- Reports often lag the activity by weeks; hunt the full retention window, not the last 7 days.
- IOC-only hunts that return nothing give false comfort; the actor's infrastructure rotates.
- Vendor reports may contain errors or defanged IOCs needing normalisation.

## Verify
Each hunt record lists the source intelligence, hypotheses, data sources and time ranges queried, results per hypothesis and follow-up actions.
