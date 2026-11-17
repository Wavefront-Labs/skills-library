---
id: computing-software.cybersecurity-defensive.security-operations.dettect-data-source-coverage
name: dettect-data-source-coverage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, dettect, data-source-coverage, attack-navigator, data-components, visibility-scoring, detection-coverage]
level: advanced
status: draft
description: "Measure log visibility and detection coverage against ATT&CK with DeTT&CT: data source files, data quality scores, visibility and detection layers, gap priorities."
sources: ["https://github.com/rabobank-cdc/DeTTECT", "https://github.com/rabobank-cdc/DeTTECT/wiki", "https://attack.mitre.org/datasources/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data source coverage with DeTT&CT

DeTT&CT (Rabobank CDC) answers two questions: which ATT&CK techniques can we **see** (visibility from
log data) and which can we **detect** (rules), scored and visualised as ATT&CK Navigator layers.

## Install and run
```
# DeTT&CT is not on PyPI (checked): clone github.com/rabobank-cdc/DeTTECT and `pip install -r requirements.txt`, or use the Rabobank CDC docker image
# (image name not re-verified)
python dettect.py editor     # web editor for YAML admin files
```

## Data source administration file
List each ATT&CK data component you collect (e.g. Process Creation, Command Execution, Logon Session
Creation, Network Traffic Flow, DNS Query, Windows Registry Key Modification) with:
- platforms and products (Sysmon, MDE, Zeek, CloudTrail),
- date registered/connected,
- **data quality** scores (1-5) for device completeness, data field completeness, timeliness, consistency,
  retention.
Generate a visibility layer:
```
python dettect.py ds -fd data-sources.yaml -l       # Navigator layer of data source coverage
python dettect.py v -ft techniques.yaml -fd data-sources.yaml -l   # visibility scores per technique
```

## Technique administration file
For each technique: visibility score (0-4, with comment and date) and detection score (-1 to 5) with
location (rule IDs, SIEM, EDR). Generate:
```
python dettect.py d -ft techniques.yaml -l          # detection layer
python dettect.py d -ft techniques.yaml -o          # overlay detection vs visibility
```

## Using the results
- Techniques with good visibility but no detection: cheap wins for detection engineering.
- Techniques with no visibility: data collection projects (enable 4688 command line, Sysmon events,
  cloud data events); prioritise by threat relevance (actors targeting you, ATT&CK groups layer overlay).
- Track score changes over time in Git (YAML files) and report quarterly.

## Gotchas
- Scores are self-assessed; validate with purple team tests (does the rule actually fire?).
- "Detected" for a technique with one narrow procedure overstates coverage; score honestly and note procedures.
- Keep the files maintained in the detection repo or they go stale within months.

## Verify
Navigator overlay renders with current scores, and three randomly chosen "detected" techniques are
confirmed by running the corresponding atomic tests.
