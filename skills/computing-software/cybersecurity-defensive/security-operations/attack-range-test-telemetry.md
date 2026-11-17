---
id: computing-software.cybersecurity-defensive.security-operations.attack-range-test-telemetry
name: attack-range-test-telemetry
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [attack-range, detection-engineering, atomic-red-team, test-data, attack-data, detection-testing, purple-team]
level: advanced
status: draft
description: "Generate detection test telemetry with Splunk Attack Range or similar labs: build the range, run Atomic Red Team or simulations, capture datasets and replay them."
sources: ["https://github.com/splunk/attack_range", "https://github.com/splunk/attack_data", "https://github.com/redcanaryco/atomic-red-team"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Generating test telemetry with attack ranges

Detections need realistic positive samples. An attack range is a disposable lab with logging
identical to production that you attack on purpose.

## Splunk Attack Range
- Terraform + Ansible build on AWS/Azure/local: Splunk server, Windows DC/servers with Sysmon and
  Universal Forwarder, Linux hosts, optional Zeek, Kali.
```
python attack_range.py configure     # writes attack_range.yml
python attack_range.py build
python attack_range.py simulate -e ART -te T1003.001 -t ar-win-dc-0
python attack_range.py dump --file_name t1003_001 --search 'index=win' --earliest 2h
python attack_range.py destroy
```
- Simulation engines: Atomic Red Team, PurpleSharp; custom commands via Ansible.
- `dump` exports raw logs used as test datasets (attack_data repository format).

## Alternatives
- DetectionLab-style local labs, Elastic's detection-rules test data, Mordor/Security Datasets
  (OTRF) pre-recorded datasets, Microsoft's attack simulation in Defender evaluation labs.

## Making datasets useful
- Match production logging config (Sysmon config, audit policies, EDR) or the data will not match.
- Record metadata: technique, tool/command, host OS, logging config version, time window.
- Include benign background noise or negative samples to test false-positive behaviour.
- Store with the detection in the repo (`tests/<detection>/dataset.log`) and replay in CI: Splunk
  `contentctl test` replays attack_data into a container and asserts the detection fires.

## Gotchas
- Cloud costs: always `destroy`; ranges left running are expensive and exposed.
- Lab hosts must be isolated; Atomic tests run real tooling (credential dumping etc.).
- Simulation tools produce artefacts specific to themselves; vary procedures to avoid overfitting.

## Verify
Each production detection has at least one recorded dataset that triggers it in CI replay.
