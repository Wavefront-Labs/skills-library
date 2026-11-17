---
id: computing-software.cloud-infrastructure-engineering.keda.cloudevent-types-and-filters
name: cloudevent-types-and-filters
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [includedeventtypes, excludedeventtypes, keda-scaledobject-failed, event-filter, cloudevent-types]
level: advanced
status: docs-checked
description: "Filter KEDA CloudEvents with includedEventTypes and excludedEventTypes and recognise the event types for ScaledObjects, ScaledJobs and authentication resources."
sources:
  - https://keda.sh/docs/2.17/operate/cloud-events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each emitted event has a GUID `id`, a `time` stamp and `datacontenttype` set to `application/json`. Filters are given per CloudEventSource under `eventSubscription`, and the page describes them as defining which event types you are interested in or want to ignore for a given sink. Every listed type carries a version suffix, `.v1`, so write the strings exactly as in the list below.
The optional `eventSubscription` section filters which event types are emitted:

```yaml
eventSubscription:
  includedEventTypes:
  - keda.scaledobject.failed.v1
  excludedEventTypes:
  - keda.scaledobject.ready.v1
```

Only types in `includedEventTypes` are emitted; types in `excludedEventTypes` are suppressed.

Supported event types and when they fire:
- `keda.scaledobject.ready.v1`: the first time a ScaledObject is ready, or when its previous ready condition was `Unknown` or `False`.
- `keda.scaledobject.failed.v1`: validation of a ScaledObject fails.
- `keda.scaledobject.removed.v1`: a ScaledObject is deleted.
- `keda.scaledjob.ready.v1`, `keda.scaledjob.failed.v1`, `keda.scaledjob.removed.v1`: the same three situations for ScaledJobs.
- `keda.authentication.triggerauthentication.created.v1`, `.updated.v1`, `.removed.v1`: lifecycle of a TriggerAuthentication.
- `keda.authentication.clustertriggerauthentication.created.v1`, `.updated.v1`, `.removed.v1`: lifecycle of a ClusterTriggerAuthentication.

## Checked

2026-11-03. Confirmed on the 2.17 CloudEvent Support page: event list, includedEventTypes and excludedEventTypes. Removed: the claim that every event is emitted by default.

Method: documentation only; no commands were run.
