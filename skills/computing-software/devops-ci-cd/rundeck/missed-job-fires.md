---
id: computing-software.devops-ci-cd.rundeck.missed-job-fires
name: missed-job-fires
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, misfire-detection, missed-execution, misfire-threshold, scheduler]
level: advanced
status: docs-checked
description: "Detect scheduled Rundeck jobs that did not fire: misfire marking, threshold and check-rate settings, and how it interacts with failure notifications (Enterprise)."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/schedules/missedjobfires.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If a scheduled job does not run at its scheduled time, an execution with status "missed" is added to the Activity page. If the job has a failure notification, it fires and reports the miss. Enterprise only.

Behaviour notes:
- Only the last "next execution" time is checked. If several executions of one job were missed, there is a single missed mark.
- Next execution times account for calendars, and project, system and job schedules.
- Detection is enabled by default.

Change settings in System Menu > Configuration Management (Add Config), or in `rundeck-config.properties`:

```properties
rundeck.feature.misfireDetection.enabled=true
rundeck.scheduler.misfire.threshold=60000
rundeck.scheduler.misfire.checkRate=60000
```

- `threshold`: milliseconds past schedule before a run counts as missed (default 60000).
- `checkRate`: milliseconds between checks (default 60000).

Gotcha: keep the configuration identical on every cluster member or results can be unexpected.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Missed Job Fires (Enterprise Only): missed status on the Activity page, failure notification triggering, single missed mark, next execution calculation, enabled by default, Configuration Management steps, the three rundeck properties with 60000 ms defaults, and the identical cluster configuration note. Nothing removed.

Method: documentation only; no commands were run.
