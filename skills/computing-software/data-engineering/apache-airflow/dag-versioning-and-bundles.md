---
id: computing-software.data-engineering.apache-airflow.dag-versioning-and-bundles
name: dag-versioning-and-bundles
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-3, dag-versioning, dag-bundles, gitdagbundle, localdagbundle, dag-processor, code-versions]
level: advanced
status: docs-checked
description: "Configure Airflow 3 DAG bundles (local and Git) and DAG versioning so runs keep the code version they started with, and view or rerun history per version."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/dag-bundles.html
  - https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-66%3A+DAG+Bundles+%26+Parsing
  - https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-65%3A+Improve+DAG+history+in+UI
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAG versioning and DAG bundles (Airflow 3)

**Goal:** a DAG run executes all its tasks with the code version it started with, and the UI shows which version each run used.

## Concepts
- **DAG bundle:** a source of DAG files with an optional version. Built-in: `LocalDagBundle` (a folder, no versioning) and `GitDagBundle` (repo + branch, versioned by commit), from the git provider.
- **DAG version:** Airflow 3 records a new serialized DAG version whenever the structure/code changes. Runs reference the version. The Grid view can show the graph/code for any version.
- With a versioned bundle, workers check out the exact bundle version the run started with; with a local bundle, tasks run the latest code on disk (history is still recorded but not enforced).

## Configure bundles
```ini
[dag_processor]
dag_bundle_config_list = [
  {"name": "main", "classpath": "airflow.providers.git.bundles.git.GitDagBundle",
   "kwargs": {"git_conn_id": "git_dags", "tracking_ref": "main", "subdir": "dags", "refresh_interval": 60}}
]
```
`tracking_ref` (branch, tag or commit SHA) is the only required Git kwarg; `git_conn_id` references an Airflow connection with the repository credentials. By default Airflow adds a `LocalDagBundle` for the configured DAGs folder.

## Operational effects
- Deploying a change mid-run no longer mixes old and new task code in a single run (versioned bundles).
- Rerunning/clearing tasks of an old run: the default version behaviour is configurable, and the `run_on_latest_version` request parameter overrides it (see the dag-bundles page for precedence).
- The DAG processor is a separate component in Airflow 3 (`airflow dag-processor`); it must have access to bundles; workers need bundle access too.

## Migration from Airflow 2 style deployments
- Baked-image or git-sync folder: keep as a `LocalDagBundle` first (identical behaviour), then switch to `GitDagBundle` for per-run versioning.
- Remove git-sync sidecars once workers fetch bundles themselves; size worker disk for bundle caches.

## Gotchas
- Only DAG code in the bundle is versioned. Shared libraries installed in the image, plugins, connections and variables are not.
- Private repos: rotate the token in the Git connection and watch the dag-processor logs for refresh errors.

## Verify
- [ ] Change a task's code during a long run: remaining tasks in that run still execute the old version (check task log header for bundle version/commit).
- [ ] Grid view shows version markers between runs.

## Checked

2026-10-28. Confirmed against: dag-bundles page (dag_bundle_config_list under [dag_processor], GitDagBundle classpath and kwargs, tracking_ref required, git_conn_id, per-bundle refresh_interval, default LocalDagBundle, run_on_latest_version, GitDagBundle supports versioning). Removed (not confirmable in the fetched pages): LocalDagBundle path kwarg example, deployment-mixing claim detail, commit-cache detail, version-per-commit claim.

Method: documentation only; no commands were run.
