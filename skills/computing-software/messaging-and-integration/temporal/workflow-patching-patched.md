---
id: computing-software.messaging-and-integration.temporal.workflow-patching-patched
name: workflow-patching-patched
category: computing-software
field: messaging-and-integration
product: temporal
tags: [patching, patched, workflow-versioning, replay, marker, non-determinism, version-branch]
level: practitioner
status: docs-checked
description: "How the patched() API behaves in Temporal Python, .NET and Ruby: markers, replay cases, why the newest branch must come first, and unexpected false returns."
sources:
  - https://docs.temporal.io/patching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A patch is a named logical branch, like a feature flag, that applies a change to new executions without disrupting running ones. This describes `patched()` in the Python, .NET and Ruby SDKs.

Not replaying: if the patch ID is not in history, the call adds a marker, upserts a search attribute and returns `true` (first block of that ID); if the ID is already present it leaves history alone and returns `true`.

Replaying:
- Marker at the same place: writes the marker to the replay history and returns `true`. A marker earlier in history returns `true` without changes.
- Marker only later in history (the patch is placed too early): a non-deterministic exception, because histories do not match.
- No marker for that ID: returns `false`, adds nothing, and every later call with that ID also returns `false`, even once replay ends and new code runs.

Implication: the history after the current position matters, and a workflow does not always run the newest code. Executions that replay past a deployment follow old code at every `patched()` that lacks a marker, which keeps dependent patched code consistent.

Rule: put the newest version first:
```python
if patched('v3'):
    ...  # newest
elif patched('v2'):
    ...
else:
    ...  # original
```
If `v2` is tested first, fresh executions evaluate `patched('v2')` as `true` (not replaying), write its marker, and never reach `v3`.

## Checked

2026-11-08. Read in full: the Patching page (docs.temporal.io/patching). Every remaining claim matches those pages. Removed: the closing Worker Versioning recommendation, which the page does not state.

Method: documentation only; no commands were run.
