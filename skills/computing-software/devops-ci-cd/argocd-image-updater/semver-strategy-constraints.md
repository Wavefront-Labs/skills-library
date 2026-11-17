---
id: computing-software.devops-ci-cd.argocd-image-updater.semver-strategy-constraints
name: semver-strategy-constraints
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, semver, version-constraint, prerelease, semver-constraint, tilde-constraint, update-strategy]
level: practitioner
status: docs-checked
description: "Constrain semver updates in imageName with 1.2.x, 1.x or ~1.26, the v prefix, -0 for pre-releases, and non-semver tag handling."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/testing.md", "https://github.com/Masterminds/semver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Semver strategy and constraints

Default strategy. Tags must contain `X.Y.Z` with whole numbers; an optional `v` prefix is treated as equal (`v1.x` matches tag `1.0`, `1.x` matches `v1.0`). Tags that are not valid semver are omitted.

Put the constraint after the colon in `imageName`:

```yaml
images:
  - alias: "someImage"
    imageName: "some/image:1.2.x"   # 1.2.5, 1.2.12 but not 1.3
  - alias: "nginx"
    imageName: "nginx:~1.26"        # any patch in 1.26
  - alias: "other"
    imageName: "some/image:1.x"     # 1.3.0, 1.15.2 but not 2.0
```

Constraint syntax follows the Masterminds semver library. With no constraint, the highest version in the registry is chosen, which can pull in a breaking major release.

Pre-releases are supported but must be explicitly allowed by appending `-0`, for example `some/image:2.x-0` to include `v2.0-rc1`.

The currently deployed tag need not be semver: an app running `latest` can move to a semver tag with a constraint such as `1.x`.

Try constraints before committing: `argocd-image-updater test nginx --semver-constraint 1.17.X` prints the latest match (`nginx:1.17.10` in the docs). In the `test` help the example uses `v1.17.x`.

Semver ignores the `platforms` setting.

## Checked
2026-11-08. Confirmed against the Argo CD Image Updater update-strategies, images, testing and test command pages, and the Masterminds semver README: X.Y.Z tags with optional v prefix treated as equal, `1.2.x` and `1.x` examples, the `~` operator (`~2.3` is `>= 2.3, < 2.4`, so `~1.26` is any patch in 1.26), the `-0` pre-release suffix, highest version when no constraint, non-semver tags omitted, non-semver current tag allowed, the `test --semver-constraint` examples, and `platforms` having no effect for semver. Nothing removed.
Method: documentation only; no commands were run.
