---
id: computing-software.devops-ci-cd.renovate.ignore-deps-and-paths
name: ignore-deps-and-paths
category: computing-software
field: devops-ci-cd
product: renovate
tags: [ignore-deps, ignore-paths, include-paths, renovate]
level: intro
status: docs-checked
description: "Exclude dependencies, files or whole managers using ignoreDeps, ignorePaths, includePaths and enabled."
sources:
  - https://docs.renovatebot.com/configuration-options/#ignoredeps
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Several options remove things from Renovate's scope:

- `ignoreDeps` lists exact dependency names to skip. It does not support patterns. It is equivalent to a package rule with `enabled` set to `false`.
- `ignorePaths` skips package files whose path matches a string or glob. The default is `**/node_modules/**` and `**/bower_components/**`; `config:recommended` also ignores vendor, examples, test(s) and fixtures directories.
- `includePaths` restricts Renovate to package files within the given paths.
- `enabled: false` inside a `packageRules` entry disables matching updates, including by manager or dep type.
- `ignoreUnstable` and `ignoreDeprecated` both default to `true`: Renovate does not move to unstable versions (such as `4.0.0-rc3`) or to deprecated releases unless the current version already is.
- `enabledManagers` allows only the listed managers and implicitly disables all others.

```json
{
  "ignoreDeps": ["eslint", "eslint-config-base"],
  "ignorePaths": ["**/test/fixtures/**", "**/vendor/**"],
  "enabledManagers": ["dockerfile", "npm"],
  "packageRules": [
    {
      "matchPackageNames": ["/legacy-/"],
      "enabled": false
    }
  ]
}
```

Custom managers need the `custom.` prefix in `enabledManagers`, for example `custom.regex`.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`ignoreDeps` exact-match only and its equivalent package rule, `ignorePaths` default and the `config:recommended` additions, `includePaths`, `enabledManagers` and the `custom.` prefix, `ignoreUnstable`, `ignoreDeprecated`). Removed: the `description` advice and the `allowedVersions` advice (not confirmed on these pages). The example path and package names are placeholders.

Method: documentation only; no commands were run.
