---
id: computing-software.devops-ci-cd.gitlab-ci.publishing-components-to-the-ci-catalog
name: publishing-components-to-the-ci-catalog
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, publish-component, catalog-release, ci-catalog, component-project-layout]
level: advanced
status: docs-checked
description: "Publish a GitLab CI/CD component project to the CI/CD Catalog: required layout, README and description, catalog toggle, and release jobs on semver tags."
sources: ["https://docs.gitlab.com/ci/components/#publish-a-component-project", "https://docs.gitlab.com/ci/components/#semantic-versioning", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/components/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing a component to the CI/CD Catalog

## 1. Layout
```text
my-components/
├── templates/
│   ├── pytest.yml               # component "pytest"
│   └── docker-build/
│       ├── template.yml         # component "docker-build"
│       └── Dockerfile.helper    # only template.yml is used by consumers
├── README.md                    # shown in the catalog; document every input
└── .gitlab-ci.yml               # tests + release
```
Max 100 components per project (limit raised from 30 in GitLab 18.5).

## 2. Make it a catalog project
- Owner role: Settings > General > Visibility, project features, permissions > turn on **CI/CD Catalog project**. (GraphQL `catalogResourcesCreate` can automate it.)
- The project needs a description, a root `README.md` and at least one component in `templates/` at the tagged commit.
- Maintainer or Owner role is needed to publish a release.
- Catalog visibility follows the source project's visibility setting; the project only becomes findable after a release is published.

## 3. Release job (catalog versions come from releases created with the `release` keyword)
```yaml
create-release:
  stage: release
  image: registry.gitlab.com/gitlab-org/cli:latest
  rules:
    - if: $CI_COMMIT_TAG
  script: echo "Creating release $CI_COMMIT_TAG"
  release:
    tag_name: $CI_COMMIT_TAG
    description: "Release $CI_COMMIT_TAG of components in $CI_PROJECT_PATH"
```
The tag must use semantic versioning (`1.0.0`, `2.3.4` and `1.0.0-alpha` are valid). The release must be created with the
`release` keyword in a CI/CD job, not the Releases API. Test the components in the tag pipeline before the release job.
To unpublish, turn the catalog toggle off (this destroys the published metadata); a new release republishes it.

## 4. Checklist before tagging
- Every input documented in README with defaults.
- Components test-run in this project's own pipeline (see component testing).
- No global keywords inside components (the docs say they affect every job in the consuming pipeline); configure each job or use uniquely named `extends`.

## Verify
- [ ] The CI/CD Catalog lists the project with the new version and its components.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/components/_index.md: layout and the 100-component limit, catalog toggle location and Owner role, publish prerequisites (description, README, template present, Maintainer or Owner), the `release` keyword requirement, semantic versioning examples, the `registry.gitlab.com/gitlab-org/cli:latest` release image, unpublishing, and the global-keywords guidance. Replaced the `release-cli` image and the tag regex with the documented example, and removed the unconfirmed claims about a `v` prefix and UI-created releases.

Method: documentation only; no commands were run.
