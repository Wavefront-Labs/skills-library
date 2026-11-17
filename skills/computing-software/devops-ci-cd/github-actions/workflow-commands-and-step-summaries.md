---
id: computing-software.devops-ci-cd.github-actions.workflow-commands-and-step-summaries
name: workflow-commands-and-step-summaries
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, workflow-commands, github-output, github-env, github-path, github-step-summary, step-summary, add-mask, annotations, error-annotation, warning-annotation, notice-annotation, group-endgroup, log-grouping, problem-matchers, debug-command, stop-commands, environment-files, multiline-values, heredoc-delimiter, job-summary-markdown, mermaid-in-summary, checks-api]
level: practitioner
status: verified
description: "Drive the Actions runner from scripts: GITHUB_OUTPUT/ENV/PATH with multiline heredocs, ::add-mask, ::error annotations with file+line, log groups, problem matchers, Markdown job summaries."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions", "https://github.com/actions/toolkit/blob/main/docs/problem-matchers.md", "https://github.blog/news-insights/product-news/supercharging-github-actions-with-job-summaries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow commands and step summaries

**Goal:** scripts that hand values to later steps, hide secrets from logs, annotate PR
diffs with errors, and render a readable report on the run page — no custom action needed.

## 1. Environment files
```bash
echo "version=1.4.2"        >> "$GITHUB_OUTPUT"   # step output (needs step id)
echo "APP_ENV=staging"      >> "$GITHUB_ENV"      # env var for all LATER steps (not this one)
echo "$HOME/.local/bin"     >> "$GITHUB_PATH"     # prepended to PATH for later steps
```
Multiline values use a heredoc delimiter that cannot appear in the value:
```bash
delim="EOF_$RANDOM$RANDOM"      # evaluate ONCE: two separate $RANDOM expansions would differ
{
  echo "notes<<$delim"
  git log --oneline -20
  echo "$delim"
} >> "$GITHUB_OUTPUT"
```
The delimiter must not occur on a line of its own inside the value. GitHub's docs advise that a value
that is completely arbitrary should not use this format at all: write it to a file instead. (Running
`echo "a<<EOF_$RANDOM"; echo "EOF_$RANDOM"` gives two different numbers, so the heredoc never closes.)
PowerShell: `"version=1.4.2" | Out-File -FilePath $env:GITHUB_OUTPUT -Encoding utf8 -Append`.

## 2. Masking
```bash
TOKEN=$(vault read -field=token secret/ci)
echo "::add-mask::$TOKEN"
```
Masks the value in later log output. Register the mask **before** the value is printed or used in any
other workflow command (GitHub docs). Job outputs that contain secrets are redacted on the runner and
not sent, so to pass a masked secret between jobs store it somewhere and re-fetch it in the next job.

## 3. Annotations
```bash
echo "::error file=src/app.ts,line=42,col=7,endLine=42,title=Lint::Unused variable"
echo "::warning file=README.md,line=1::Spelling"
echo "::notice::Deployed to staging"
```
Annotations appear in the run summary and, for a `file` in the diff, on the PR. GitHub Actions is
limited to 10 warning annotations and 10 error annotations per step (Checks API docs); for large reports
use a problem matcher or the Checks API. `::error::` only creates the message; the step's exit code
decides pass or fail.

## 4. Groups and debug
```bash
echo "::group::npm install"; npm ci; echo "::endgroup::"
echo "::debug::cache key = $KEY"        # visible when the secret ACTIONS_STEP_DEBUG is true
```
`::stop-commands::<token>` … `::<token>::` disables command parsing while printing untrusted
output (prevents log content from issuing `::add-mask`/`::error` commands).

## 5. Problem matchers
Turn tool output into annotations automatically:
```json
{"problemMatcher":[{"owner":"eslint-compact","pattern":[{"regexp":"^(.+):\\sline\\s(\\d+),\\scol\\s(\\d+),\\s(Error|Warning|Info)\\s-\\s(.+)\\s\\((.+)\\)$","file":1,"line":2,"column":3,"severity":4,"message":5,"code":6}]}]}
```
`echo "::add-matcher::.github/matchers/eslint.json"` before the tool runs,
`::remove-matcher owner=eslint-compact::` after. The pattern above is the example from the actions/toolkit
problem-matcher docs (checked here against `src/app.ts: line 42, col 7, Error - Unused variable
(no-unused-vars)`); registering two matchers with the same `owner` leaves only the last one active.

## 6. Job summaries (`GITHUB_STEP_SUMMARY`)
```bash
{
  echo "## Test results"
  echo "| Suite | Passed | Failed |"
  echo "|---|---|---|"
  echo "| unit | $PASS | $FAIL |"
  echo '```mermaid'; echo 'pie title Coverage'; echo "  \"covered\" : $COV"; echo "  \"missed\" : $((100-COV))"; echo '```'
} >> "$GITHUB_STEP_SUMMARY"
```
Each step's summary is limited to **1 MiB**; above that the upload for the step fails with an error
annotation, without affecting the step's or job's status, and at most 20 step summaries are displayed per
job (GitHub docs). Summaries cannot be modified after the step finishes.

## 7. Checks API for anything bigger
Annotations beyond the per-step limit, or from a tool running elsewhere: the Checks API takes at most 50
annotations per request, and each update to the check run appends more
(`gh api -X PATCH repos/{o}/{r}/check-runs/{id}` repeatedly). Needs `checks: write`.

## Verify
- [ ] Step outputs and env changes use the `GITHUB_OUTPUT` / `GITHUB_ENV` files.
- [ ] Multiline outputs use random heredoc delimiters.
- [ ] Secrets fetched at runtime are masked before use and absent from logs.
- [ ] Lint errors appear inline on a PR diff; summary renders on the run page.
