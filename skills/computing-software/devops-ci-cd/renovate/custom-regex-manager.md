---
id: computing-software.devops-ci-cd.renovate.custom-regex-manager
name: custom-regex-manager
category: computing-software
field: devops-ci-cd
product: renovate
tags: [custom-managers, regex-manager, match-strings, renovate]
level: advanced
status: docs-checked
description: "Teach Renovate to update versions in arbitrary files using customManagers with the regex engine."
sources:
  - https://docs.renovatebot.com/configuration-options/#custommanagers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`customManagers` (formerly `regexManagers`) extract dependencies from files Renovate has no built-in manager for. Two engines exist: `regex` (named capture groups) and `jsonata` (queries).

Each manager needs `managerFilePatterns` (regex or glob for files) and `matchStrings` (patterns or queries). The match must produce `datasource`, `depName` and/or `packageName`, and `currentValue`, either as named groups or through templates like `depNameTemplate`. Use only one of the two methods to avoid confusion.

```json
{
  "customManagers": [
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)Dockerfile$/"],
      "matchStrings": [
        "# renovate: datasource=(?<datasource>[a-z-]+) depName=(?<depName>\\S+)\\nENV VERSION=(?<currentValue>\\S+)"
      ],
      "versioning": "semver"
    }
  ]
}
```

Tips:

- Set `versioning` explicitly. If both the manager and datasource lack it, Renovate falls back to `semver-coerced`.
- In template fields use triple braces such as `{{{depName}}}` so Handlebars does not escape characters.
- `autoReplaceStringTemplate` rewrites the matched text, which enables migrations such as moving to a new Docker registry path.
- Enable it with `enabledManagers` using the `custom.` prefix, for example `custom.regex`.
- Check the custom manager presets before writing your own.

## Checked

Method: docs-checked 2026-11-09 against the customManagers, customManagers.customType, customManagers.autoReplaceStringTemplate and enabledManagers sections of the configuration-options page (read in full for those sections); example shape cross-checked against the regex manager page.
