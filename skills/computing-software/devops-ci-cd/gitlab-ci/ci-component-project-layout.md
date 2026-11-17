---
id: computing-software.devops-ci-cd.gitlab-ci.ci-component-project-layout
name: ci-component-project-layout
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, component-project-structure, ci-cd-components, ci-catalog]
level: practitioner
status: docs-checked
description: "Lay out a GitLab CI/CD component project: templates/ directory forms, README docs, its own test pipeline, and release requirements for the CI/CD Catalog."
sources: ["https://docs.gitlab.com/ci/components/#directory-structure", "https://docs.gitlab.com/ci/components/#publish-a-component-project", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/components/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD component project layout

```
my-components/
  templates/
    lint.yml                 # component "lint"
    build/
      template.yml           # component "build" (directory form)
      helper.sh              # NOT accessible to consumers
  README.md                  # catalog page: inputs table, usage examples
  LICENSE.md
  .gitlab-ci.yml             # tests the components + releases
```
Consumers: `include: - component: $CI_SERVER_FQDN/group/my-components/lint@1.2.0`.

## Rules
- Only `templates/<name>.yml` or `templates/<name>/template.yml` are components; max 100 per project.
- A component file has a `spec:` header, `---`, then jobs:
  ```yaml
  spec:
    inputs:
      stage: { default: test }
      image: { default: "node:22-alpine" }
  ---
  lint:
    stage: $[[ inputs.stage ]]
    image: $[[ inputs.image ]]
    script: echo "run the linter here"
  ```
- Only the `template.yml` file is used by consumers; other files in a component directory are not released with the component.
- To publish to the catalog the project needs a description, a `README.md` in the root, and the **CI/CD Catalog project** toggle (Settings > General > Visibility, project features, permissions; Owner role).

## Self-test pipeline
```yaml
include:
  - component: $CI_SERVER_FQDN/$CI_PROJECT_PATH/lint@$CI_COMMIT_SHA
create-release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cli:latest
  rules: [{ if: $CI_COMMIT_TAG }]
  script: echo "release $CI_COMMIT_TAG"
  release: { tag_name: $CI_COMMIT_TAG, description: "Release $CI_COMMIT_TAG" }
```
Create the release with the `release` keyword in a job, not the Releases API, and tag with a semantic version, for the catalog to publish it.

## Verify
- [ ] After the release job succeeds, the catalog lists the project with its components and the new version.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/components/_index.md: directory structure (single `templates/<name>.yml` or `templates/<name>/template.yml`, only `template.yml` used from a directory), maximum 100 components per project (raised from 30 in GitLab 18.5), `spec` header then `---`, the self-test include with `$CI_COMMIT_SHA`, the `create-release` job using `registry.gitlab.com/gitlab-org/cli:latest`, and the publish prerequisites (description, README.md, catalog toggle, `release` keyword rather than the Releases API, semantic version tag). Removed the unconfirmed container-image advice and tool-specific commands.

Method: documentation only; no commands were run.
