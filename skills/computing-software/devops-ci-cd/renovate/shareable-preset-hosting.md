---
id: computing-software.devops-ci-cd.renovate.shareable-preset-hosting
name: shareable-preset-hosting
category: computing-software
field: devops-ci-cd
product: renovate
tags: [shareable-presets, preset-hosting, default-json, renovate]
level: practitioner
status: docs-checked
description: "Host your own shared Renovate presets in a repo, pick file names, paths and tags, and reference them from extends."
sources:
  - https://docs.renovatebot.com/config-presets/
  - https://docs.renovatebot.com/self-hosted-configuration/#globalextends
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Shared presets live in a repository on the same platform Renovate runs against, or are served over HTTP. npm-hosted presets are deprecated and planned for removal, so avoid them in new setups.

Reference formats for a GitHub repo `abc/foo`:

- `github>abc/foo` loads `default.json` from the default branch.
- `github>abc/foo:xyz` loads `xyz.json`; use `github>abc/foo:xyz.json5` or `.jsonc` for other formats.
- `github>abc/foo//path/xyz` loads `path/xyz.json`.
- Append `#1.2.3` to pin to a Git tag, for example `github>abc/foo#1.2.3`.
- `github>abc/foo:xyz/sub#1.2.3` selects the sub-preset `sub` inside `xyz.json`.

`gitlab>` works the same way against GitLab.

Using a `renovate.json` file as the shared default preset name is deprecated; name it `default.json`.

```json
{
  "extends": ["github>my-org/renovate-config", "github>my-org/renovate-config:node-apps#2.0.0"]
}
```

Other hosts: `gitea>`, `forgejo>` and `local>` (the current platform, useful for self-hosted servers; `local>abc/foo` also works with the prefix left out). HTTP URLs also work, with parameters appended in parentheses. A private GitLab preset repository needs at least Reporter access. Presets can reference each other relatively (`./x`, `../x`, `/x`), inheriting the tag of the referencing preset; a relative reference cannot carry its own `#tag`.

Only JSON, JSONC and JSON5 are accepted, and comments are fine in JSONC. Put a `description` in each preset. Renovate also checks for an org-level `renovate-config` repository with `default.json` (or `.github` with `renovate-config.json`) when onboarding. Admins who need presets inside global config use `globalExtends`, which is resolved immediately instead of being passed through unresolved.

## Checked

2026-11-08: read the whole Shareable Config Presets page (raw source of docs.renovatebot.com/config-presets) and the `globalExtends` section of the self-hosted configuration page (partial read of that page). Confirmed the reference formats and file resolution for github, gitlab, gitea, forgejo and local, tags, `default.json` naming and the `renovate.json` deprecation, npm-based preset deprecation, accepted formats, HTTP presets, relative references, the org-level `renovate-config` lookup and `globalExtends` resolving immediately.
Method: documentation only; no commands were run.
