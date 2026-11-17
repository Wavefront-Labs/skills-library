---
id: computing-software.digital-forensics-incident-response.evidence-handling.collecting-digital-evidence-for-admissibility
name: collecting-digital-evidence-for-admissibility
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-admissibility, rfc-3227, authentication, best-evidence, chain-of-custody, dfir]
level: advanced
status: draft
description: "Collect digital evidence so it stays admissible (RFC 3227 2.4): authentication, integrity, reliability of tools, completeness, chain of custody and avoiding legal pitfalls."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://www.law.cornell.edu/rules/fre/rule_901", "https://www.law.cornell.edu/rules/fre/rule_902", "https://www.law.cornell.edu/rules/fre/rule_702", "https://www.cps.gov.uk/legal-guidance/computer-misuse-act"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collecting digital evidence for admissibility

RFC 3227 2.4 lists the properties computer evidence must have: **admissible** (conforms to legal rules), **authentic** (tied to the incident), **complete** (tells the whole story, not one side), **reliable** (collection and handling do not cast doubt), **believable** (understandable by a court). Assume any incident could end in court.

## Authenticity
- US FRE 901 needs evidence "that the item is what the proponent claims"; FRE 902(14) allows self-authentication of data copied from a device by hash verification with a qualified person's certification. So: hash at acquisition, re-hash at examination, record both.
- Record provenance: physical identifiers (serial numbers, photos), host identifiers (hostname, MAC, volume serial), and who collected.

## Reliability
- Use tools with known, tested behaviour; keep validation records (your own test against a reference image, or NIST CFTT reports) and versions.
- Avoid altering the source: write blockers for dead-box, documented and minimal footprint for live response.
- Expert testimony (FRE 702 / Daubert) will probe whether methods are generally accepted and whether you followed them; follow written SOPs and note deviations.

## Completeness
Collect exculpatory as well as inculpatory data; image whole sources where practical; do not cherry-pick log extracts without keeping the original full logs.

## Chain of custody
Unbroken record from seizure to court: who, when, why, condition, seal numbers. Gaps do not automatically exclude evidence but reduce its weight.

## Legal pitfalls to avoid
- Exceeding authority (searching data not covered by consent, policy or warrant).
- Hacking back or accessing attacker infrastructure: may be an offence (e.g. CFAA, UK Computer Misuse Act) and taints evidence.
- Privilege breaches (reading attorney-client mail without a filter process).
- Spoliation: deleting or reimaging before preservation once litigation is reasonably anticipated.

## Gotchas
- Business records exceptions cover routine logs; logs you created during the incident (e.g. ad hoc captures) need a witness to explain them.
- Different jurisdictions differ; for cross-border cases involve counsel early.

## Verify
For each key exhibit you can show: original hash, verification hash, tool validation record, complete custody chain and the authority under which it was collected.
