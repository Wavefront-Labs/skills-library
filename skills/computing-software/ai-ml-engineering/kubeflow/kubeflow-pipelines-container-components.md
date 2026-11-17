---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-container-components
name: kubeflow-pipelines-container-components
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [container-components, containerspec, container-component, outputpath]
level: practitioner
status: docs-checked
description: "Write Kubeflow Pipelines container components with dsl.container_component and ContainerSpec: image, command, args, inputs and OutputPath outputs."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/components/container-components.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines container components

Every KFP task is a container execution defined by `image`, `command` and `args`. Python components hide this; container components expose it, so you can run shell tools or arbitrary images.

```python
from kfp import dsl

@dsl.container_component
def say_hello(name: str):
    return dsl.ContainerSpec(image='alpine', command=['echo'], args=[f'Hello, {name}!'])
```

Use the `dsl.container_component` decorator on a function that returns a `dsl.ContainerSpec`. The function parameters and annotations define the component interface. At compile time `name` becomes a placeholder replaced with the real value at runtime. Use them in a pipeline like any other component and compile with `compiler.Compiler().compile(hello_pipeline, 'pipeline.yaml')`.

Passing the value as an argument to `sh -c` is more flexible than interpolating into the command string:

```python
return dsl.ContainerSpec(image='alpine', command=['sh', '-c', 'echo Hello, $0!'], args=[name])
```

Containers have no standard way to return values, so outputs go through files. Declare an output parameter with `dsl.OutputPath(str)`:

```python
@dsl.container_component
def say_hello(name: str, greeting: dsl.OutputPath(str)):
    ...
```

At runtime KFP passes a system-generated path for each `dsl.OutputPath` parameter; your container logic writes the output value to that path as JSON, and KFP reads the file and persists the output. Pass the path in `args` (for example `args=[name, greeting]` with `sh -c`) and create its parent directory first (the docs example uses `mkdir -p $(dirname $1)`). Never provide output parameters when calling the component in a pipeline; read them with `task.outputs['greeting']` rather than `task.output`.

Two placeholders are available only in the `ContainerSpec` of a `@dsl.container_component`:

- `dsl.ConcatPlaceholder(items)` concatenates strings, upstream outputs and parameters without a separator (list elements are otherwise joined by a space).
- `dsl.IfPresentPlaceholder(input_name=..., then=[...], else_=[...])` conditionally supplies arguments depending on whether an optional input was passed; `else_` is optional.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Container Components" (content/en/docs/components/pipelines/user-guides/components/container-components.md, read in full). Removed the unconfirmed statement about input deserialization.

Method: docs-checked 2026-11-09 against the Kubeflow website container-components page (raw markdown, read in full).
