---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-log-settings-local-disk-and-memory
name: fortigate-log-settings-local-disk-and-memory
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [log-settings, fortios, local-disk-log, memory-log, log-filter, event-logging, traffic-log]
level: practitioner
status: draft
description: "Configure FortiGate local logging, retention, filters and event logs, and view logs from the CLI."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: logs stored where needed with predictable volume.

```
config log disk setting
    set status enable
    set maximum-log-age 14
    set diskfull overwrite
    set log-quota 5000
end
config log setting
    set local-in-allow enable
    set local-in-deny-unicast enable
    set resolve-ip disable
    set fwpolicy-implicit-log enable
end
config log eventfilter
    set event enable
    set system enable
    set vpn enable
    set user enable
end
```
Memory logging is limited and cleared on reboot; models without a disk rely on FortiAnalyzer/FortiCloud or syslog. Per-policy logging is `set logtraffic all|utm|disable`.

View logs:
```
execute log filter category 0
execute log filter field srcip 10.1.0.5
execute log display
```
(`category 0` is traffic; confirm numbers per release.)

Gotchas
- Logging all sessions on busy units slows throughput and fills disk; use `utm` plus selective `all`.
- The implicit deny is not logged by default (`fwpolicy-implicit-log enable` fixes that).
- Disk logging on SSD wears the disk; prefer remote logging.

## Verify
```
diagnose log kernel-stats
execute log display
get log disk setting
```
New traffic appears in the display within seconds.
