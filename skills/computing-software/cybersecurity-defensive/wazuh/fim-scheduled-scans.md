---
id: computing-software.cybersecurity-defensive.wazuh.fim-scheduled-scans
name: fim-scheduled-scans
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [frequency, scheduled-scan, fim-interval, macos, wazuh-control]
level: intro
status: docs-checked
description: "Run Wazuh FIM on a fixed interval using syscheck frequency, as shown for a macOS agent scanning a single file every 300 seconds, and know the detection delay."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/use-cases/monitoring-files-at-specific-intervals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scheduled FIM checks files on a timer instead of in real time. The documented example monitors one file every five minutes on a macOS Monterey agent.

Add to `/Library/Ossec/etc/ossec.conf`:

```xml
<syscheck>
  <frequency>300</frequency>
  <directories>/Users/*/Documents/user_details.txt</directories>
</syscheck>
```

`<frequency>` is the scan interval in seconds (300 is five minutes). The `<directories>` entry can be a single file and may use wildcards.

Steps: create the file, add the `<syscheck>` block, then restart with `/Library/Ossec/bin/wazuh-control restart`.

Test by modifying the file and waiting for the interval. Review the resulting alert in the FIM view of the Wazuh dashboard.

Failure modes:
- Changes are not reported immediately; detection happens only at the next scheduled scan, so a 300 second interval means up to five minutes of latency.
- The agent must be restarted after editing the configuration.
- Without the setting, the default scan frequency is 43200 seconds (12 hours), so lowering it is what makes this use case timely.
- Real-time monitoring is not available for single files, so scheduled scans are the way to watch an individual file.

## Checked

2026-11-03. Confirmed against the Wazuh pages "Monitoring files at specific intervals" and "Basic settings": the macOS Monterey example, the `<frequency>300</frequency>` block, restart command, test step, default 43200-second frequency, and that realtime works only on directories. Fixed: the example path now matches the page (`/Users/*/Documents/user_details.txt`).

Method: documentation only; no commands were run.
