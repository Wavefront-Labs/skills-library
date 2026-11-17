---
id: computing-software.ai-ml-engineering.kserve.kserve-runtime-auto-selection-priority
name: kserve-runtime-auto-selection-priority
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [autoselect, priority, runtime-selection, protocolversion, protocolversions, supportedmodelformats, creationtimestamp]
level: advanced
status: docs-checked
description: "How KServe auto-selects a runtime when none is named: autoSelect, version match, protocolVersion and priority rules, and the creationTimestamp fallback hazard."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/resources/servingruntime.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Runtime auto-selection and priority

With no `runtime:` in the predictor, the controller considers runtimes whose `supportedModelFormats` entry has the same `name` and `autoSelect: true`. If the InferenceService gives `modelFormat.version`, the runtime's version must match; `kserve-sklearnserver` lists sklearn "1", so a request for version "0" excludes it.

When several runtimes match name, version and `protocolVersion`, use `priority`:

```yaml
# ClusterServingRuntime kserve-sklearnserver
spec:
  protocolVersions: [v1, v2]
  supportedModelFormats:
    - {name: sklearn, version: "1", autoSelect: true, priority: 1}
---
# ClusterServingRuntime mlserver
spec:
  protocolVersions: [v2]
  supportedModelFormats:
    - {name: sklearn, version: "1", autoSelect: true, priority: 2}
```

An InferenceService with `model.protocolVersion: v2` and `modelFormat.name: sklearn` picks `mlserver` (higher value wins).

## Constraints
- Value must be greater than 0; higher means higher precedence.
- Only honoured when `autoSelect` is true.
- A runtime with a priority beats one without.
- Two entries with the same format name and version cannot share a priority.
- If a runtime lists several versions of a format, they must carry the same priority.
- Naming the runtime explicitly overrides priority.

## Gotcha
If several runtimes qualify and none has a priority, the most recently created one (`creationTimestamp`) wins, so the result is not guaranteed. Enable `autoSelect` sparingly.

## Checked

Checked 2026-11-08 against the KServe website page servingruntime.md, read in full: autoSelect and version matching, the kserve-sklearnserver example, the priority rules and constraints, the explicit-runtime override and the creationTimestamp warning. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
