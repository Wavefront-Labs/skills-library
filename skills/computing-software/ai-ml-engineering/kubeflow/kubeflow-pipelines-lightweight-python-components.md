---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-lightweight-python-components
name: kubeflow-pipelines-lightweight-python-components
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [lightweight-python-components, dsl-component, packages-to-install, hermetic, base-image]
level: practitioner
status: docs-checked
description: "Author Lightweight Python Components with @dsl.component: type annotation and hermetic rules, packages_to_install, pip_index_urls, base_image, additional_funcs and more."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/components/lightweight-python-components.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines lightweight python components

A Lightweight Python Component is a Python function decorated with `@dsl.component`; KFP extracts the source and runs it in a container.

Function requirements:
1. **Type annotations** on all inputs and outputs. Parameters: `int`, `float`, `str`, `bool`, `typing.Dict`, `typing.List`. Artifacts use artifact annotations.
2. **Hermetic**: no references to symbols outside the body. Constants and imports must be defined inside the function; a module-level constant fails at runtime.

Decorator arguments:
- `packages_to_install`: pip requirements installed at runtime, like a requirements file. As a production best practice the docs prefer Containerized Python Components, which eliminate installing dependencies at runtime.
- `pip_index_urls`: alternative package indices, passed as `--index-url` and `--extra-index-url` with trusted hosts. PyPI is not added automatically; list it yourself if you also need public packages.
- `base_image`: container image to run on (the docs page names `python:3.7` as the default, so check the SDK version you use; override with, for example, `base_image='python:3.8'`).
- `install_kfp_package`: KFP is installed at runtime so symbols such as artifact annotations exist; setting this to `False` is rarely needed and discouraged. Pair with `pip_index_urls` for control.
- `additional_funcs`: helper functions copied into the component and callable from the main function, useful for shared utilities that are not an importable package.
- `embedded_artifact_path`: embeds a local file or directory; at runtime it is extracted to a temp directory exposed through a `dsl.EmbeddedInput[T]` parameter, with the extraction root added to `sys.path`.
- `task_config_passthroughs`: passes task configuration (resources, env, volumes) through with `dsl.TaskConfig`, useful when the component launches another resource such as a Kubeflow Trainer job.

Hermeticism is limiting for real code; use Containerized Python Components when it hurts.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Lightweight Python Components" (content/en/docs/components/pipelines/user-guides/components/lightweight-python-components.md, read in full). Reworded the production-install note and the base image default to match the page.

Method: docs-checked 2026-11-09 against the Kubeflow website lightweight-python-components page (raw markdown, read in full).
