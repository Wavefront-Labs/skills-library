---
id: computing-software.cloud-infrastructure-engineering.alertmanager.template-alert-and-kv
name: template-alert-and-kv
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, templating, alert-object, kv-methods, sortedpairs]
level: practitioner
status: docs-checked
description: "The Alert object and KV type in Alertmanager templates: Status, Labels, StartsAt, EndsAt, Fingerprint and SortedPairs, Remove, Names, Values."
sources: ["https://prometheus.io/docs/alerting/latest/notifications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alert and KV in templates

Alert holds one alert for notification templates:

- `Status`: whether the alert is resolved or currently firing.
- `Labels`: KV of labels.
- `Annotations`: KV of annotations.
- `StartsAt` (`time.Time`): when the alert started firing. If omitted, the current time is assigned by Alertmanager.
- `EndsAt` (`time.Time`): only set if the end time is known; otherwise set to a configurable timeout period from the last time the alert was received.
- `GeneratorURL`: a backlink identifying the causing entity.
- `Fingerprint`: identifies the alert.

KV is a set of key/value string pairs representing labels and annotations: `type KV map[string]string`. Direct access works, for example `.Annotations.summary`. Methods:

| Method | Arguments | Returns |
|---|---|---|
| SortedPairs | none | sorted list of key/value pairs |
| Remove | []string | copy of the map without the given keys |
| Names | none | the label names in the LabelSet |
| Values | none | the values in the LabelSet |

## Checked

2026-11-03. Confirmed against the Notification template reference: Alert fields and KV methods. Removed: the range/Remove example (not on the page and its argument order was wrong).

Method: documentation only; no commands were run.
