---
id: computing-software.cloud-infrastructure-engineering.crossplane.pt-readiness-checks
name: pt-readiness-checks
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function-patch-and-transform, readiness, readinesschecks, matchstring]
level: practitioner
status: docs-checked
description: "Override when function-patch-and-transform considers a composed resource Ready with readinessChecks."
sources:
  - https://docs.crossplane.io/latest/guides/function-patch-and-transform/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a composed resource is ready when its status shows `Type: Ready`, `Status: True`. Resources without a status, such as a ProviderConfig, are never ready by default. Add `readinessChecks` to a resource; use several checks if a resource must meet several conditions.

```yaml
readinessChecks:
- type: MatchString
  fieldPath: status.atProvider.state
  matchString: "Online"
```

Types:

- `MatchString`: exact string (no substrings or regex), field `matchString`.
- `MatchInteger`: field `matchInteger`, for example `4`. Matching 0 is not supported.
- `NonEmpty`: the field exists with a non-empty value.
- `None`: always ready.
- `MatchCondition`: `matchCondition` with `type` and `status`, for example `MyType` and `Success`, in `status.conditions`.
- `MatchTrue` / `MatchFalse`: a boolean field, for example `status.atProvider.manifest.status.ready`.

Checks have a `type` and a `fieldPath`; the page's `None` and `MatchCondition` examples omit `fieldPath`.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Function Patch and Transform guide, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the claim that a failing check names the resource in the Ready message, an unsourced MatchCondition example and advice on None.

Method: documentation only; no commands were run.
