---
id: computing-software.cloud-infrastructure-engineering.crossplane.xr-annotations-pause-poll
name: xr-annotations-pause-poll
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [composite-resource, annotation, pause, poll-interval, reconcile]
level: practitioner
status: docs-checked
description: "Pause an XR, override its poll interval, or force reconciliation with crossplane.io annotations, and read its conditions."
sources:
  - https://docs.crossplane.io/latest/composition/composite-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three annotations control a composite resource:

```yaml
metadata:
  annotations:
    crossplane.io/paused: "true"
    crossplane.io/poll-interval: "24h"
    crossplane.io/reconcile-requested-at: "2024-01-15T10:30:00Z"
```

- `crossplane.io/paused: "true"` stops Crossplane checking or changing the XR's external resources.
- `crossplane.io/poll-interval` overrides the global `--poll-interval` for this XR. It takes any Go duration string.
- `crossplane.io/reconcile-requested-at` triggers an immediate reconcile whenever its value changes; any string such as a timestamp works. The handled token is recorded in `status.lastHandledReconcileAt`.

An XR has two conditions. `Synced` is True when Crossplane can reconcile it, otherwise it carries the error. `Ready` is True when the function pipeline reports all composed resources ready; otherwise it names the resource that is not.

List XRs with `kubectl get composite`, or only one kind with `kubectl get <plural>`.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Composite Resources page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the resume-by-other-value claim, the kubectl annotate example and poll-interval advice.

Method: documentation only; no commands were run.
