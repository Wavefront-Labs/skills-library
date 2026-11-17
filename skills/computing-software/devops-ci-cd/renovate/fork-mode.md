---
id: computing-software.devops-ci-cd.renovate.fork-mode
name: fork-mode
category: computing-software
field: devops-ci-cd
product: renovate
tags: [fork-processing, fork-token, fork-mode, renovate]
level: advanced
status: docs-checked
description: "Run Renovate from a fork with forkProcessing, forkToken, forkOrg and forkCreation for repositories you cannot write to."
sources:
  - https://docs.renovatebot.com/configuration-options/#forkprocessing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate can create PRs from a fork when the bot account has no write access to the target repository.

Options:

- `forkProcessing` accepts `auto` (default), `enabled` and `disabled`. In `autodiscover` mode Renovate skips forked repositories, even ones with a Renovate config file, because it cannot tell who added the file. Set `"forkProcessing": "enabled"` in the repository's `renovate.json`, or run the CLI with `--fork-processing=enabled`.
- In other modes, set `"forkProcessing": "disabled"` in global config to skip forks.
- Only the `onboardingConfigFileName` (default `renovate.json`) is supported for `forkProcessing`.
- `forkModeDisallowMaintainerEdits` (default `false`, GitHub only) stops the upstream maintainers pushing to Renovate PRs created from a fork; it only matters if you set `forkToken`.

```json
{
  "forkProcessing": "enabled"
}
```

With the Mend Renovate App, `forkProcessing` is `disabled` when you allow all repositories and `enabled` for each repository you select.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`forkProcessing` values, default, autodiscover behaviour, allowed filenames, Mend app behaviour, `forkModeDisallowMaintainerEdits`). Removed: `forkCreation` and `forkOrg` (not on that page), the example's invented organisation, and the unsupported practical notes and sync advice. `forkToken` is mentioned only as the page notes it.

Method: documentation only; no commands were run.
