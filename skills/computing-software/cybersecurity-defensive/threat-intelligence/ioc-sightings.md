---
id: computing-software.cybersecurity-defensive.threat-intelligence.ioc-sightings
name: ioc-sightings
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [ioc-sightings, ioc-handling, misp, stix-sighting, confidence-scoring, ioc-lifecycle, threat-intelligence-platform]
level: practitioner
status: draft
description: "Record and use IOC sightings: reporting detections and false positives back to the TIP (MISP sightings, STIX sighting objects), and using sightings for scoring and expiry."
sources: ["https://www.misp-project.org/2019/02/27/MISP.2.4.103.released.html", "https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_a795guqsap3r", "https://www.circl.lu/doc/misp/sightings/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# IOC sightings

A sighting records that an indicator was observed (or judged a false positive) at a time, by a source.
Sightings turn a static IOC list into evidence of current relevance.

## MISP
- Types: `0` sighting (seen), `1` false positive, `2` expiration (indicator should be considered expired).
- Add via UI (thumbs up/down on attribute), API, or PyMISP:
```python
misp.add_sighting({"value": "203.0.113.50", "type": "0", "source": "proxy-detections", "timestamp": ts})
misp.add_sighting({"value": "198.51.100.7", "type": "1", "source": "soc-triage"})
```
- Sighting policies control visibility (who can see sightings: owner org, event contributors, all).
- **Decaying models** use sightings: an indicator's score decays over time and sightings refresh it;
  exports can filter by decayed score (`includeDecayScore`, `excludeDecayed`).

## STIX 2.1
`sighting` SRO: `sighting_of_ref` (indicator), `observed_data_refs`, `where_sighted_refs` (identity),
`first_seen`, `last_seen`, `count`. OpenCTI and TAXII-sharing communities exchange these.

## Automation
- SIEM/EDR detections matching TIP indicators post sightings automatically (SOAR step after an IOC
  match alert; Splunk ES threat activity -> MISP sighting).
- Analysts' false-positive dispositions post type `1` sightings, prompting review of the indicator's
  `to_ids` flag or warninglist addition.

## Using sightings
- Prioritise alerts on indicators with recent sightings in your community.
- Expire indicators with no sightings over N days (for IPs/domains especially).
- Share sightings back to communities (with sighting policy) - valuable to others even without details.

## Gotchas
- Sightings from your scanners or sandboxes are not real-world sightings; use a distinct source.
- Sharing sightings reveals you were targeted; check sharing policy and TLP.

## Verify
Sample IOC-matching alerts from last month: each has a corresponding sighting in the TIP with source and time.
