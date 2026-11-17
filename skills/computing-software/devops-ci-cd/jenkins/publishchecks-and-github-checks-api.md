---
id: computing-software.devops-ci-cd.jenkins.publishchecks-and-github-checks-api
name: publishchecks-and-github-checks-api
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, publish-checks, github-checks, commit-status]
level: practitioner
status: docs-checked
description: "Report Jenkins results as GitHub check runs with the Checks API plugin: automatic junit/warnings checks, custom publishChecks, and skipping duplicate status checks."
sources: ["https://plugins.jenkins.io/checks-api/", "https://plugins.jenkins.io/github-checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# publishChecks and the Checks API

With `checks-api` + `github-checks` and a **GitHub App** credential on the branch source, Jenkins
publishes check runs (not just commit statuses) to PRs.

## Automatic checks
- Statuses (pending, in progress, completed) are published at build stages; consuming
  plugins such as `junit` publish their own checks.
- `junit skipPublishingChecks: true, testResults: '...'` disables the junit check.

## Custom checks
```groovy
publishChecks name: 'Security scan', title: 'Trivy',
  summary: "${critical} critical vulnerabilities",
  text: readFile('trivy-summary.md'),
  conclusion: critical == 0 ? 'SUCCESS' : 'FAILURE',
  detailsURL: env.BUILD_URL,
  annotations: [[path: 'Dockerfile', startLine: 1, endLine: 1,
                 annotationLevel: 'WARNING', message: 'base image outdated']]
```
The valid `conclusion` and annotation-level values are listed in the Checks API plugin docs
and the `publishChecks` step reference in Pipeline Syntax; confirm there.

`withChecks('Integration') { ... }` publishes an in-progress check immediately; consuming
plugins then publish the final check. `withChecks(name: 'Tests', includeStage: true)` also
includes the stage name.

## Gotchas
- Only GitHub Apps with Checks read/write permission can publish checks.
- Branch protection lists each check name separately; keep names stable (set per job
  under Status Checks Properties).
- GitHub Branch Source also sends status notifications through the Status API; disable
  them with the "Skip GitHub Branch Source notifications" behaviour if you see duplicates.

## Verify
- [ ] PR "Checks" tab shows the named check with summary and annotations.

## Checked
2026-11-02. Confirmed against the Checks API and GitHub Checks plugin pages and the JUnit plugin page: publishChecks parameters name, title, summary, text, detailsURL; withChecks behaviour and includeStage; GitHub App requirement; junit skipPublishingChecks; per-job check names and duplicate Status API notifications. Removed: status and conclusion enumerations, checksName rename, recordIssues claim, error text, annotation cap.
Method: documentation only; no commands were run.
