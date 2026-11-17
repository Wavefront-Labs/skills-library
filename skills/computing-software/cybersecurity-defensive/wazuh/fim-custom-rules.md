---
id: computing-software.cybersecurity-defensive.wazuh.fim-custom-rules
name: fim-custom-rules
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [fim-rules, changed-fields, if-sid, rule-550, rule-553, custom-rules]
level: practitioner
status: docs-checked
description: "Write custom Wazuh rules on FIM alerts by chaining from base rules 550 and 553 and matching mapped fields such as file, changed_fields and process_name."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/creating-custom-fim-rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom FIM rules go in `/var/ossec/etc/rules/`; restart `wazuh-manager` afterwards.

Field names used inside rules map to alert fields:
- `file` is alert `path`; `size` is `size_after`
- `perm` is `perm_after` or `win_perm_after`
- `changed_fields` is `changed_attributes`; `changed_content` is `diff`
- `win_attributes` is `attrs_after`
- `user_name` is `audit.user.name`; `process_name` is `audit.process.name`

Examples from the page:
- Rule `100002`, level 8, `if_sid` 550: matches `file` `.sh$`, `changed_fields` `^permission$` and `perm` `\w\wx` with PCRE2 to flag execute permission added to scripts (MITRE T1222.002). The agent monitors the directory with `realtime="yes"`.
- Rule `100003`, level 8, `if_sid` 553: matches `process_name` `explorer.exe$` and a `user_name` to catch deletion through File Explorer (T1070.004, T1485). The agent uses `whodata="yes"`.
- Rule `100005`, level 12, `if_sid` 550, `file` `customer_details.rtf`: raises severity for a sensitive file. The macOS agent uses `<frequency>300</frequency>` and the page waits 5 minutes for the scan before the alert appears.

Note: `user_name` and `process_name` map to `audit.*` alert fields; the page's example using them monitors the directory with `whodata="yes"`.

## Checked

2026-11-03. Confirmed against the Wazuh page "Creating custom FIM rules": the decoded-field to alert-field table, the three example rules (ids 100002, 100003, 100005, levels, `if_sid` 550/553, field regexes, MITRE ids), the monitored-directory settings, and manager restarts. Removed: the unsupported statement that who-data is required (the page only shows it in its example).

Method: documentation only; no commands were run.
