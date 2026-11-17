---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-control-flow
name: kubeflow-pipelines-control-flow
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [control-flow, dsl-if, conditions, oneof, parallelfor]
level: practitioner
status: docs-checked
description: "Control flow in KFP pipelines: dsl.If, Elif and Else conditions, OneOf, loops and exit handling."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/control-flow.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/execute-kfp-pipelines-locally.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines control flow

KFP pipeline functions describe topology, so control flow uses DSL context managers. The core types are conditions, loops and exit handling.

Conditions: `dsl.If(condition)` runs the tasks in its scope based on an upstream task output or pipeline input. The condition needs at least one operand that is a task output or pipeline parameter. `dsl.Condition` is deprecated in favor of the identical `dsl.If`.

```python
@dsl.pipeline
def my_pipeline():
    coin = flip_three_sided_coin()
    with dsl.If(coin.output == 'heads'):
        print_comp(text='Got heads!')
    with dsl.Elif(coin.output == 'tails'):
        print_comp(text='Got tails!')
    with dsl.Else():
        print_comp(text='Draw!')
```

`dsl.Elif` and `dsl.Else` must come immediately downstream of `dsl.If`.

`dsl.OneOf` gathers outputs from mutually exclusive branches into a single value that downstream tasks or the pipeline output can consume. The compiler requires it to consume tasks from one logically associated group of conditional branches, one of which is a `dsl.Else`. The outputs must be the same type and cannot be other `dsl.OneOf` or `dsl.Collected` values.

Loops: `dsl.ParallelFor(items=..., name=..., parallelism=...)` runs tasks over a static set of items. `parallelism` is the maximum number of concurrent iterations, and `0` means unconstrained. `dsl.Collected(task.outputs['x'])` gathers loop outputs for a downstream task (input typed as a `List`) or for the pipeline return. Output parameters from nested loops come back as nested lists, while artifacts from nested loops come back as a flat list.

Exit handling: `with dsl.ExitHandler(exit_task=cleanup_task):` runs the exit task after the tasks in scope finish, even if one fails, like `try`/`finally`. An exit task can take a parameter annotated `dsl.PipelineTaskFinalStatus`, which the backend fills in; do not pass it yourself. The alternative `.ignore_upstream_failure()` on a task makes it run despite upstream failures; its component needs default values for every input it takes from upstream tasks.

Local execution does not yet support `dsl.Condition`, `dsl.ParallelFor` or `dsl.ExitHandler`, so test these on a cluster.

## Checked

2026-11-09: confirmed against the Kubeflow website pages "Control Flow" (content/en/docs/components/pipelines/user-guides/core-functions/control-flow.md, read in full) and "Execute KFP pipelines locally" (limitations section). Added the second page to sources because the local execution limitation comes from it.

Method: docs-checked 2026-11-09 against the Kubeflow website control-flow and local-execution pages (raw markdown).
