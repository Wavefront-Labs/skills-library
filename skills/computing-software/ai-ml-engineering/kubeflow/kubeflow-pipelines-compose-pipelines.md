---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-compose-pipelines
name: kubeflow-pipelines-compose-pipelines
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [pipeline-decorator, dsl-pipeline, pipelinetask, data-passing, compose-pipeline]
level: practitioner
status: docs-checked
description: "Compose components into a KFP pipeline with @dsl.pipeline: decorator arguments, inputs and outputs, PipelineTask.output and task dependencies."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/components/compose-components-into-pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines compose pipelines

A pipeline is a Python function decorated with `@dsl.pipeline`. It looks like Python but expresses topology and control flow when compiled.

```python
@dsl.pipeline
def pythagorean(a: float, b: float) -> float:
    a_sq = square(x=a)
    b_sq = square(x=b)
    s = add(x=a_sq.output, y=b_sq.output)
    return square_root(x=s.output).output
```

Four parts: the decorator, inputs and outputs in the signature, data passing and dependencies, and task configuration (plus control flow).

Decorator arguments: `name` (defaults to a sanitized function name), `description`, `pipeline_root` (remote storage root for task outputs; can be overridden at submission) and `display_name`.

Inputs are function parameters with type annotations; outputs are declared with return annotations and are never pipeline parameters. See the data types guide for details.

Calling a component inside a pipeline builds a `PipelineTask`. Pass data with `.output` for a single unnamed output, or `.outputs['name']` for several or named outputs. Passing one task's output as another's input creates the dependency edge, so tasks with no data link can run in parallel. To order tasks that exchange no data, call `b_task.after(a_task)`.

Task configuration uses chainable `PipelineTask` methods, for example `task.set_env_variable('MY_ENV_VAR', 'hello')`. The docs list `.add_accelerator_type`, `.set_accelerator_limit`, `.set_cpu_limit`, `.set_memory_limit`, `.set_env_variable`, `.set_caching_options`, `.set_display_name`, `.set_retry` and `.ignore_upstream_failure`; the docs flag `.ignore_upstream_failure` as unsupported by the open source backend.

Pipelines can be used as components inside other pipelines, like any single-step component.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Compose components into pipelines" (content/en/docs/components/pipelines/user-guides/components/compose-components-into-pipelines.md, read in full). Nothing removed.

Method: docs-checked 2026-11-09 against the Kubeflow website compose-components-into-pipelines page (raw markdown, read in full).
