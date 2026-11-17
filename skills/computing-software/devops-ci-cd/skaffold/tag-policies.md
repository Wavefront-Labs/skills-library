---
id: computing-software.devops-ci-cd.skaffold.tag-policies
name: tag-policies
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [tagpolicy, gitcommit, inputdigest, datetime, envtemplate]
level: practitioner
status: docs-checked
description: "Choose how Skaffold tags built images: git commit by default, or input digest, date-time, env template, custom template or sha256."
sources:
  - "https://skaffold.dev/docs/taggers/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Set the policy under `build.tagPolicy`. The default is `gitCommit`.

```yaml
build:
  tagPolicy:
    gitCommit:
      variant: AbbrevCommitSha
      prefix: "v-"
      ignoreChanges: false
```

`gitCommit` variants: `Tags` (default), `CommitSha`, `AbbrevCommitSha`, `TreeSha`, `AbbrevTreeSha`. A `-dirty` suffix is added when there are uncommitted changes, unless `ignoreChanges` is set.

Other taggers:

- `inputDigest`: a digest of the artifact source files (the dependencies calculated by the builder); no options.
- `envTemplate`: required `template`, such as `"{{.FOO}}"`, filled from environment variables (`FOO=v1` gives `example:v1`). Using `IMAGE_NAME` in the template is deprecated.
- `dateTime`: `format` (default `2006-01-02_15-04-05.999_MST`) and `timezone` (default `Local`).
- `customTemplate`: required `template` plus named `components`, each any other tagger (for example `{{.FOO}}_{{.BAR}}`); nested `customTemplate` components are not supported.
- `sha256`: uses `latest`; the name is misleading, as the image digest is added to `:latest` for an immutable reference when deploying to a remote cluster. No options.

Override everything on the command line with `skaffold build --tag v1.2.3`.

Tags are computed before images are built. Skaffold always makes image references in manifests immutable: a pushed image becomes `tag@sha256:...`. Images loaded directly into the cluster get an extra local-only tag named after the image ID. Skaffold never references an image by tag alone.

A `dateTime` tag uses the time Skaffold starts building, so it changes on every build; pick a deterministic policy such as `gitCommit` or `inputDigest` where you need the same tag for the same source.

## Checked

2026-11-09: tagger list, default, gitCommit variants and `-dirty` suffix, dateTime defaults, customTemplate nesting limit, sha256 behaviour, `--tag` override and immutable references confirmed. Corrected envTemplate (IMAGE_NAME is deprecated), expanded inputDigest and sha256 detail, and reworded the CI advice as non-documented guidance.

Method: docs-checked 2026-11-09 against skaffold.dev/docs/taggers/
