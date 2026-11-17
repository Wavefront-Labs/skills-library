---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-cli-run-pipeline
name: kubeflow-pipelines-cli-run-pipeline
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [kfp-cli, create-run-from-pipeline-func, run-pipeline, kfp-run-create, pipeline-upload]
level: practitioner
status: docs-checked
description: "Use the kfp CLI and SDK client to compile, build components and submit runs; plus the three ways to start a run (dashboard, SDK client, CLI)."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/cli.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/run-a-pipeline.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines cli run pipeline

The CLI is installed with the SDK (`pip install kfp`); check with `kfp --version`. Syntax: `kfp [OPTIONS] COMMAND [ARGS]`, for example `kfp --endpoint http://my_kfp_endpoint.com run list`; use `--help` on any command.

Resource commands take `<resource> <action>`: resources `run`, `recurring-run`, `pipeline`, `experiment`; actions `create`, `list`, `get`, `delete`. Extras: `archive` and `unarchive` (run, experiment), `enable` and `disable` (recurring-run), `create-version`, `list-versions`, `get-versions`, `delete-versions` (pipeline).

Compile: `kfp dsl compile --py path/to/pipeline.py --output out.yaml [--function my_pipeline] [--pipeline-parameters JSON]`. `--function` selects one pipeline or component in a file with several. `kfp component build` creates the image files for containerized Python components.

Ways to start a run:
1. **Dashboard**: Pipelines, Upload pipeline (yaml, zip or tar.gz), then Runs, Create run, choose the pipeline, Start.
2. **SDK client**: `kfp_client = kfp.Client()`, then `create_run_from_pipeline_package("./add-pipeline.yaml", arguments={"a": 1, "b": 2})` for compiled YAML or `create_run_from_pipeline_func(add_pipeline, arguments={...})` which compiles for you.
3. **CLI**: `kfp run create --experiment-name "my-experiment" --package-file "./path/to/pipeline.yaml"`.

For scheduled runs use Recurring Runs in the dashboard or API. The run guide covers only immediate runs. Building containerized components with `kfp component build` needs `pip install kfp[all]` for the Docker dependency.

## Checked

2026-11-09: every command, resource, action and example confirmed against the Kubeflow website pages "Use the KFP CLI" and "Run a Pipeline" (both read in full). Nothing removed.

Method: docs-checked 2026-11-09 against the Kubeflow website core-functions cli and run-a-pipeline pages (raw markdown, read in full).
