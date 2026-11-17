---
id: computing-software.devops-ci-cd.argo-workflows.conditional-outputs
name: conditional-outputs
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [conditional-outputs, from-expression, value-from-expression, conditional-artifacts, ternary-expression]
level: advanced
status: docs-checked
description: "Select Step or DAG level output artifacts and parameters from branches with fromExpression and valueFrom.expression, including the ternary pattern."
sources: ["https://argo-workflows.readthedocs.io/en/latest/conditional-artifacts-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional artifacts and parameters
A Steps or DAG template can expose an output chosen by an expression, useful after `when` branches where only one branch ran.

Artifacts use `fromExpression` under the template's `outputs.artifacts`:

```yaml
outputs:
  artifacts:
    - name: result
      fromExpression: "steps['flip-coin'].outputs.result == 'heads' ? steps.heads.outputs.artifacts.headsresult : steps.tails.outputs.artifacts.tailsresult"
```

Parameters use `valueFrom.expression` under `outputs.parameters`:

```yaml
outputs:
  parameters:
    - name: stepresult
      valueFrom:
        expression: "steps['flip-coin'].outputs.result == 'heads' ? steps.heads.outputs.result : steps.tails.outputs.result"
```

The two branches in the example are steps guarded by `when: "{{steps.flip-coin.outputs.result}} == heads"` (and `tails`). The examples write `steps['flip-coin']` in bracket form and pick the branch with a ternary `cond ? a : b`.

The page links Steps and DAG variants for both artifacts and parameters, plus an advanced fibonacci sequence example.

## Checked
2026-11-03. Confirmed against the Argo Workflows Conditional Artifacts and Parameters page: `fromExpression` for artifacts, `valueFrom.expression` for parameters, both example expressions and the `when` guards. Removed uncited claims about why brackets are needed, the expression engine, and example file names.
Method: documentation only; no commands were run.
