---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-local-execution
name: kubeflow-pipelines-local-execution
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [local-execution, kfp-local, dockerrunner, subprocessrunner]
level: practitioner
status: docs-checked
description: "Run KFP components and pipelines locally with kfp.local: local.init, SubprocessRunner and DockerRunner, and the limitations of local execution."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/execute-kfp-pipelines-locally.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines local execution

Local execution gives a fast development loop. Initialize a session, then call a component or pipeline like a normal function; outputs are materialized values rather than references.

```python
from kfp import local, dsl
local.init(runner=local.DockerRunner())

@dsl.component
def add(a: int, b: int) -> int:
    return a + b

task = add(a=1, b=2)
assert task.output == 3
```

Pipelines work too (`pipeline_task = math_pipeline(x=1, y=2, z=3)` then `pipeline_task.output`). Artifacts are readable: `task.outputs['out_artifact'].path` and `.metadata` after the run. `SubprocessRunner` runs components in a local subprocess; `DockerRunner` runs each in a container.

Limitations:
- No caching, retries or other production optimizations.
- Simple assumptions about resources; memory, CPU and affinity requests are not honored.
- No authentication; components touching cloud resources must be tested remotely.
- Sequential and nested pipelines are supported, but `dsl.Condition`, `dsl.ParallelFor` and `dsl.ExitHandler` are not yet.

By default an exception is raised if a task fails; `raise_on_error=False` in `local.init` changes that, and `pipeline_root` sets the local directory where outputs are written.

Runner choice: the docs strongly recommend `DockerRunner` (needs Docker installed, strongest isolation, runs all component types). `SubprocessRunner` is recommended only where Docker cannot be installed, such as some notebook environments; it runs only lightweight Python components and by default installs dependencies into a virtual environment (`use_venv=False` disables that).

Local execution is for testing logic, not cluster behavior.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Execute KFP pipelines locally" (content/en/docs/components/pipelines/user-guides/core-functions/execute-kfp-pipelines-locally.md, read in full). Rewrote the loose limitation wording ("task methods have no effect locally") only by tightening; nothing removed.

Method: docs-checked 2026-11-09 against the Kubeflow website local execution page (raw markdown, read in full).
