---
id: computing-software.devops-ci-cd.build-systems.auto-merging-minor-dependency-updates
name: auto-merging-minor-dependency-updates
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, dependency-pinning, automerge-minor, automerge, renovate-automerge, dependabot-automerge, gh-pr-merge-auto, platformautomerge, merge-queue, required-checks, minimumreleaseage, dependency-update-toil]
level: practitioner
status: docs-checked
description: "Safely auto-merge patch/minor dependency updates: Renovate automerge rules, Dependabot + gh pr merge --auto with fetch-metadata, required checks as the gate, and what never to automerge."
sources: ["https://docs.renovatebot.com/key-concepts/automerge/", "https://docs.renovatebot.com/configuration-options/", "https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions", "https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference", "https://github.com/dependabot/fetch-metadata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auto-merging minor dependency updates

Automerge is only as safe as the checks it waits for. Prerequisites: branch protection
/ ruleset with **required status checks** that run real tests, and preferably a merge
queue. Without them, automerge can merge untested code (Renovate's documentation warns
about this when `platformAutomerge` is on).

## Renovate
```json5
{
  packageRules: [
    {
      matchUpdateTypes: ["minor", "patch", "pin", "digest"],
      matchCurrentVersion: "!/^0/",          // 0.x minors can break: exclude
      automerge: true,
      automergeType: "pr",                   // or "branch": merge without a PR when green (less noise)
    },
    { matchDepTypes: ["devDependencies"], matchUpdateTypes: ["major"], automerge: false },
    { matchPackageNames: ["typescript", "/^@types//"], matchUpdateTypes: ["minor"], automerge: false },
  ],
  minimumReleaseAge: "3 days",               // let compromised/yanked releases surface first
  platformAutomerge: false,                  // needed for automergeSchedule to be honoured
  automergeSchedule: ["after 7am and before 5pm every weekday"],   // merge when humans are around
}
```
`platformAutomerge` defaults to true (use GitHub/GitLab native auto-merge); in that mode Renovate enqueues the merge when it creates the PR, so `automergeSchedule` cannot be followed. Renovate only automerges branches that are up to date with their target and green, so frequent commits to the default branch can keep deferring automerges. If you have no tests but still want automerge, Renovate requires `ignoreTests: true`, which is rarely wise.

## Dependabot (via a workflow)
```yaml
name: Dependabot auto-merge
on: pull_request
permissions: { contents: write, pull-requests: write }
jobs:
  automerge:
    if: github.event.pull_request.user.login == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - id: meta
        uses: dependabot/fetch-metadata@v3     # GitHub's docs pin this action to a commit SHA
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"
      - if: steps.meta.outputs.update-type != 'version-update:semver-major'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
`gh pr merge --auto` enables GitHub auto-merge: the PR merges when required reviews and status checks pass, and auto-merge must be enabled for the repository. GitHub recommends enabling **Require status checks to pass before merging** for the target branch. If the branch uses a merge queue, `GITHUB_TOKEN` cannot add pull requests to the queue; authenticate the workflow with a personal access token or GitHub App token instead.

## Never automerge
- Majors, and 0.x minors.
- Packages that run code at install/build with high privilege where a compromise is
  catastrophic (build plugins, CI actions) unless digest-pinned and aged.
- Anything with weak test coverage of the affected area.
- Security-sensitive libraries (auth, crypto) without a human glance.

## Guardrails
- Renovate's `minimumReleaseAge` (a "dependency cooldown") and Dependabot's `cooldown` option (version updates only) delay updates so hijacked releases that get yanked quickly never reach you.
- Monitor: a weekly report of automerged PRs; a broken main after automerge -> revert and
  add the package to the exclusion list.
- Keep merged updates small (grouped minor/patch per ecosystem) so bisecting is easy.

## Verify
A patch update PR opens, checks run, and it merges itself without human action; a major
update PR stays open awaiting review; a failing test blocks the automerge.

## Checked
Date: 2026-10-25. Documentation: Renovate docs sources (renovatebot/renovate `docs/usage/key-concepts/automerge.md`, `minimum-release-age.md`, `configuration-options.md`); GitHub docs "Automating Dependabot with GitHub Actions", "Automatically merging a pull request" and the Dependabot options reference (github/docs); dependabot/fetch-metadata README.
Confirmed: `matchUpdateTypes`, `matchCurrentVersion: "!/^0/"` pattern for excluding 0.x, `automergeType` (`pr` default, `branch`), `platformAutomerge` default true and its conflict with `automergeSchedule`, `minimumReleaseAge`, `ignoreTests`, up-to-date-and-green automerge rule; `fetch-metadata` `update-type` output and `version-update:semver-major`; `gh pr merge --auto`; required-status-checks and merge-queue notes; Dependabot `cooldown` (version updates only).
Fixed: the Renovate example combined `platformAutomerge: true` with `automergeSchedule`, which the documentation says cannot work together; `fetch-metadata` major version (v2 replaced by v3).
Removed: `gh pr review --approve` and the claim that approval by `GITHUB_TOKEN` counts toward required reviews (not in the pages read).
Method: documentation only; no commands were run.
