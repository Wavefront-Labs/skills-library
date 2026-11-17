---
id: computing-software.digital-forensics-incident-response.incident-response-process.intrusion-root-cause-analysis
name: intrusion-root-cause-analysis
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [root-cause-analysis, lessons-learned, five-whys, contributing-factors, postmortem, dfir]
level: advanced
status: draft
description: "Perform root cause analysis of an intrusion: technical root cause, contributing control failures, five whys and causal factor charts, blameless framing."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://sre.google/sre-book/postmortem-culture/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intrusion root cause analysis

**Goal:** understand not just how the attacker got in, but why the organisation's controls
allowed each stage, so fixes address causes and not symptoms.

## Three levels
1. **Proximate technical cause**: e.g. unpatched VPN appliance CVE exploited.
2. **Control failures per stage**: what should have prevented or detected each step of the
   attack and why it did not (missing, misconfigured, alert ignored, not monitored).
3. **Organisational root causes**: patch process had no SLA for edge devices, asset
   inventory missing the appliance, SOC understaffed at night.

## Method
- Start from the master timeline; for each ATT&CK stage list: preventive control expected,
  detective control expected, what actually happened, evidence.
- **Five whys** on the key failures:
  VPN exploited -> not patched -> patch released 40 days earlier -> appliance not in vuln
  scanner scope -> asset inventory excludes network appliances -> ownership unclear.
- Causal factor chart or fishbone (people, process, technology) for complex incidents.
- Identify **detection opportunities missed**: alerts that fired and were closed, logs that
  existed but were not monitored.

## Blameless framing
Focus on systems and conditions. "Analyst closed the alert" becomes "alert lacked context and
the queue had 400 items per analyst per shift". Blame makes people hide information next time.

## Output
A table: stage, failure, root cause, recommended fix, owner, priority. Feed it to the
lessons-learned meeting and the final report.

## Verify
Each recommended fix traces to a root cause, and each root cause has at least one fix; if
the same incident replayed after fixes, at least one stage would be prevented or detected.
