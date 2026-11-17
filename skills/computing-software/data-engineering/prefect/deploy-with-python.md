---
id: computing-software.data-engineering.prefect.deploy-with-python
name: deploy-with-python
category: computing-software
field: data-engineering
product: prefect
tags: [deploy, serve, from-source, work-pool, docker-image]
level: practitioner
status: docs-checked
description: "Create Prefect deployments in Python with flow.deploy, from_source and the multi-flow deploy function, with image, push and schedule arguments."
sources:
  - https://docs.prefect.io/v3/how-to-guides/deployments/deploy-via-python
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deploy a flow to a work pool from Python.

`flow.deploy` creates a deployment using dynamic infrastructure through a work pool. `flow.serve` suits static, always-available infrastructure.

```python
if __name__ == "__main__":
    my_flow.deploy(name="my-deployment", work_pool_name="my-work-pool",
                   image="my-registry.com/my-docker-image:my-tag", push=False)
```

Running the script builds an image with your code and dependencies, then creates the deployment. Start a worker and trigger:

```bash
prefect worker start --pool my-work-pool
prefect deployment run 'my-flow/my-deployment'
```

Arguments:
- `name`, `work_pool_name`
- `image`: a reference string or a `DockerImage` object for your own Dockerfile
- `build=False`: reuse an existing image
- `push=False`: skip pushing to a registry
- `parameters`: default flow parameters
- `job_variables`: override work pool defaults such as environment variables
- schedules: `interval` (seconds or `timedelta`), `cron` (`"0 0 * * *"`), `rrule`, or a `schedules` list

Remote code: `flow.from_source(source=..., entrypoint=...).deploy(...)` loads from Git, `s3://`, `gs://` or `az://`. `entrypoint` is `path/to/flow.py:func` or a module path.

Several flows: the top-level `deploy(...)` function, with `flow.to_deployment("name")` for per-deployment settings; shared `image`, `push` and `work_pool_name` apply to all and a single image is built.

Prerequisites: a running server or Cloud workspace, a work pool (a Docker pool in the guide) and Docker.

## Checked

2026-11-09. Read the whole deploy-via-python page. Confirmed every command, argument, schedule option, remote-source scheme and multi-flow behaviour above. Removed nothing.

Method: documentation only; no commands were run.
