---
id: computing-software.devops-ci-cd.argo-workflows.node-field-selector
name: node-field-selector
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [node-field-selector, resume-stop-retry, restart-successful, display-name, node-phase]
level: practitioner
status: docs-checked
description: "Target specific nodes in argo resume, stop and retry with --node-field-selector fields and operators, including full-name disambiguation."
sources: ["https://argo-workflows.readthedocs.io/en/latest/node-field-selector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node field selectors
`argo resume`, `stop` and `retry` (and the matching API calls) accept `--node-field-selector=FIELD=VALUE` to act on a subset of nodes. For `retry` it picks nodes to restart even if they previously succeeded, and must be combined with `--restart-successful`.

Fields:
- `displayName`: name as shown in CLI or UI, without ancestors; a shortcut when only one node has it
- `id`: unique node ID, found in the workflow status
- `name`: full name including ancestors; needed when displayNames collide
- `templateName`
- `phase`, such as Running
- `templateRef.name` and `templateRef.template`
- `inputs.parameters.<NAME>.value`

Operators are `=` and `!=`. Join selectors with commas to AND them.

```bash
--node-field-selector=inputs.parameters.foo.value=bar
--node-field-selector=foo1=bar1,phase!=Running
```

Example problem: two nodes both display `wait-approval` (under `app1` and `app3`). Select one with the full name, `appr-promotion-ffsv4.app1.wait-approval`. When unsure of a full name, run `kubectl get wf NAME -o yaml` and read `status.nodes.<id>.name` (the display name is under `displayName`). In that status output a waiting node shows `type: Suspend` and `phase: Running`.

## Checked
2026-11-03. Confirmed against the Argo Workflows Node Field Selectors page: the field table, operators, comma AND, the retry and restart-successful rule and the two-node example. Removed an uncited tip on combining selectors.
Method: documentation only; no commands were run.
