---
id: computing-software.messaging-and-integration.apache-camel.quartz-component
name: quartz-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, quartz, cron, scheduling]
level: practitioner
status: docs-checked
description: "Camel quartz component: URI forms, cron with + for spaces, trigger.repeatInterval, stateful, durableJob, deleteJob and pauseJob rules, autoStartScheduler and fire headers."
sources:
  - https://camel.apache.org/components/next/quartz-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quartz:

Forms: `quartz://timerName?options` or `quartz://groupName/timerName?options`. Group defaults to `Camel`. A `cron` option creates a `CronTrigger`; otherwise a `SimpleTrigger`.

Cron in URIs: `+` replaces spaces, so `cron=0+0/5+12-18+?+*+MON-FRI` equals `0 0/5 12-18 ? * MON-FRI`.

Simple trigger: set via `triggerParameters` with the `trigger.` prefix, e.g. `trigger.repeatInterval=2000&trigger.misfireInstruction=4`, with `repeatCount`. Intervals of 1000 ms or less can make the first events fire faster than expected after startup.

Job options (all default `false`): `stateful` (uses `PersistJobDataAfterExecution` and `DisallowConcurrentExecution`), `durableJob` (keep stored after no triggers point to it), `recoverableJob` (re-execute after recovery or fail-over).

Lifecycle: `deleteJob` true (delete trigger when the route stops), `pauseJob` false (pause instead); both cannot be true.

Scheduler: `autoStartScheduler` true (component and endpoint); `triggerStartDelay` 500 ms so the endpoint is fully started; component `properties` (Map), `propertiesFile` (classpath) or `propertiesRef` configure Quartz.

Headers from the execution context include `fireTime`, `nextFireTime`, `previousFireTime`, `scheduledFireTime`, `refireCount`, `jobDetail`, `trigger`, `triggerName`, `triggerGroup`.

Verify: `quartz://reports/daily?cron=0+0+2+*+*+?` fires only at 02:00.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/components/next/quartz-component.html
