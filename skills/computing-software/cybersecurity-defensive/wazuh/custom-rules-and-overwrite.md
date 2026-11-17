---
id: computing-software.cybersecurity-defensive.wazuh.custom-rules-and-overwrite
name: custom-rules-and-overwrite
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [custom-rules, local-rules, overwrite, rule-ids, rule-5710, wazuh-logtest]
level: practitioner
status: docs-checked
description: "Add custom Wazuh rules with IDs 100000 to 120000 in local_rules.xml and modify default rules with overwrite=yes, noting which if_ options are ignored."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/rules/custom.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use rule IDs between 100000 and 120000 for custom rules to avoid clashing with default rules.

Where: minor changes go in `/var/ossec/etc/rules/local_rules.xml`; larger sets go in new files under `/var/ossec/etc/rules/`. The page's example is rule `100010`, level `0`, matching `<program_name>example</program_name>`.

Testing: use `/var/ossec/bin/wazuh-logtest`. Saving the file is enough for testing, but the manager must be restarted to generate alerts: `systemctl restart wazuh-manager` or `service wazuh-manager restart`.

Changing a default rule: files in `/var/ossec/ruleset/rules` are overwritten on upgrade. Copy the rule into a file in `/var/ossec/etc/rules/`, edit it and add `overwrite="yes"`. The page's example raises SSH rule `5710` from level 5 to 10; the original is in `/var/ossec/ruleset/rules/0095-sshd_rules.xml`.

Gotcha: `if_sid`, `if_group`, `if_level`, `if_matched_sid` and `if_matched_group` cannot be overwritten. In an overwrite rule they are ignored and the original values are kept, so you cannot re-parent a default rule this way.

## Checked

2026-11-08: confirmed against the Wazuh docs page Custom rules (read in full): the 100000 to 120000 ID range, local_rules.xml, the rule 100010 example, wazuh-logtest and restart behaviour, overwrite=yes with rule 5710 level 5 to 10 and 0095-sshd_rules.xml, and the five if_ tags that cannot be overwritten. Removed the unsupported advice on always adding a description and group.
Method: documentation only; no commands were run.
