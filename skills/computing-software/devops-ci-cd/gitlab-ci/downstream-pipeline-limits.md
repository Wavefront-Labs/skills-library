---
id: computing-software.devops-ci-cd.gitlab-ci.downstream-pipeline-limits
name: downstream-pipeline-limits
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, downstream-limits, downstream-pipelines, parent-child-pipelines]
level: advanced
status: docs-checked
description: "Know GitLab downstream pipeline limits: parent-child nesting depth and the pipeline hierarchy size, and how to restructure pipelines that hit them."
sources: ["https://docs.gitlab.com/ci/pipelines/downstream_pipelines/", "https://docs.gitlab.com/administration/instance_limits/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downstream pipeline depth and include limits

| Limit | Default |
|---|---|
| Parent-child nesting depth | a maximum of two levels of child pipelines (parent > child > grandchild) |
| Downstream pipelines in one pipeline hierarchy | up to 1000 by default (`pipeline_hierarchy_size` in the instance limits) |
| Multi-project pipelines | independent of the parent, so no nesting limit |
| Generated child config from an artifact | the artifact holding the generated YAML must be within instance limits |

For include counts, YAML size and the other CI limits, read the GitLab CI/CD limits for your
version; they were not in the pages checked for this review.

## Restructuring
- Too deep: flatten grandchildren into the child; use `parallel:matrix` instead of another level.
- Huge generated child configs: split by area into several triggered children (each its own include).
- Multi-project pipelines are independent, so they do not nest under the parent; use them to split a tree that is too deep.

Self-managed instances can change the hierarchy limit: see "Limit pipeline hierarchy size" in the GitLab docs.

## Verify
- [ ] The pipeline editor validates the parent; trigger jobs show downstream pipelines created.

## Checked

2026-10-31. Confirmed against the GitLab downstream pipelines page and the instance limits page: maximum depth of two levels of child pipelines, 1000 downstream pipelines per hierarchy by default (`pipeline_hierarchy_size`), multi-project pipelines are independent with no nesting limit, generated YAML artifact must be within instance limits. Removed: include count and nesting figures, YAML size figures, `ci_active_jobs` note, error message texts, and the rails console commands (not in the fetched pages).

Method: documentation only; no commands were run.
