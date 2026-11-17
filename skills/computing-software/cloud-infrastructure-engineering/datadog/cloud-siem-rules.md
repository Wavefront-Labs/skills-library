---
id: computing-software.cloud-infrastructure-engineering.datadog.cloud-siem-rules
name: cloud-siem-rules
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, cloud-siem, detection-rules, security-signals, threat-detection]
level: practitioner
status: docs-checked
description: "Use Cloud SIEM detection rules over logs to generate security signals, with suppression and notification."
sources: ["https://docs.datadoghq.com/security/cloud_siem/detect_and_monitor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud SIEM detection rules
Goal: detect suspicious activity in log data and turn it into security signals.

- Monitor Datadog telemetry with out-of-the-box (OOTB) detection rules or custom rules. A detected threat generates a security signal.
- OOTB rules begin analysing logs, Audit Trail events and Event Management events once the Cloud SIEM content packs are enabled and configured.
- OOTB rules can be edited: rename, extend the query (the original query cannot be edited, you add a custom query to it), change severity in Set conditions, and modify the playbook.
- Custom rules use log search syntax to build and join queries, then conditions decide if a signal is generated and at what severity. Signals carry a customisable playbook.
- Add suppressions to a rule so no signal is generated under specific conditions.
- When creating a rule, pick a rule type (real-time rules analyse incoming logs continuously; scheduled rules run at set intervals), then set conditions, severity and notification recipients under "And notify".
- Optionally test a rule against sample logs with Unit Test before enabling.
- Use the MITRE ATT&CK Map to see rule coverage against the framework.
- Case Management tracks signals that need further analysis.

Gotcha: a rule only sees logs that reach Datadog; enable the matching content pack first. Defensive use only.

## Verify
- Run Unit Test with a sample log; once the rule is enabled, look for its signals in the Signal Explorer.

## Checked
2026-11-09. Confirmed against the Datadog documentation source for Cloud SIEM detection rules (hugo/content/en/security/cloud_siem/detect_and_monitor/_index.md and custom_detection_rules/create_rule/_index.mdoc.md, plus cloud_siem/_index.md in DataDog/documentation): signal generation, OOTB rules and what can be edited, content packs, log search syntax, severity and "And notify" recipients, real-time and scheduled rule types, Unit Test, suppressions, the MITRE ATT&CK Map, Case Management and the Signal Explorer. Removed as unsupported: the CloudTrail example query, group-by and count/time thresholds as a worked rule, the Slack handle, the claim that OOTB rules "map to MITRE" by default, signals triggering workflows, the parsing-pipeline gotcha, and the low-severity trial and on-call routing advice, the menu path to Detection Rules, and RBAC scoping.
Method: documentation only; no commands were run.
