---
id: computing-software.data-engineering.prefect.deployment-versioning
name: deployment-versioning
category: computing-software
field: data-engineering
product: prefect
tags: [versioning, rollback, version, commit-sha, image-digest]
level: advanced
status: docs-checked
description: "Prefect deployment versions: live version, rollback and promote, which properties are versioned, and pinning git commits or image digests."
sources:
  - https://docs.prefect.io/v3/how-to-guides/deployments/versioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: version deployments and pin code to a version.

The page describes version history in Prefect Cloud. Every update (CLI, Python or UI) creates a new version and makes it live. Rollback makes a previous version live; promote makes a newer version live again.

Optional `version` label:

```yaml
deployments:
- name: my-deployment
  version: 0.0.1
```
```python
my_flow.deploy(version="0.0.1", ...)
```

Versioned: `description`, `tags`, `labels`, `entrypoint`, `pull_steps`, `parameters`, `parameter_openapi_schema`, `enforce_parameter_schema`, `work_queue_id`, `work_pool_name`, `job_variables`, `created_by`, `updated_by`, `version_info`.

Unversioned (persist across rollbacks): `name` (immutable), `schedules`, `is_schedule_active`, `paused`, `disabled`, `concurrency_limit`, `concurrency_options`.

Pin git code:

```yaml
pull:
- prefect.deployments.steps.git_clone:
    repository: https://github.com/my-org/my-repo.git
    commit_sha: "{{ $GITHUB_SHA }}"
```

In Python pass `GitRepository(url=..., commit_sha=os.getenv("GITHUB_SHA"))` to `from_source()`.

Pin Docker: `job_variables: image: "my-registry/my-image@{{ $IMAGE_DIGEST }}"` in `prefect.yaml`, or `image=f"my-registry/my-image@{os.getenv('IMAGE_DIGEST')}"` with `build=False`.

Git metadata (repo name, URL, branch, commit SHA, first commit message line) is collected automatically in GitHub Actions, GitLab CI, Bitbucket Pipelines and Azure Pipelines.

The page lists no CLI flags for rollback or promote.

## Checked

2026-11-09. Confirmed: Versioning page (docs.prefect.io/v3/how-to-guides/deployments/versioning): live version, rollback and promote, versioned and unversioned property lists, git_clone commit_sha, GitRepository commit_sha, image digest in job_variables, supported CI platforms. Added that the page describes version history for Prefect Cloud.

Method: documentation only; no commands were run.
