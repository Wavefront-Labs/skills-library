---
id: computing-software.devops-ci-cd.github-actions.dependency-review-on-pull-requests
name: dependency-review-on-pull-requests
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, dependency-review, dependency-review-action, dependency-graph, vulnerable-dependencies, license-policy, allow-licenses, deny-licenses, openssf-scorecard, supply-chain-security, pr-gate]
level: practitioner
status: docs-checked
description: "Block PRs that add vulnerable or badly licensed dependencies with actions/dependency-review-action: severity, license allow/deny lists, scopes, org-wide config and exceptions."
sources: ["https://github.com/actions/dependency-review-action", "https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review", "https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/configuring-the-dependency-review-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency review on pull requests

The dependency review action diffs the dependency graph between the PR base and head
(manifests + lockfiles) and fails if the PR **introduces** packages with known
vulnerabilities (GitHub Advisory Database) or disallowed licences. See the about-dependency-review page for prerequisites.

```yaml
name: Dependency review
on: pull_request
permissions:
  contents: read
  pull-requests: write        # only if comment-summary-in-pr is used
jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high               # low | moderate | high | critical
          fail-on-scopes: runtime              # runtime, development, unknown
          allow-licenses: MIT, Apache-2.0      # only one of allow-licenses / deny-licenses; deny-licenses is deprecated
          allow-dependencies-licenses: pkg:npm/some-internal-lib
          allow-ghsas: GHSA-xxxx-xxxx-xxxx     # accepted risk, with a ticket
          comment-summary-in-pr: on-failure
          show-openssf-scorecard: true
```

## Org-wide policy
Put options in a shared file and reference it so every repo applies the same rules:
```yaml
        with:
          config-file: acme/security-policies/.github/dependency-review-config.yml@main
```
(External repo config needs a token with read access via `external-repo-token` when
private.) A repository ruleset can set the dependency review action as a required workflow, so PRs merge only once it passes.

## Gotchas
- The action compares base and head of a pull request; for events other than `pull_request` and `pull_request_target`, pass `base-ref` and `head-ref`.
- `allow-dependencies-licenses` takes packages in purl format and excludes them from licence checks; `allow-ghsas` skips listed advisories (record why).

## Verify
On a test PR add a dependency version with a known advisory; the job fails listing the advisory, and the PR comment shows the summary.

## Checked
2026-10-28. Confirmed in the action README and the configure-dependency-review-action page: option names `fail-on-severity` (low, moderate, high, critical), `fail-on-scopes` (runtime, development, unknown), `allow-dependencies-licenses` (purl list), `allow-ghsas`, `comment-summary-in-pr` (always, on-failure, never; needs pull-requests: write), `show-openssf-scorecard`, `config-file`, `external-repo-token`, `base-ref`/`head-ref`; only one of allow-licenses and deny-licenses may be used; required-workflow use through repository rulesets.
Fixed: `deny-licenses` is marked deprecated in the README, so the example now uses `allow-licenses`.
Removed (not confirmed): the Code Security requirement for private repos, the lockfile and Gradle/C++ gotchas with submission action names, the strict allow-licenses remark, the scorecard threshold value, the lodash version.

Method: documentation only; no commands were run.
