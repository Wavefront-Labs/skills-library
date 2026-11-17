---
id: computing-software.devops-ci-cd.argocd-image-updater.alphabetical-strategy
name: alphabetical-strategy
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, alphabetical, name-strategy, lexical-sort, date-tags, allow-tags, update-strategy]
level: practitioner
status: docs-checked
description: "Use the alphabetical strategy to pick the lexically last tag, restricted by allowTags, and avoid the unpadded-number sorting trap that silently pins an older tag."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# alphabetical strategy

Name `alphabetical`; the old alias `name` is deprecated and logs a warning.

```yaml
images:
  - alias: "myimage"
    imageName: "some/image"
    commonUpdateSettings:
      updateStrategy: "alphabetical"
      allowTags: "regexp:^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
```

It sorts the registry tags lexically by name in descending order and picks the last tag in the list for update. By default every tag is considered; the `allowTags` regular expression above admits only `YYYY-MM-DD` date tags.

Trap: tags are compared byte by byte, so numeric fields must be zero padded to a constant width. With `2026-9-01` and `2026-10-03`, the unpadded `9` sorts above `10`, and the image stays pinned to the older tag with no error logged.

For calendar-versioned tags, prefer the `calver` strategy, which compares fields numerically.

This strategy does not fetch metadata, so `platforms` is ignored, and a version constraint in `imageName` has no effect.

## Checked

2026-11-04. Confirmed against the Argo CD Image Updater docs pages update-strategies.md (alphabetical strategy, deprecated alias name and its warning, descending lexical sort and last tag picked, zero-padding warning, allowTags example) and images.md (platforms only affects strategies that fetch metadata; a version constraint has no effect for strategies other than semver, digest and calver). Removed a generic self-check line the page does not state.

Method: documentation only; no commands were run.
