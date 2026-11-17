---
id: computing-software.devops-ci-cd.renovate.package-rules-matching
name: package-rules-matching
category: computing-software
field: devops-ci-cd
product: renovate
tags: [package-rules, matchers, rule-merging, renovate]
level: practitioner
status: docs-checked
description: "How packageRules are evaluated and merged, and the all-matchers-must-match semantics of match options."
sources:
  - https://docs.renovatebot.com/configuration-options/#packagerules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Use `packageRules` to apply settings to a subset of dependencies. Every rule is evaluated, and when several rules match a dependency their settings are merged. Order matters: a later rule overrides an earlier one when both set the same option.

Matching works like this:

- Each rule needs at least one `match...` matcher (for example `matchPackageNames`, `matchUpdateTypes`, `matchManagers`, `matchDatasources`, `matchDepTypes`, `matchCurrentVersion`).
- If a rule has several matchers, all of them must match.
- A matcher with positive patterns needs at least one of them to match.
- A matcher returns false if any negative pattern matches, even when a positive one also matched.

```json
{
  "packageRules": [
    {
      "description": "Group eslint packages",
      "matchPackageNames": ["eslint**"],
      "groupName": "eslint packages"
    },
    {
      "matchUpdateTypes": ["major"],
      "matchManagers": ["npm"],
      "dependencyDashboardApproval": true
    }
  ]
}
```

Put broad rules first and specific exceptions last, because the later rule wins. Add a `description` to each rule so reviewers know why it exists. For Maven the package name is `groupId:artifactId`, so match it with that form.

Mixing exact names and patterns in one `matchPackageNames` array is allowed, and the rule applies if either kind matches.

## Checked

Method: docs-checked 2026-11-09 against the packageRules section of the configuration-options page (read in full for the matching rules, the eslint, neutrino and Maven examples) and the option headings for matchPackageNames, matchUpdateTypes, matchManagers, matchDatasources, matchDepTypes, matchCurrentVersion and dependencyDashboardApproval. Dropped the unsourced advice on rule size.
