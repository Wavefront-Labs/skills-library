---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-trigger-conditions-reset
name: argo-events-sensor-trigger-conditions-reset
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, conditions-reset, cron, timezone, trigger, stale-events]
level: advanced
status: docs-checked
description: "Prevent stale partial matches by scheduling a conditionsReset by cron so yesterday's A cannot combine with tomorrow's B."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/trigger-conditions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor trigger conditions reset

When a trigger depends on several events, a partial match can sit around. Example: conditions `A && B` where both are expected daily; one day A arrives but B does not, and the next day B arrives, so today's A and tomorrow's B fire the action, which you may not want. `conditionsReset` clears the recorded state of all dependencies in the conditions on a schedule:

```yaml
spec:
  triggers:
    - template:
        name: trigger01
        conditions: "dep01 && dep02"
        conditionsReset:
          - byTime:
              # reset conditions at 23:59
              cron: "59 23 * * *"
              # optional, defaults to UTC
              timezone: America/Los_Angeles
```

`byTime.cron` is a cron expression and `timezone` is optional and defaults to UTC; the page links the tz database list of time zone names. The Trigger Conditions page is marked v1.0 and after.

## Checked

2026-11-04. Confirmed against the Trigger Conditions page, Conditions Reset section: the `A && B` daily scenario, the `conditionsReset` `byTime` YAML with `cron` and `timezone`, the UTC default and the v1.0 marker. Removed the closing design note about choosing a reset time, which the page does not give, and reworded the timezone description to the page's link to the tz database list.
Method: documentation only; no commands were run.
