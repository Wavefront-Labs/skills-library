---
id: computing-software.devops-ci-cd.renovate.automerge-rules
name: automerge-rules
category: computing-software
field: devops-ci-cd
product: renovate
tags: [automerge, auto-merge, automerge-config, renovate]
level: practitioner
status: docs-checked
description: "Choose which Renovate updates to automerge, with lock file maintenance, non-major and dev dependency examples."
sources:
  - https://docs.renovatebot.com/key-concepts/automerge/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Automerge lets Renovate merge a PR once required checks pass. Maintainers recommend it for updates you would merge anyway, and leaving it off where you want to read changelogs first. It suits `devDependencies` well, and production dependencies when test coverage is strong.

```json
{
  "lockFileMaintenance": { "enabled": true, "automerge": true },
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "matchCurrentVersion": "!/^0/",
      "automerge": true
    }
  ]
}
```

The `matchCurrentVersion` clause excludes pre-1.0 packages, which can break at any time under SemVer.

Behaviour to expect:

- Automerge takes time. Renovate only merges one branch per target branch per run, and only if the branch is up to date and green. Wait about two hours before troubleshooting.
- Constant commits to the base branch keep deferring automerge because branches fall behind.
- With no tests, set `ignoreTests` to `true` or nothing will merge.
- Renovate withholds assignees and reviewers on automerge PRs until checks fail; set `assignAutomerge` to always add them.

Combine automerge with a `schedule` so Renovate can rebase and merge a batch unattended, rather than leaving you conflicting lock file PRs.

## Checked

2026-11-03. Confirmed against the Renovate Automerge key-concepts page: the maintainer recommendation, the lock file maintenance and non-major examples, the `matchCurrentVersion` pre-1.0 exclusion, the two-hour wait, one merge per target branch per run, `ignoreTests`, `assignAutomerge`, and the scheduling benefit. Nothing removed.

Method: documentation only; no commands were run.
