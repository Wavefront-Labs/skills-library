---
id: computing-software.devops-ci-cd.gitlab-ci.component-version-references-and-latest
name: component-version-references-and-latest
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, component-version-ref, latest-tag, partial-semver-ref, component-pinning]
level: practitioner
status: docs-checked
description: "Reference CI components by exact version, partial semver, ~latest, branch or SHA; pick the right pinning strategy and keep references updated automatically."
sources: ["https://docs.gitlab.com/ci/components/#component-versions", "https://docs.gitlab.com/ci/components/#partial-semantic-versions", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/components/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component version references and `~latest`

```yaml
include:
  - component: $CI_SERVER_FQDN/platform/ci/pytest@1.4.2     # exact release
  - component: $CI_SERVER_FQDN/platform/ci/lint@1.4         # latest 1.4.x
  - component: $CI_SERVER_FQDN/platform/ci/scan@1           # latest 1.x.y
  - component: $CI_SERVER_FQDN/platform/ci/docs@~latest     # newest release, any major
  - component: $CI_SERVER_FQDN/platform/ci/build@main       # branch HEAD (testing only)
  - component: $CI_SERVER_FQDN/platform/ci/deploy@e3262fdd0914fa823210cdb79a8c421e2cef79d8   # commit SHA
```

## Resolution
- Exact version (tag): `1.4.2`. Components released to the CI/CD Catalog must be tagged with a semantic version.
- Partial semver (`1`, `1.4`): selects the latest published version in that pattern, so it receives minor and patch updates, not new majors. Example: with versions 1.0.0, 1.1.0, 1.1.1, 1.2.0, 2.0.0, 2.0.1, 2.1.0, `1` selects 1.2.0, `1.1` selects 1.1.1 and `~latest` selects 2.1.0.
- `~latest`: the latest published version, which may include breaking changes. Partial versions and `~latest` work only for components published in the catalog, and never select pre-releases such as `1.0.1-rc` (name a pre-release in full).
- Branch names and commit SHAs may not be published in the catalog but can be used for testing.
- Precedence when a name is ambiguous (highest first): commit SHA, tag, branch.

## Strategy
| Consumer | Ref |
|---|---|
| Production pipelines, regulated | exact version or SHA, updated deliberately |
| Internal teams who trust platform | major (`@2`) |
| Component's own tests | `@$CI_COMMIT_SHA` |
| Never | `@~latest` in anything that deploys |

The docs recommend pinning dependencies on other components to a catalog release or Git SHA rather than `~latest` or a branch, and updating the pins regularly.

## Gotchas
- Use `$CI_SERVER_FQDN` instead of a hardcoded host so the same component reference works on another instance (for example a mirror on GitLab Self-Managed).
- A reference that cannot be resolved fails pipeline creation.

## Verify
- [ ] Pipeline creation succeeds and the component job appears with the version you expect.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/components/_index.md: reference types and precedence order, partial semantic versions and the worked 1/1.1/~latest example, that partial versions and `~latest` apply only to catalog components and skip pre-releases, `$CI_SERVER_FQDN` usage, and the pinning guidance. Removed the Renovate claim, the tags-can-move claim and the quoted error text, which that page does not state.

Method: documentation only; no commands were run.
