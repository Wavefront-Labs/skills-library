---
id: computing-software.devops-ci-cd.argocd-image-updater.calver-layout-tokens
name: calver-layout-tokens
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, calver, calver-layout, calendar-versioning, layout-tokens, update-strategy, tag-layout]
level: advanced
status: docs-checked
description: "Configure the calver strategy: the layout goes in the tag position of imageName, defaults to YYYY.0M.0D, and uses tokens like YYYY, 0M, 0D, MAJOR, MICRO, and MODIFIER."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# calver layout and tokens

`calver` decodes each tag into calendar-version segments and picks the newest, comparing segments numerically (so `2026-9-01` sorts below `2026-10-03`). Tags not matching the scheme are ignored, like non-semver tags under `semver`.

The scheme is the tag part of `imageName`, default `YYYY.0M.0D` (zero padded on purpose, because lenient layouts would make `2026.1.3` and `2026.01.03` the same version and could flip the image between spellings):

```yaml
images:
  - alias: "myimage"
    imageName: "some/image:vYYYY-0M-0D"
    commonUpdateSettings:
      updateStrategy: "calver"
```

Writing a concrete tag such as `some/image:v2026-01-30` is a configuration error: the position holds the layout, not the current version. Bad layouts are reported once at startup and the image is skipped.

Tokens (from calver.org): `YYYY` full year; `YY` short year from 2000 (`6`, `26`, `106`); `0Y` padded short year; `MM` / `0M` month; `WW` / `0W` week of year (`%W` and `%U` conventions); `DD` / `0D` day; `MAJOR`, `MINOR`, `MICRO` numeric segments; `MODIFIER` text such as `rc1`. Padded tokens require the padding; short tokens accept both.

Everything else (the `v` prefix, separators) must appear verbatim. The layout must also be a valid image tag: letters, digits, `_`, `.`, `-`, not starting with `.` or `-`. A non-existent date such as `2026-02-31` is rejected.

## Checked

2026-11-04. Confirmed against the Argo CD Image Updater docs page update-strategies.md (calver section: default layout, token table, padding rules, layout-in-tag-position warning, valid image tag characters, nonexistent dates, startup validation).

Method: documentation only; no commands were run.
