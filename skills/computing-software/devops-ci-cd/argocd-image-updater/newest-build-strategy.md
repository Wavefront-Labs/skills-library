---
id: computing-software.devops-ci-cd.argocd-image-updater.newest-build-strategy
name: newest-build-strategy
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, newest-build, latest-strategy, build-date, docker-hub-limits, reproducible-builds, update-strategy]
level: practitioner
status: docs-checked
description: "Use the newest-build strategy to follow the image with the most recent build date, handle multi-tag ties, and avoid Docker Hub pull limits and reproducible-build traps."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# newest-build strategy

Name `newest-build`; the old alias `latest` is deprecated and logs a warning.

```yaml
images:
  - alias: "myimage"
    imageName: "some/image"
    commonUpdateSettings:
      updateStrategy: "newest-build"
      allowTags: "regexp:^[0-9a-f]{7}$"
```

It picks the tag whose image has the most recent build date, whatever its name (Git SHA, random string). Note it is the build date, not the push or tag time.

Tie rule: if one image carries several tags (say `f33bacd`, `dev`, `latest`) they share a build date; the tool sorts tag names lexically descending and picks the last, so you get `latest` instead of the SHA. Restrict candidates with `allowTags` (the example matches 7-hex-digit short SHAs) or `ignoreTags: [ "latest", "master" ]`.

Warnings:

- Docker Hub pull limits (since November 2020): this strategy pulls manifests to find the newest tag and these count against free-plan and anonymous limits, so it is not recommended for Docker Hub images unless you are unaffected.
- Reproducible builds that fix the creation date make the strategy unable to decide.

Platform filtering via `platforms` works with this strategy because it fetches metadata (the docs name it under its old name `latest`).

## Checked

2026-11-04. Confirmed against update-strategies.md (newest-build section: rename warning, build date not push date, tie rule, allowTags and ignoreTags examples, Docker Hub pull-limit warning, reproducible builds note) and images.md (platforms note). Removed a generic test-command line the page does not state for this strategy.

Method: documentation only; no commands were run.
