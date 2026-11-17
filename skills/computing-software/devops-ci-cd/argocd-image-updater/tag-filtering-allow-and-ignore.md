---
id: computing-software.devops-ci-cd.argocd-image-updater.tag-filtering-allow-and-ignore
name: tag-filtering-allow-and-ignore
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, allow-tags, ignore-tags, tag-filtering, regexp, glob-patterns, disable-updates]
level: practitioner
status: docs-checked
description: "Filter registry tags with allowTags regexp or any, exclude with ignoreTags globs, and pause an image by ignoring everything with the star pattern."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/test.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tag filtering: allowTags and ignoreTags

allowTags. A match function applied to every tag; a positive match keeps the tag as a candidate.

```yaml
commonUpdateSettings:
  allowTags: "regexp:^v[0-9]+\\.[0-9]+\\.[0-9]+$"
```

Functions: `regexp:<expression>` and `any` (the default, no filtering). An invalid function or invalid regular expression matches no tag at all, a safeguard so the wrong tags are never considered.

ignoreTags. A list of glob patterns (Go `filepath.Match` syntax); regular expressions are not supported.

```yaml
commonUpdateSettings:
  ignoreTags: [ "latest", "master" ]
```

Pause an image without deleting config: `ignoreTags: ["*"]` leaves no tags to consider.

Where each matters: filtering applies to all strategies, and it is the only restriction for `newest-build` and `alphabetical`, which ignore the version constraint. Example: `allowTags: "regexp:^v1.0.0-[0-9a-zA-Z]+$"` with `newest-build`.

Both can be set globally, per application or per image.

CLI preview: `argocd-image-updater test nginx --allow-tags '^1.19.\d+(\-.*)*$' --update-strategy newest-build` and `--ignore-tags`.

## Checked
2026-11-08. Confirmed against the Argo CD Image Updater images, update-strategies and test command pages: `allowTags` match functions `regexp:` and `any` (default), the invalid-expression safeguard, `ignoreTags` glob patterns per `filepath.Match` with no regular expressions, `ignoreTags: ["*"]` to pause an image, the newest-build example, constraint having no effect for other strategies, global, application and image level settings, and the `test --allow-tags` and `--ignore-tags` flags. Removed the backslash-escaping note and the annotation migration note, which are not on those pages.
Method: documentation only; no commands were run.
