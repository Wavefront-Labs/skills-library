---
id: computing-software.digital-forensics-incident-response.log-analysis.tahiti-threat-hunting-process
name: tahiti-threat-hunting-process
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [tahiti, threat-hunting, hunting-process, cyber-threat-intelligence, dfir]
level: practitioner
status: draft
description: "Run hunts with the TaHiTI methodology: initiate (trigger, abstract, backlog), hunt (define and refine hypothesis, investigate) and finalise (validate, document, hand over to other processes)."
sources: ["https://www.betaalvereniging.nl/en/safety/tahiti/", "https://www.betaalvereniging.nl/wp-content/uploads/TaHiTI-Threat-Hunting-Methodology-whitepaper.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TaHiTI threat hunting process

TaHiTI (Targeted Hunting integrating Threat Intelligence) was published in 2018 by the Dutch financial sector (Betaalvereniging Nederland and member banks). It structures hunting into three phases and six steps, with threat intelligence as the main driver and explicit hand-offs to other security processes.

## Phase 1: Initiate
1. **Trigger**: something prompts a hunt: threat intel (report, advisory), an incident's lessons, a red-team finding, a detection gap, a hunter's idea.
2. **Abstract**: write a short hunt abstract: the trigger, the threat, initial hypothesis direction, data sources needed, priority. Put it in the **hunt backlog**; prioritise the backlog regularly (relevance, impact, data availability).

## Phase 2: Hunt
3. **Define/refine**: turn the abstract into a testable hypothesis and investigation plan; enrich with threat intel (actor TTPs, procedures); identify data sources and analysis techniques; set scope and time box.
4. **Investigate**: execute queries and analysis; refine the hypothesis as findings emerge (iterate between steps 3 and 4). TaHiTI expects contextual intel to be pulled in during investigation, not only at the start.

## Phase 3: Finalise
5. **Validate**: confirm or reject the hypothesis; assess whether the conclusion is supported by the data (and whether data gaps make it inconclusive).
6. **Document and hand over**: record the hunt (hypothesis, data, queries, results) and hand outputs to other processes:
   - Incident response (malicious activity found)
   - Security monitoring / detection engineering (new use cases)
   - Threat intelligence (new indicators, actor behaviour observed)
   - Vulnerability management (weaknesses found)
   - Logging/visibility owners (data gaps)

## Using it in practice
- The hunt abstract template and backlog give management visibility; track backlog age and hunts completed.
- Pair with ATT&CK for hypothesis wording and PEAK-style hunt types if the team uses both; TaHiTI's distinctive pieces are the backlog and the structured hand-over.

## Gotchas
- Hunts that end without hand-over leave value on the table; the documentation step must name a receiving process or state "none required".
- Backlogs grow; prune triggers whose relevance expired.

## Verify
Each completed hunt has an abstract, a refined hypothesis, investigation records, a validation outcome, and recorded hand-overs to receiving processes.
