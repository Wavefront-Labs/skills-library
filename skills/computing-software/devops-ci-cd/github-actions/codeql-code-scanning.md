---
id: computing-software.devops-ci-cd.github-actions.codeql-code-scanning
name: codeql-code-scanning
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, codeql, code-scanning, sast, codeql-action, default-setup, advanced-setup, security-extended, build-mode, sarif, security-events, query-packs, codeql-cli, alert-triage]
level: practitioner
status: docs-checked
description: "Run CodeQL code scanning in GitHub Actions: default vs advanced setup, build-mode per language, query suites, PR gating via rulesets, SARIF uploads and dismissing false positives."
sources: ["https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql", "https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/customizing-your-advanced-setup-for-code-scanning", "https://github.com/github/codeql-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodeQL code scanning

Licensing for private repositories: see the GitHub Docs about-CodeQL page (GitHub Code Security).

## Default vs advanced setup
Default setup needs no workflow YAML; use advanced setup (a workflow file like the one below) when you need to control the build, queries or config.

## Advanced setup workflow
```yaml
name: CodeQL
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
  schedule: [{ cron: '23 4 * * 1' }]
permissions:
  contents: read
  security-events: write      # upload results
jobs:
  analyze:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - { language: javascript-typescript, build-mode: none }
          - { language: python,               build-mode: none }
          - { language: java-kotlin,          build-mode: manual }
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v4
        with:
          languages: ${{ matrix.language }}
          build-mode: ${{ matrix.build-mode }}
          queries: security-extended          # or security-and-quality
          config-file: .github/codeql/codeql-config.yml
      - if: matrix.build-mode == 'manual'
        run: ./mvnw -B -DskipTests package
      - uses: github/codeql-action/analyze@v4
        with: { category: "/language:${{ matrix.language }}" }
```
- `build-mode` takes `none`, `autobuild` or `manual`; with `manual` you run the build between init and analyze. See the workflow configuration options page for which languages support which mode.
- Config file: `query-filters`, extra `packs` (for example `my-company/my-java-queries@~7.8.9`).
- Pin actions by SHA in hardened repos; `@v4` shown for readability.

## Gating PRs
- Make it blocking with the ruleset rule **Require code scanning results** (see available rules for rulesets for its thresholds).

## Triage
- Dismiss alerts with a comment explaining why.
- Recurring false positives from one query: exclude it in the config with
  `query-filters: - exclude: { id: js/xyz }` instead of dismissing repeatedly.

## Gotchas
- Advanced setup workflows must have `security-events: write`; private repositories also need `contents: read`.
- With a merge queue, add the `merge_group` event as a trigger so queued PRs are scanned.

## Verify
Open a PR with a deliberately insecure pattern in a test branch: the PR shows a CodeQL alert; remove it and the alert closes.

## Checked
2026-10-28. Confirmed in the GitHub Docs CodeQL pages and the codeql-action README: language identifiers `javascript-typescript` and `java-kotlin`; `build-mode` values and `autobuild`; `queries: security-extended` / `security-and-quality`; `config-file`, `packs`, `query-filters` with `exclude: id`; `security-events: write` (plus `contents: read` for private repos); `category` input; `merge_group` note; ruleset rule "Require code scanning results"; v4 action tags in current examples.
Fixed: examples moved from `@v3` to `@v4`.
Removed (not confirmed): free-for-public wording, the "High or higher" threshold names, dismissal reason list, Copilot Autofit mention, "Resource not accessible" and compiled-language tips, the cron and exact config keys `paths`/`paths-ignore` in the config file.

Method: documentation only; no commands were run.
