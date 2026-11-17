---
id: computing-software.devops-ci-cd.renovate.config-file-locations
name: config-file-locations
category: computing-software
field: devops-ci-cd
product: renovate
tags: [config-file, renovate-json, default-branch, renovate]
level: intro
status: docs-checked
description: "Where Renovate looks for repository configuration, the JSON5 and JSONC rules, and why the default branch config always wins."
sources:
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate searches each repository for a config file in this order and stops at the first match: `renovate.json`, `renovate.jsonc`, `renovate.json5`; the same three names under `.github/` and under `.gitlab/`; `.renovaterc`, `.renovaterc.json`, `.renovaterc.jsonc`, `.renovaterc.json5`; and a `renovate` section in `package.json`. Anything named in the self-hosted `configFileNames` array is checked before the standard list, so an admin can add a custom filename.

Key facts from the docs:

- Renovate always reads config from the repository's default branch, even when that config sets `baseBranchPatterns`. It does not read or override config from each base branch.
- JSONC is supported for `.json` files and for files with no extension such as `.renovaterc`. For comments, prefer an explicit `.jsonc` file over a `.json` file with comments, because editors and syntax highlighters struggle with the latter.
- Shareable presets work with both JSON and JSON5 formats.
- Keeping config inside `package.json` is deprecated and may be removed.

A minimal file:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"]
}
```

If you need a different filename, an administrator sets `configFileNames`.

## Checked

2026-11-03. Confirmed against the "Locations for configuration filenames" section of the Renovate configuration options page (file list, search order, `configFileNames`, JSONC support, `package.json` deprecation, default-branch rule, shareable presets in JSON and JSON5) and the Config Validation page (`$schema` and `config:recommended` in example configs). Removed the claim about editor validation and the `requireConfig` and `onboarding` aside.

Method: documentation only; no commands were run.
