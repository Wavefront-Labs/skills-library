---
id: computing-software.digital-forensics-incident-response.log-analysis.sigma-rules-and-detection-engineering
name: sigma-rules-and-detection-engineering
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sigma, sigma-rules, detection-engineering, pysigma, sigmac, false-positive-tuning, siem, splunk-spl, kql, elastic-eql, mitre-attack, detection-as-code, logsource, dfir, threat-hunting]
level: advanced
status: docs-checked
description: "Turn a confirmed IOC/TTP from an investigation into a tuned Sigma rule, convert it to a SIEM's native query language, and manage false-positive feedback without gutting detection coverage."
sources: ["https://github.com/SigmaHQ/sigma-specification/blob/main/specification/sigma-rules-specification.md", "https://github.com/SigmaHQ/sigma-specification/blob/main/specification/sigma-appendix-taxonomy.md", "https://github.com/SigmaHQ/sigma-specification/blob/main/specification/sigma-appendix-tags.md", "https://github.com/SigmaHQ/sigma-cli", "https://github.com/SigmaHQ/pySigma"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sigma rules and detection engineering

**Goal:** close the loop from
computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting's
hypothesis-driven hunt — once a hunt finds something real, turn it into a rule that
fires automatically next time, in a format that isn't locked to one SIEM.

## 1. Why Sigma, and its actual shape
Sigma is a vendor-neutral YAML rule format for log-based detections — one rule,
converted with `pySigma`/`sigma-cli` to the query language of a backend plugin (list the installed
backends with `sigma list targets`). The point is writing the detection logic
**once**, against a normalized field model, rather than re-deriving it per SIEM.
```yaml
title: Suspicious LSASS Access via Known Dumping Tool Pattern
logsource:
  category: process_access
  product: windows
detection:
  selection:
    TargetImage|endswith: '\lsass.exe'
    GrantedAccess|contains: '<access-mask-observed-in-the-incident>'
  condition: selection
falsepositives:
  - Some legitimate EDR/AV agents request similar access rights
level: high
```
`logsource` (category/product/service) determines which field-mapping config the
converter uses — get this wrong and the converted query references fields that don't
exist in the target SIEM's schema.

## 2. From investigation finding to rule
- Write the rule against the **specific field values the investigation actually
  observed** first (exact command line, exact registry path), then generalize
  deliberately — a rule copied verbatim from one incident's exact artifact (a specific
  C2 domain, a specific dropped filename) expires the moment the actor changes that
  detail, which happens fast. The durable version keys on the *technique* (e.g. LSASS
  access rights pattern above, not a specific tool's exact process name) — map it to
  a MITRE ATT&CK technique ID and tag the rule with it (the `attack.` tag namespace, e.g. `attack.t1003.001`); this is what makes a rule
  survive variant tooling.
- Sigma's `detection` block composition (`selection`/`filter`/`condition`) lets you
  express "this pattern, EXCLUDING these known-legitimate exclusions" cleanly —
  put the exclusions in a named `filter` block and reference it in `condition:
  selection and not filter`, rather than cramming negative logic into one giant
  selection block that becomes unreadable at the third exception.

## 3. Conversion and field mapping are where rules silently break
`sigma-cli` needs a **pipeline** (field-mapping config) for the specific log source
and target backend — `sigma convert -t splunk -p sysmon rule.yml`. A rule that looks
correct in YAML can convert to a query referencing the wrong field name if the
pipeline doesn't match how the target SIEM actually ingests that log source (e.g. a
custom Sysmon field-renaming on ingest that the stock pipeline doesn't know about).
**Always test-fire the converted query against a known-positive log sample** before
deploying — a silent field-mapping mismatch produces a rule that "runs" and never
fires, which is worse than no rule because it creates false confidence in coverage.

## 4. False-positive tuning without gutting the rule
When a deployed rule generates noise, the fix is almost always a **targeted
exclusion** (a specific parent process, a specific known-legitimate tool's exact
command-line pattern) added to the `filter` block — not broadening the `selection`
block's match criteria, which is how rules quietly stop detecting the thing they were
written for. Track each exclusion with a comment/changelog entry naming what
legitimate activity it covers, so a later reviewer can tell a deliberate, justified
exclusion from an undocumented hole punched in under pressure during an on-call noisy
night.

## Verify
- Test-fire every converted rule against at least one known-positive log sample in
  the target SIEM before considering it deployed.
- Confirm the rule is tagged with the relevant MITRE ATT&CK technique ID and references
  the triggering investigation/incident for traceability.
- Review any false-positive exclusion added under time pressure within a defined
  window (e.g. the next sprint) to confirm it's still narrowly scoped and documented.

Unconfirmed: exact pySigma pipeline coverage and field-mapping completeness varies by
backend and log source — verify the specific pipeline against the target SIEM's actual
ingest schema before trusting a conversion for a new log source.

## Checked

Checked 2026-10-25 against the Sigma specification (SigmaHQ/sigma-specification, last pushed 2026-09-25) and the sigma-cli README (SigmaHQ/sigma-cli, last pushed 2026-10-04). Confirmed: required rule sections (title, logsource, detection) and optional ones, `logsource` category/product/service, the taxonomy entry `product: windows`, `category: process_access` (Sysmon event 10), the `selection and not filter` condition pattern, the `contains` and `endswith` value modifiers, the `attack.` tag namespace, and `sigma convert -t <backend> -p <pipeline> <file or directory>` with `sigma list` to find backends and pipelines. Corrected: the ATT&CK name typo, the unconfirmed `sigmac` succession claim and the specific access mask values (replaced by a placeholder to fill from the investigation).

Method: documentation only; no commands were run.
