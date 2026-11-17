---
id: computing-software.devops-ci-cd.argo-cd.image-updater-allow-and-ignore-tags
name: image-updater-allow-and-ignore-tags
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, allow-tags, ignore-tags, argocd-image-updater]
level: practitioner
status: docs-checked
description: "Filter which tags Argo CD Image Updater considers with allow-tags regexp, ignore-tags globs and platforms, so prereleases, SHA tags or wrong architectures never deploy."
sources: ["https://argocd-image-updater.readthedocs.io/en/stable/basics/update-strategies/", "https://argocd-image-updater.readthedocs.io/en/stable/configuration/images/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# allow-tags / ignore-tags filters and platforms

In the `ImageUpdater` custom resource, per-image settings go under `commonUpdateSettings`:
```yaml
images:
  - alias: "myalias"
    imageName: "some/image"
    commonUpdateSettings:
      updateStrategy: "newest-build"
      allowTags: "regexp:^[0-9a-f]{7}$"
      ignoreTags: ["latest", "master"]
```
- `allowTags` takes a match function such as `regexp:<expression>`; only matching tags are considered.
- `ignoreTags` takes a list of glob patterns; regular expressions are not supported there.
- With semver a constraint can be attached to the image name, for example `imageName: "nginx:~1.26"` allows patch versions within 1.26.
- Strategies: `semver` (the default), `newest-build` (deprecated alias `latest`), `alphabetical` (deprecated alias `name`) and `digest` (updates to the latest version of a given tag using its digest).
- By default only images built for the same platform as the updater are considered; see the "Image platforms" section of the images page to change it.

## Gotchas
- All strategies except `digest` assume tags are immutable.
- Combine `newest-build` with `allowTags` as in the docs example, so only the tag format you intend is considered.

## Verify
- [ ] The updater picks the tag you expect and ignores the tags excluded by your filters.

## Checked
2026-10-28. Confirmed on the Image Updater update-strategies and images configuration pages: `ImageUpdater` custom resource with `commonUpdateSettings`, `updateStrategy`, `allowTags` with `regexp:` match function, `ignoreTags` glob list (regexes not supported), semver constraint on the image name (`nginx:~1.26`), strategies semver, newest-build (alias latest), alphabetical (alias name), digest, immutable-tag assumption, and the Image platforms default.
Fixed: the skill used the old 0.x annotation mode (`argocd-image-updater.argoproj.io/...`); the current docs configure images in the `ImageUpdater` resource, so the example now uses that.
Removed (not confirmed): the `^1` form, the `ratelimit` setting in `registries.conf`, the `argocd-image-updater test` command and flags, the platforms value syntax.

Method: documentation only; no commands were run.
