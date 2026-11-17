---
id: computing-software.devops-ci-cd.renovate.commit-message-templates
name: commit-message-templates
category: computing-software
field: devops-ci-cd
product: renovate
tags: [commit-message, commit-message-topic, pr-title, renovate]
level: advanced
status: docs-checked
description: "Customise Renovate commit messages and PR titles with commitMessage pieces, trailers and templates."
sources:
  - https://docs.renovatebot.com/configuration-options/#commitmessagetopic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate builds commit messages and PR titles from parts: `commitMessagePrefix`, `commitMessageAction`, `commitMessageTopic`, `commitMessageExtra` and `commitMessageSuffix`. Change one part instead of copying the whole `commitMessage` template.

```json
{
  "packageRules": [
    {
      "matchManagers": ["github-actions"],
      "commitMessageTopic": "{{depName}}"
    }
  ],
  "commitMessagePrefix": "chore(deps):",
  "commitMessageLowerCase": "auto"
}
```

- `commitMessageTopic` defaults to `dependency {{depName}}`, such as `dependency react`; the docs recommend setting it with `matchManagers` in `packageRules`.
- `commitMessageAction` defaults to `Update`; `commitMessageLowerCase` defaults to `auto` (lowercases titles when semantic commits are on; `never` leaves them).
- `commitBody` appends a body, `commitBodyTable` adds an update table, and `commitTrailers` appends Git trailers.
- Editing `commitMessage` directly is deprecated; use the part options instead. These options are marked "for advanced use only".

The PR title is important to Renovate's matching algorithms (such as deciding whether to recreate a PR), so the docs advise not modifying it much; editing `prTitle` directly is deprecated. The experimental `prTitleStrict` bypasses the extra context Renovate appends to titles for base branches and for grouped updates when `separateMajorMinor` or `separateMinorPatch` is true.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`commitMessage*` options and defaults, `commitBody`, `commitBodyTable`, `commitTrailers`, `prTitle`, `prTitleStrict`). Removed the invented Docker image topic example and unsupported claims about reappearing or blocked PRs.

Method: documentation only; no commands were run.
