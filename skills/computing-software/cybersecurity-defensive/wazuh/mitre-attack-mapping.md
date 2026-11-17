---
id: computing-software.cybersecurity-defensive.wazuh.mitre-attack-mapping
name: mitre-attack-mapping
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [mitre-attack, mitre-id, rule-mitre, sysmon, eventchannel, pcre2]
level: practitioner
status: docs-checked
description: "Tag a Wazuh rule with a MITRE ATT&CK technique via the mitre id block and read the rule.mitre alert fields, with the Sysmon example."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A rule maps to a technique with a `<mitre>` block containing `<id>`. The page's example is rule 110011 with `<id>T1543.003</id>`, a child of `<if_sid>61615</if_sid>` that matches Sysmon fields (`win.eventdata.targetObject`, `win.eventdata.eventType`, `win.eventdata.user`) using `pcre2`; it alerts when a service named PSEXESVC is created, which happens each time PsExec runs. Edit `/var/ossec/etc/rules/local_rules.xml`, then restart `wazuh-manager`.

Resulting alert fields are arrays:
- `rule.mitre.id`, for example `["T1543.003"]`
- `rule.mitre.tactic`, here Persistence and Privilege Escalation
- `rule.mitre.technique`, here Windows Service

View them in the dashboard: the MITRE ATT&CK module (Intelligence, Framework, Dashboard and Events tabs) is under the Threat Detection and Response section; filter the Events tab (Security Module, MITRE ATT&CK, Events) by MITRE ID, tactic or technique.

Getting the Sysmon event to the server: install Sysmon with a configuration file, then the agent needs a `localfile` for `Microsoft-Windows-Sysmon/Operational` with `eventchannel` format, then a restart of the Wazuh agent service. In the page's example alert the Sysmon `ruleName` field reads `technique_id=T1543,technique_name=Service Creation`.

Gotchas:
- The page's example writes registry paths and `NT AUTHORITY\SYSTEM` in the `pcre2` patterns with four backslashes per literal backslash (for example `HKLM\\\\System\\\\...`); copy that pattern style.
- The page itself is inconsistent: a screenshot caption mentions T1053.005 while the text and JSON use T1543.003. Trust the rule you wrote.

## Checked

2026-11-08: confirmed against the Wazuh docs page MITRE ATT&CK framework (read in full): the mitre id block, rule 110011 and its fields, the alert fields and values, the Sysmon localfile and agent restart, the dashboard tabs and the caption inconsistency (T1053.005). Corrected dashboard navigation, field names and the backslash note; removed the unsupported claims about the Sysmon config source and wazuh-logtest.
Method: documentation only; no commands were run.
