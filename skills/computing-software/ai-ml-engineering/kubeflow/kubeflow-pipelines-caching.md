---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-caching
name: kubeflow-pipelines-caching
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [caching, set-caching-options, enable-caching, execution-caching]
level: practitioner
status: docs-checked
description: "Control Kubeflow Pipelines execution caching per task with set_caching_options, per run with enable_caching, and by default with a compile flag or environment variable."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/caching.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines caching

KFP caches a component's outputs and reuses them when the component runs again with the same inputs and parameters and the output is still available. Cached tasks show a green arrow-from-cloud icon in the UI. Caching is on by default for all components.

Disable for one task inside the pipeline:

```python
hello_task = say_hello(name=recipient)
hello_task.set_caching_options(False)
```

Override for a whole run at submission; this overrides all task settings:

```python
client.create_run_from_pipeline_func(hello_pipeline, enable_caching=True)
```

Change the default at compile time, so tasks are uncached unless enabled:
- CLI flag: `kfp dsl compile --py my_pipeline.py --output my_pipeline.yaml --disable-execution-caching-by-default`
- Environment variable: `KFP_DISABLE_EXECUTION_CACHING_BY_DEFAULT=true` (any truthy value), which also applies to `Compiler().compile()`.

The page's example: with the variable set to true and `task_1.set_caching_options(False)` in the pipeline, running the file leaves `task_2` with caching disabled. When the variable is false or absent, caching stays enabled by default.

Gotcha: Python reads configuration during import, so set the environment variable before importing pipeline components, not after.

## Checked

2026-11-08. Confirmed against the Use Caching page: default on, per-task call, run-level override, compile flag, environment variable behaviour and the import-order note. Replaced an unsupported precedence claim with the page's own example.
Method: docs-only read of cited pages, 2026-11-08
