---
id: computing-software.devops-ci-cd.helm.hook-weights-and-delete-policies
name: hook-weights-and-delete-policies
category: computing-software
field: devops-ci-cd
product: helm
tags: [hook-weight, hook-delete-policy, before-hook-creation, hook-succeeded, hook-failed, hooks, ordering]
level: advanced
status: docs-checked
description: "Order hooks with helm.sh/hook-weight and clean them up with helm.sh/hook-delete-policy values."
sources:
  - "https://helm.sh/docs/topics/charts_hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When several hooks share an event, `helm.sh/hook-weight` orders them. The weight must be a string, can be positive, zero or negative, and hooks sort ascending; ties are broken by resource kind, then by name.

```yaml
annotations:
  "helm.sh/hook": pre-install
  "helm.sh/hook-weight": "5"
  "helm.sh/hook-delete-policy": hook-succeeded
```

`helm.sh/hook-delete-policy` decides when a hook resource is removed. Values:

- `before-hook-creation`: delete the previous resource before a new hook is launched. This is the default if no policy is given.
- `hook-succeeded`: delete after the hook runs successfully.
- `hook-failed`: delete if the hook fails during execution.

Several policies may be listed comma-separated.

Gotchas:

- Weights are strings, so quote them: `"-5"`, `"10"`.
- Helm sorts hooks by weight (default 0), then by resource kind, then by name, ascending, and loads the lowest weight first. From Helm 3.2.0, hook resources with the same weight are installed in the same order as normal non-hook resources. The guide advises always setting a weight, using `0` if it does not matter.
- Hook resources are not tracked as part of the release. The guide says any hook resource that must never be deleted should be annotated `helm.sh/resource-policy: keep`; the alternatives for removing them are a delete policy or a Job TTL.

## Checked

2026-11-08. Read the Chart Hooks page in full. Confirmed weights as strings, ascending sort by weight/kind/name and the three delete-policy values with before-hook-creation as default. Removed unsupported gotchas (name-conflict, generateName, hook-failed advice, resource-policy on uninstall); added the 3.2.0 same-weight ordering note.

Method: documentation only; no commands were run.
