---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-log-forwarding-profiles
name: pan-os-log-forwarding-profiles
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [log-forwarding, pan-os, log-forwarding-profile, panorama-logging, match-list, auto-tagging, system-logs]
level: practitioner
status: draft
description: "Create PAN-OS log forwarding profiles for traffic, threat and URL logs, include auto-tagging, and attach them to security rules."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/configure-log-forwarding"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: every log type that matters reaches Panorama and the SIEM, and attached rules actually generate logs.

```
configure
set shared log-settings profiles LFP-STD match-list ml-traffic log-type traffic filter "All Logs" send-to-panorama yes send-syslog SYSLOG-SIEM
set shared log-settings profiles LFP-STD match-list ml-threat log-type threat filter "(severity geq high)" send-to-panorama yes send-syslog SYSLOG-SIEM
set rulebase security rules allow-web log-setting LFP-STD log-end yes
set shared log-settings system match-list sys-high filter "(severity geq high)" send-syslog SYSLOG-SIEM
set shared log-settings config match-list cfg-all filter "All Logs" send-syslog SYSLOG-SIEM
commit
```
System, config, user-ID, HIP and GlobalProtect logs are not rule-based; they use the shared log-settings sections as above.

Auto-tagging: add `actions` in a match-list to tag the source IP (for example `quarantine`) which dynamic address groups can then use to isolate the host (see dynamic-address-group skill).

Gotchas
- A rule without a log-setting writes local logs only; you will not see it in Panorama or SIEM.
- Disk fills if log quotas are not set (Device > Setup > Management > Logging and Reporting Settings).
- Filters use the log filter syntax of the Monitor tab; copy them from there.

## Verify
```
show log traffic direction equal backward
show logging-status
```
Check `show logging-status` for Panorama and syslog connected, and that new events appear downstream within seconds.
