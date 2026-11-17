---
id: computing-software.devops-ci-cd.github-actions.rulesets-and-required-checks
name: rulesets-and-required-checks
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, rulesets, branch-protection, required-status-checks, required-workflows, two-person-review, required-reviewers, codeowners, code-owner-review, dismiss-stale-reviews, require-last-push-approval, linear-history, signed-commits, push-rulesets, tag-rulesets, bypass-list, merge-queue, required-checks-naming, skipped-checks, slsa-source-track, repository-rules-api, enforcement-evaluate]
level: practitioner
status: docs-checked
description: "Enforce review and CI gates with GitHub rulesets: required status checks, review rules, push rulesets and merge queue triggers."
sources: ["https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets", "https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#require-workflows-to-pass-before-merging", "https://slsa.dev/spec/v1.1/source-requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rulesets and required checks

**Goal:** nothing reaches `main` without passing CI and a second human — enforced by the
platform, not by convention, across every repo in the org.

## 1. Rulesets
- Rulesets can target repositories across an organisation, including by custom property, and support bypass lists.
- **Evaluate** enforcement mode lets you monitor which actions would or would not violate rules on the Rule Insights page before enforcing (Evaluate needs GitHub Enterprise).
- Rules in the available-rules page include: Block force pushes, Require linear history, Require signed commits, Require deployments to succeed before merging, Require code scanning results, and the pull request rule with *Dismiss stale pull request approvals when new commits are pushed*, *Require review from Code Owners* and *Require approval of the most recent reviewable push*.
- *Require branches to be up to date before merging* only takes effect when you define a status check.

## 2. Required status checks
- In the rules API a required check is a `context` name plus an optional `integration_id` (the app it must come from), and `strict_required_status_checks_policy` controls the up-to-date requirement. Treat required check names as a stable interface: renaming a job changes the name the rule looks for.
- Prefer one always-running aggregate job (`if: always()`, `needs: [...]`, inspect `needs.*.result`) as the only required check, so path filters and matrix changes do not leave a required name missing.
- Checks that need secrets will not have them on fork PRs; do not make them required.

## 3. Review gates
- CODEOWNERS plus *Require review from Code Owners* means a PR touching owned content needs that owner's approval; cover every path with an owner.
- Dismiss stale approvals together with approval of the most recent reviewable push so an approval binds to the content that merges.
- Keep the bypass list empty or minimal for production branches.

## 4. Push rulesets
Push rulesets can block pushes by file extension, file path length, file and folder path (fnmatch syntax) and file size, and they apply to the repository's whole fork network. Use them to protect `.github/workflows/**` or block key file extensions.

## 5. Merge queue and `merge_group`
If a repository uses a merge queue, code scanning and other workflows need the `merge_group` event as an extra trigger so queued PRs run them:
```yaml
on:
  pull_request:
  merge_group:
```

## Verify
- [ ] Ruleset moved to *Active* after an *Evaluate* soak with no unexpected blocks.
- [ ] A PR with a doc-only change still merges (aggregate check reports).
- [ ] Renaming a non-required job does not block PRs; renaming the aggregate job is caught by a test PR.
- [ ] Attempting a direct push to `main` as an admin is rejected.
- [ ] `merge_group` runs appear for queued PRs (if a merge queue is used).

## Checked
2026-10-28. Confirmed in the available-rules, creating-rulesets and REST organisation rules pages: Evaluate mode and Rule Insights (Evaluate needs Enterprise); block force pushes, linear history, signed commits, deployments, code scanning results; dismiss stale approvals, code owner review, approval of most recent reviewable push; up-to-date check needs a defined check; `context`, `integration_id`, `strict_required_status_checks_policy` fields; push rulesets by extension, path length, path (fnmatch) and size across the fork network; `merge_group` trigger note from the code scanning docs.
Removed (not confirmed): the claim that the strictest ruleset wins, approval counts for regulated teams, skipped-job and path-filter reporting behaviour, org required-workflow plan availability and `@main` pinning advice, audit-log event name, SLSA source track (page 404), tag ruleset and immutable release interplay, `gh-readonly-queue` branch pattern, Terraform resource names and the GitHub App permission.

Method: documentation only; no commands were run.
