---
id: computing-software.devops-ci-cd.flux.alert-event-filtering
name: alert-event-filtering
category: computing-software
field: devops-ci-cd
product: flux
tags: [alert, inclusionlist, exclusionlist, eventseverity, eventsources]
level: sme
status: docs-checked
description: "Cut alert noise with eventSeverity, inclusionList and exclusionList regexes, wildcard and label event sources."
sources:
  - https://fluxcd.io/flux/components/notification/alerts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alerts forward everything from the listed sources unless filtered.

Severity: `.spec.eventSeverity` unset or `info` forwards all events including errors. Use `error` to receive only errors.

Event sources can select one object by name, all objects of a kind via `name: '*'` (in a `namespace`), or objects by labels with `matchLabels`:

```yaml
eventSources:
  - kind: HelmRelease
    name: '*'
    namespace: apps
    matchLabels:
      team: app-dev
```

Message filters use Go regular expressions:
- `.spec.exclusionList`: drop an event if its message matches any expression.
- `.spec.inclusionList`: send only events matching at least one expression.
- If both match, the event is discarded: exclusion is stronger.

Skip transient Git clone socket errors:

```yaml
spec:
  eventSources:
    - kind: GitRepository
      name: '*'
  exclusionList:
    - "waiting.*socket"
```

Alert on successful Helm installs, upgrades and rollbacks but not uninstalls or tests:

```yaml
spec:
  eventSources:
    - kind: HelmRelease
      name: '*'
  inclusionList:
    - ".*succeeded.*"
  exclusionList:
    - ".*uninstall.*"
    - ".*test.*"
```

Event metadata has three sources, lowest to highest precedence: annotations on Flux objects with the `event.toolkit.fluxcd.io/` prefix, then the Alert `.spec.eventMetadata`, then controller-defined metadata. On a key conflict the higher source wins and a warning log and Kubernetes event are emitted.

## Checked

2026-11-08. Read in full: https://github.com/fluxcd/notification-controller/blob/main/docs/spec/v1/alerts.md.

Removed or corrected: the advice to test regexes with flux events, which is not on the page.

Method: documentation only; no commands were run.
