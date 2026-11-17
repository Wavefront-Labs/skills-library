---
id: computing-software.cybersecurity-defensive.wazuh.fim-realtime-and-check-attributes
name: fim-realtime-and-check-attributes
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [realtime, check-all, report-changes, frequency, scan-time, ignore, fim-attributes]
level: practitioner
status: docs-checked
description: "Choose Wazuh FIM real-time versus scheduled scans, the check_* attributes, report_changes diffs, and ignore exclusions on directories entries."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/basic-settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Basic FIM behaviour is tuned with attributes on `<directories>` inside `<syscheck>`.

Real-time: `realtime="yes"` works only on directories, not single files, and only on Windows and Linux. The directory must exist before the agent restarts, otherwise it is ignored until a later restart.

Check attributes (all default to yes): `check_all` controls everything; `check_sum` covers MD5, SHA-1 and SHA-256; others are `check_sha1sum`, `check_md5sum`, `check_sha256sum`, `check_size`, `check_owner` (Linux), `check_group`, `check_perm`, `check_attrs` (Windows), `check_mtime`, `check_inode` (Linux). If options conflict, the last one configured wins.

Scheduled scans: `<frequency>` defaults to 43200 seconds (12 hours). `<scan_time>` (for example `10pm`) and `<scan_day>` (for example `saturday`) are alternatives.

Change reports: `report_changes="yes"` logs text diffs but copies monitored files into the queue diff folder (`/var/ossec/queue/diff/` on Linux), so storage grows. `<nodiff>` suppresses content for named files.

Exclusions: `<ignore>` takes one path per line; `type="sregex"` enables regex matching. Level 0 rules on the server (for example in `fim_ignore.xml`) are an alternative, followed by a `wazuh-manager` restart.

Gotcha: files created after the initial scan are added only at the next scheduled scan.

## Checked

2026-11-03. Confirmed against the Wazuh page "Basic settings" (FIM): realtime attribute limits and directory-must-exist note, the attribute table with defaults, last-option-wins precedence, 12-hour default frequency, scan_time and scan_day, report_changes storage and queue/diff path, nodiff, ignore with sregex, level 0 rules, and the next-scan note. Nothing removed.

Method: documentation only; no commands were run.
