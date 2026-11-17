---
id: computing-software.data-engineering.prefect.flow-code-storage
name: flow-code-storage
category: computing-software
field: data-engineering
product: prefect
tags: [storage, git-clone, from-source, blob-storage, docker-image]
level: practitioner
status: docs-checked
description: "Where Prefect deployments fetch flow code: git, blob storage or baked images, pull steps, credentials and dependency auto-install conditions."
sources:
  - https://docs.prefect.io/v3/how-to-guides/deployments/store-flow-code
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose where flow code lives and let workers fetch it.

Options: local filesystem (Process pools or a local directory), Git (GitHub, GitLab, Bitbucket), fsspec blob storage (S3, Azure Blob, GCS), or a Docker image with code baked in (all pools except Process and Prefect Managed).

Python: `flow.from_source(source=..., entrypoint=...).deploy(...)`; `source` is a path, git URL or storage object (`GitRepository`, `S3Bucket`). In `prefect.yaml` use a `pull` section. Either yields pull steps the worker runs before a flow run.

Pull steps: `prefect.deployments.steps.set_working_directory` (`directory`), `git_clone` (`repository`, `credentials` or `access_token`), `pull_from_blob_storage` (`container`, `folder`), plus `prefect_aws`, `prefect_azure`, `prefect_gcp` equivalents.

Git: public repos take the URL. `GitRepository(url=..., credentials=GitHubCredentials.load(...))` or `credentials={"access_token": Secret.load(...)}`; `branch` defaults to `"main"`. Install `prefect-github`, `prefect-bitbucket` or `prefect-gitlab`. Bitbucket tokens are prefixed `x-token-auth:`; GitLab needs `read_repository` and `api` scopes. Prefect does not push code to your git host.

Docker: `image=` with `deploy()` and `push=True`; without an image the base image such as `prefecthq/prefect:3-latest` is used.

Auto-installing dependencies needs all of: `PREFECT_RUNNER_AUTO_INSTALL_DEPENDENCIES=true`, `pyproject.toml` at the project root, `prefect` in `[project] dependencies`, and `uv` on `PATH`; otherwise it silently skips.

## Checked

2026-11-09. Read the whole store-flow-code page. Confirmed the storage options, `from_source` sources, pull step names and parameters, git credential options and token notes, default branch, no push to the git host, Docker behaviour and the four auto-install conditions. Removed nothing.

Method: documentation only; no commands were run.
