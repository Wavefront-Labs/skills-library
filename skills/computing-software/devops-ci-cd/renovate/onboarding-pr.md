---
id: computing-software.devops-ci-cd.renovate.onboarding-pr
name: onboarding-pr
category: computing-software
field: devops-ci-cd
product: renovate
tags: [onboarding, onboarding-pr, installing, renovate]
level: intro
status: docs-checked
description: "What the Renovate onboarding PR contains, how to change it, and the global options that control onboarding."
sources:
  - https://docs.renovatebot.com/getting-started/installing-onboarding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When Renovate first runs on a repository without a config file, it opens a "Configure Renovate" pull request that adds a `renovate.json` with suggested defaults. Renovate makes no changes and raises no further PRs until you merge it. You can edit the config on the `renovate/configure` branch and Renovate keeps updating the PR description to match.

- Closing the onboarding PR without merging opts the repository out. It is reversible: rename the closed PR, or commit a Renovate config file to the default branch.
- Fix warnings and errors on the base branch so Renovate can recreate its PR on the next cycle.
- Renovate may add overrides to the defaults, such as Angular-style semantic commits if the repository uses them, or range pinning depending on whether the project looks like an app or a library.
- Alternative config locations include `renovate.json5`, `.github/renovate.json`, `.gitlab/renovate.json`, `.renovaterc` and a deprecated `package.json` section.
- Self-hosters can enable the `onboardingRebaseCheckbox` option to add a rebase/retry checkbox to the PR.
- To change config later, push a branch named `renovate/reconfigure`; Renovate comments on the PR with the expected changes. To re-onboard, rename the original PR and remove the current config file from the default branch.

Self-hosting on Windows: the docs recommend `git config --global core.autocrlf input` (or `* text=auto eol=lf` in `.gitattributes`), because carriage returns may confuse Renovate.

## Checked

2026-11-03. Confirmed against the Renovate "Installing and onboarding Renovate into repositories" page. Removed the other admin options (`onboarding`, `onboardingConfig`, `onboardingBranch`, `onboardingPrTitle`, `onboardingCommitMessage`, `onboardingConfigFileName`, `onboardingNoDeps`, `onboardingAutoCloseAge`) and the example block, which are not on the fetched pages, and the claim that the PR lists detected package files.

Method: documentation only; no commands were run.
