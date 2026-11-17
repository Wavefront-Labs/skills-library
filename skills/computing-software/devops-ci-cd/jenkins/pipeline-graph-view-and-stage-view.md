---
id: computing-software.devops-ci-cd.jenkins.pipeline-graph-view-and-stage-view
name: pipeline-graph-view-and-stage-view
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, pipeline-graph-view, blue-ocean, pipeline-visualisation]
level: intro
status: docs-checked
description: "Visualise Jenkins pipelines with the Pipeline Graph View plugin (Blue Ocean's successor) or Stage View: install, per-step logs, parallel branches and rerun."
sources: ["https://plugins.jenkins.io/pipeline-graph-view/", "https://www.jenkins.io/doc/book/blueocean/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline graph view and stage view

Blue Ocean has been deprecated since July 2026 and receives no further security fixes or functionality
updates. The Jenkins docs point to the **Pipeline Graph View** plugin (`pipeline-graph-view`), which adds a
"Pipeline Overview" to each build page.

## Options
| Plugin | Shows | Notes |
|---|---|---|
| Pipeline Graph View | stage graph with parallel branches and nested stages, real-time logs, graph and stage views | actively maintained |
| Pipeline: Stage View | alternate view of Pipeline execution | see the plugin page |
| Blue Ocean | graph UI | deprecated since July 2026 |

## Useful features
- Logs can be viewed in real time without leaving the interface.
- Stages with parallel branches or nested children can be collapsed and expanded.
- "Restart from stage" is available in the classic UI and Pipeline Graph View for declarative pipelines (it can be turned off with the `disableRestartFromStage` option).

## Making graphs readable
- Name parallel branches and stages meaningfully; dynamic stage names should be stable across runs
  for Stage View to line up columns.
- Avoid hundreds of parallel branches; group with matrix or batches.

## Verify
- [ ] The build page offers "Pipeline Overview" with all stages including parallel branches.

## Checked

2026-10-28. Confirmed from the Jenkins Blue Ocean page (deprecated since July 2026, no further fixes, Pipeline Graph View actively maintained, Stage View as an alternate view), the Pipeline Graph View plugin page ("Pipeline Overview", real-time logs, collapsible parallel and nested stages) and the Pipeline syntax page (`disableRestartFromStage`). Removed: plugin id for Stage View, suggested-plugin status, default-page setting, unstable colours, scripted-parallel graph advice, "Pipeline Console".

Method: documentation only; no commands were run.
