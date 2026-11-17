---
id: computing-software.digital-forensics-incident-response.log-analysis.hunting-maturity-model-assessment
name: hunting-maturity-model-assessment
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [hunting-maturity-model, threat-hunting, hmm, program-assessment, dfir]
level: practitioner
status: draft
description: "Assess a threat-hunting program with the Hunting Maturity Model (HMM0 to HMM4): evidence for each level, data collection versus process maturity, and a roadmap to the next level."
sources: ["https://www.threathunting.net/files/framework-for-threat-hunting-whitepaper.pdf", "https://detect-respond.blogspot.com/2015/10/a-simple-hunting-maturity-model.html", "https://www.sans.org/white-papers/37172/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hunting maturity model assessment

David Bianco's Hunting Maturity Model (published with Sqrrl, 2015) rates hunting capability on two factors: the quality and quantity of data collected, and how the team creates and automates hunts.

## Levels
| Level | Name | Characteristics |
|---|---|---|
| HMM0 | Initial | Relies on automated alerts (IDS/AV/SIEM); little or no routine data collection; no hunting |
| HMM1 | Minimal | Collects some routine data; hunts mainly by searching for IOCs from threat intel |
| HMM2 | Procedural | Follows hunting procedures written by others (published playbooks), regularly; moderate to high data collection |
| HMM3 | Innovative | Creates its own hunting procedures and hypotheses; high data collection; analysts understand data analysis techniques |
| HMM4 | Leading | Automates successful hunts into detections so hunters keep working on new problems; high data collection |

## Assessment method
1. **Data**: inventory sources available to hunters (endpoint process/network telemetry, DNS, proxy, authentication, cloud), retention, search speed. HMM2 and above need broad endpoint and network visibility.
2. **Process evidence** (not claims): hunt records over the last 6 to 12 months, how hypotheses originated, documentation quality, whether a repeatable process (PEAK, TaHiTI) is used.
3. **Automation evidence**: count of hunts converted into detections, with links.
4. **People**: hunter time allocation (dedicated vs left-over time), training in data analysis.
Rate the lower of data and process; a team writing novel hypotheses without endpoint telemetry is not HMM3.

## Roadmap examples
- HMM1 -> HMM2: adopt a library of published hunts (ThreatHunter-Playbook, vendor packs), schedule them, document outcomes.
- HMM2 -> HMM3: hypothesis backlog fed by intel and incidents, analysts trained in stacking/statistics, time-boxed self-originated hunts.
- HMM3 -> HMM4: detection-as-code pipeline; every successful hunt ends with a detection proposal.

## Gotchas
- Maturity is not hunt count; ten IOC sweeps are still HMM1.
- Do not skip data foundations; hypothesis-driven hunting without telemetry produces only "not enough data" outcomes.

## Verify
The assessment cites specific hunt records, data-source inventory and detection conversions for the assigned level, and the roadmap has dated actions.
