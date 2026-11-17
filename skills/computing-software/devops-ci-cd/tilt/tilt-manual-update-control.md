---
id: computing-software.devops-ci-cd.tilt.tilt-manual-update-control
name: tilt-manual-update-control
category: computing-software
field: devops-ci-cd
product: tilt
tags: [manual-update-control, tilt]
level: practitioner
status: docs-checked
description: "Switch Tilt resources from auto-update to manual with trigger_mode and combine it with auto_init to control when each resource runs."
sources:
  - "https://docs.tilt.dev/manual_update_control.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual update control

Goal: stop Tilt from rebuilding/redeploying a resource on every file change, and run updates only when you click a button.

By default (`TriggerMode: Auto`) Tilt triggers an update whenever it detects a change affecting a resource. With `TriggerMode: Manual`, Tilt still monitors file changes but only indicates in the UI that files changed and gives you a button to kick off the update. Useful when an update is slow, or when checking out a branch would cause many spurious updates.

## Setting the trigger mode

1. Per resource: `k8s_resource()`, `local_resource()`, and `dc_resource()` take an optional `trigger_mode` arg, either `TRIGGER_MODE_AUTO` or `TRIGGER_MODE_MANUAL`.
2. For all resources: call top-level `trigger_mode()` with one of those constants to set the default; per-resource calls can still override.

```python
# TriggerMode = Manual
k8s_resource('snack', trigger_mode=TRIGGER_MODE_MANUAL)
```

```python
trigger_mode(TRIGGER_MODE_MANUAL)
# TriggerMode = Manual (default set above)
k8s_resource('snack')

# TriggerMode = Auto (override for a specific resource)
k8s_resource('bar', trigger_mode=TRIGGER_MODE_AUTO)
```

With manual mode, unapplied changes are shown by an asterisk to the right of the resource in the sidebar; Tilt waits until you click the apply button to its left.

## Combining with auto_init

`auto_init` on `k8s_resource()`, `local_resource()` and `dc_resource()` gives finer control:

- Run only when explicitly triggered from the UI: `auto_init=False` and `trigger_mode=TRIGGER_MODE_MANUAL`. It will not run on start nor when files change.
- Not run at start, but run whenever a file dependency changes: `auto_init=False` and `trigger_mode=TRIGGER_MODE_AUTO`. Useful for linting or running tests automatically.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Manual Update Control page in full (intro, Using TriggerMode, Auto Init). Confirmed the trigger modes, the per-resource `trigger_mode` argument, the top-level `trigger_mode()` default and override, the asterisk and apply button, and both `auto_init` combinations. Nothing removed. 

Method: documentation only; no commands were run.
