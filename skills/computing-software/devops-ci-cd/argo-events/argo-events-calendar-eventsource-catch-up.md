---
id: computing-software.devops-ci-cd.argo-events.argo-events-calendar-eventsource-catch-up
name: argo-events-calendar-eventsource-catch-up
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, calendar, catch-up, persistence, configmap, schedule, rbac]
level: advanced
status: docs-checked
description: "Make Calendar EventSources run missed schedules after a restart using persistence.catchup with a ConfigMap and a service account that can edit it."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/calendar-catch-up.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events calendar eventsource catch up

Catch-up lets a Calendar EventSource execute schedules missed since the last run. Configure it per event:

```yaml
spec:
  template:
    serviceAccountName: configmap-sa
  calendar:
    example-with-catch-up:
      schedule: "* * * * *"
      persistence:
        catchup:
          enabled: true
          maxDuration: 5m
        configMap:
          createIfNotExist: true
          name: test-configmap
```

On every start it checks for missed schedules since the last persisted event time, going back at most `maxDuration`. The last successful event timestamp is stored in the ConfigMap under a key like `calendar.example-with-catch-up` as JSON (`{"eventTime": "..."}`); one ConfigMap can serve several events.

RBAC: the service account needs a Role on `configmaps` with `get`, `create` and `update` when `createIfNotExist: true`; if the ConfigMap already exists, `create` can be dropped. To disable, set `catchup.enabled: false`.

Persisted state example: the ConfigMap stores each event's last time as a JSON string such as `{"eventTime":"2020-10-19 22:50:00.0003192 +0000 UTC m=+683.567066901"}`.

## Checked

2026-11-04. Confirmed against the Calendar EventSource Catch Up page: the YAML (`serviceAccountName`, `persistence.catchup.enabled`, `maxDuration`, `configMap.createIfNotExist`, `name`), the ConfigMap data key and JSON, the Role (`configmaps` with get, create, update; `create` removable if the ConfigMap exists) and disabling with `enabled: false`. Removed the claim that catch-up is off by default and the description of replay after a pod restart, which the page does not state.
Method: documentation only; no commands were run.
