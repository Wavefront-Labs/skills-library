---
id: computing-software.cybersecurity-defensive.wazuh.fim-report-changes-and-nodiff
name: fim-report-changes-and-nodiff
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [report-changes, nodiff, syscheck-diff, rule-550, realtime]
level: practitioner
status: docs-checked
description: "Show file content changes in Wazuh FIM alerts with report_changes=yes and hide sensitive files from diffs with nodiff, using the documented /appfolder example."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/use-cases/reporting-file-changes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To see what changed inside a file, enable `report_changes`. The documented example uses a CentOS Stream 10 agent and `/var/ossec/etc/ossec.conf`:

```xml
<syscheck>
  <directories realtime="yes" report_changes="yes">/appfolder</directories>
  <nodiff>/appfolder/private-file.conf</nodiff>
</syscheck>
```

Apply with `systemctl restart wazuh-agent`, after creating the directory with `mkdir /appfolder`.

Test: create `appreport.conf` and `private-file.conf` in the folder and append a line to each. The File Integrity Monitoring view shows alerts from rule `550`. The `syscheck.diff` field contains the added text for `appreport.conf` but shows no content for `private-file.conf`.

Gotchas:
- `report_changes` copies monitored files for diffing, so storage on the agent grows with the monitored set.
- `<nodiff>` hides only the content diff. The page does not state whether the change alert for that file is suppressed, so do not assume the event disappears.
- Use `nodiff` for files whose contents should not appear in alerts; the Basic settings page says it avoids leaking file content through alerts.

## Checked

2026-11-03. Confirmed against the Wazuh pages "Reporting file changes" and "Basic settings": the /appfolder example on CentOS Stream 10, the exact syscheck block, restart command, test files, rule id 550 alerts, `syscheck.diff` behaviour, and that report_changes copies monitored files (storage). Removed: the "hold secrets / credentials" wording, which the pages do not state.

Method: documentation only; no commands were run.
