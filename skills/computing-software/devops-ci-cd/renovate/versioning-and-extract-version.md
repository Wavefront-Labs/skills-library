---
id: computing-software.devops-ci-cd.renovate.versioning-and-extract-version
name: versioning-and-extract-version
category: computing-software
field: devops-ci-cd
product: renovate
tags: [versioning, extract-version, allowed-versions, renovate]
level: advanced
status: docs-checked
description: "Fix version parsing mismatches with versioning schemes, extractVersion capture groups and allowedVersions."
sources:
  - https://docs.renovatebot.com/configuration-options/#extractversion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate compares versions with a versioning scheme, usually decided by the manager or datasource. Override it with `versioning` when the default does not fit, for example `semver`, `pep440` or `regex`.

When the datasource returns raw strings that differ from what your package file holds, use `extractVersion` with a named capture group called `version`:

```json
{
  "packageRules": [
    {
      "matchPackageNames": ["foo"],
      "extractVersion": "^(?<version>v\\d+\\.\\d+)"
    }
  ]
}
```

`extractVersion` applies only to versions coming from the datasource. It is not applied to the `currentValue` in your file, so that value must already have the extracted form.

Other helpers:

- `allowedVersions` restricts releases to a range or regex, for example `"<2.0.0"`.
- `followTag` keeps a package synced strictly to a registry tag such as `insiders`; the datasource must support tags (npm does). Documented as advanced use only.
- `respectLatest` (default `true`) ignores versions newer than the `latest` tag, unless the current version is already past it. It defaults to `false` for Maven when a `latest` tag is found.
- `ignoreUnstable` (default `true`) avoids unstable versions such as `4.0.0-rc3` unless you are already on an unstable version with the same major.minor.patch.
- Instead of a single `version` group, `extractVersion` can use `major`, `minor`, `patch`, `prerelease` and `build` groups; `major` is required, and a `version` group takes priority if present.

Custom managers default to `semver-coerced` when neither the manager nor datasource sets a versioning, so set `versioning` explicitly for predictable results.

## Checked

Method: docs-checked 2026-11-09 against the extractVersion, packageRules.allowedVersions, followTag, ignoreUnstable, respectLatest, versioning and customManagers sections of the configuration-options page (read in full for those sections). Dropped the Docker suffix claim, which was not confirmed.
