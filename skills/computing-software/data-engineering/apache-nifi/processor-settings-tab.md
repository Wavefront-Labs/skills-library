---
id: computing-software.data-engineering.apache-nifi.processor-settings-tab
name: processor-settings-tab
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, penalty-duration, yield-duration, bulletin-level, processor-config]
level: intro
status: docs-checked
description: "Processor Settings tab defaults: Penalty Duration 30 secs, Yield Duration 1 sec, Bulletin level WARN, enabled flag, plus the Properties and Comments tabs."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Processor settings

Settings tab:
- Name and Enabled. A disabled processor is skipped when its group is started.
- Penalty Duration: 30 seconds (how long a penalized FlowFile waits).
- Yield Duration: 1 second.
- Bulletin level: WARN (shows warnings and errors; hover the bulletin icon to read them).

Properties tab: processor-specific properties with help icons; New Property adds user-defined properties, sensitive if the processor supports it; some processors have an Advanced UI button.

Related admin keys: `nifi.administrative.yield.duration` 30 secs, `nifi.bored.yield.duration` 10 ms.

Verify: the processor shows no validation warnings and bulletins appear at the chosen level.

## Checked

Checked against the NiFi User Guide, Processor Settings and Properties tab sections, and the Administration Guide system properties: Penalty 30 seconds, Yield 1 second, Bulletin level WARN, the disabled-processor behaviour, user-defined and sensitive properties, the Advanced button, `nifi.administrative.yield.duration` 30 secs and `nifi.bored.yield.duration` 10 ms match.

Method: docs-only read of cited pages, 2026-11-08
