---
id: computing-software.cybersecurity-defensive.threat-intelligence.ioc-extraction-from-reports
name: ioc-extraction-from-reports
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [ioc-extraction, ioc-handling, iocextract, refanging, threat-intelligence-platform, misp, automation]
level: practitioner
status: docs-checked
description: "Extract IOCs from threat reports reliably: parsing PDFs and blogs with iocextract/ioc-finder, refanging, deduplication, context capture, false-positive filtering and TIP import."
sources: ["https://github.com/InQuest/python-iocextract", "https://github.com/fhightower/ioc-finder", "https://www.misp-project.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IOC extraction from reports

## Tooling
- `iocextract` (InQuest): extracts URLs, IPs, emails, hashes, YARA rules; handles defanged forms
  (`hxxp`, `[.]`) with `refang=True`.
```python
import iocextract
text = open("report.txt").read()
urls = set(iocextract.extract_urls(text, refang=True))
# the README documents further extractors for IPs, hashes, emails and YARA rules
```
- `ioc-finder`: covers more indicator types than iocextract; see its README.
- Convert PDFs to text first; tables in PDFs often split values across lines - check hashes for
  truncation (length 64 for SHA-256).

## Context
IOC without context is noise. Capture per indicator: role (C2, payload hash, phishing sender),
first/last seen in report, associated malware/actor, ATT&CK technique, report source and TLP,
confidence.

## Filtering false positives
- Remove references and benign domains (vendor's own domain, `microsoft.com`, `github.com`, example
  domains, sinkholes); MISP warninglists automate this.
- Private IPs and documentation-range IPs.
- Hashes of legitimate tools mentioned in the report (e.g. `rclone`, `AnyDesk`) - keep as context, not
  as block indicators.

## Import
Create a TIP event per report with attributes and `to_ids` set only for detection-worthy indicators;
tag with source, TLP, actor/malware galaxies.

## Verify
Spot check: extracted count equals report appendix count; no indicator on warninglists marked for IDS export.

## Checked
2026-10-28. Confirmed in the python-iocextract README: it extracts URLs, IP addresses, MD5/SHA hashes, email addresses and YARA rules, handles defanged forms such as `127[.]0[.]0[.]1`, and offers `extract_urls` with `refang`. Removed: the unconfirmed `extract_ipv4s`/`extract_sha256_hashes` names, `(dot)` form, pdftotext command, ioc-finder type list, MISP freetext and OpenCTI import claims, example CIDRs.
Method: documentation only; no commands were run.
