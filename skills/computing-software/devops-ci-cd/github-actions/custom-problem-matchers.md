---
id: computing-software.devops-ci-cd.github-actions.custom-problem-matchers
name: custom-problem-matchers
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, problem-matcher-json, custom-problem-matcher, add-matcher, annotations-from-logs]
level: practitioner
status: docs-checked
description: "Turn compiler and linter output into file/line annotations on PRs with a problem matcher JSON registered via ::add-matcher::, including multi-line patterns and limits."
sources: ["https://github.com/actions/toolkit/blob/main/docs/problem-matchers.md", "https://github.com/actions/toolkit/blob/main/docs/commands.md#problem-matchers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom problem matchers

**Goal:** lint/test failures show inline on the PR diff without writing a reporter action.

## 1. Single-line format (e.g. `src/app.py:12:5: E501 line too long`)
```json
{
  "problemMatcher": [{
    "owner": "flake8",
    "severity": "error",
    "pattern": [{
      "regexp": "^(.+?):(\\d+):(\\d+): ([A-Z]\\d+) (.*)$",
      "file": 1, "line": 2, "column": 3, "code": 4, "message": 5
    }]
  }]
}
```
```yaml
- run: echo "::add-matcher::.github/matchers/flake8.json"
- run: flake8 src
- if: always()
  run: echo "::remove-matcher owner=flake8::"
```

## 2. Multi-line (file header, then indented problems — eslint "stylish")
```json
{ "problemMatcher": [{ "owner": "eslint-stylish", "pattern": [
  { "regexp": "^([^\\s].*)$", "file": 1 },
  { "regexp": "^\\s+(\\d+):(\\d+)\\s+(error|warning|info)\\s+(.*)\\s\\s+(.*)$",
    "line": 1, "column": 2, "severity": 3, "message": 4, "code": 5, "loop": true }
]}]}
```
`loop: true` on the last pattern keeps matching consecutive lines for the same file.

## 3. Details
- Fields: `owner` (required, used to remove or replace the matcher) and `severity` (default `warning` or
  `error`, defaulting to `error`) at matcher level; per pattern `regexp` (required), `file`, `fromPath`, `line`,
  `column`, `severity` (a group holding `warning` or `error`), `code`, `message` (at least one pattern must set it)
  and `loop` (only valid on the last pattern of a multi-pattern matcher).
- The file must exist under the workflow's repository, otherwise the `file` property is dropped (enable debug
  logging to see why). `fromPath` roots the file against a project-file path.
- Multi-line patterns must match on consecutive lines.
- Registering two matchers with the same owner means only the last registered one runs.
- Limits: 10 warning, 10 error and 10 notice annotations per step, and 50 annotations per job; if your output may
  exceed these, filter what the matcher sees.
- JSON escaping: `\\d` in JSON is `\d` in the regex. Patterns use ECMAScript regular expression syntax.
- setup-node, setup-python, setup-go and setup-dotnet already use problem matchers.

## Verify
- [ ] Introduce a deliberate lint error: annotation appears on the right file/line in "Files changed".
- [ ] After `remove-matcher`, later steps' output is not annotated.

## Checked

Date: 2026-10-25. Documentation release: actions/toolkit docs (main).
- Matcher fields, severity default, loop rule, consecutive-line rule, same-owner replacement, annotation limits (10 warning, 10 error, 10 notice per step; 50 per job), ECMAScript regex, and which setup actions ship matchers: confirmed in actions/toolkit docs/problem-matchers.md.
- ::add-matcher:: and ::remove-matcher:: command forms: confirmed in actions/toolkit docs/commands.md (the owner= argument form is the documented remove syntax).
- Removed unconfirmed claims about silent dropping of extra annotations, container path prefixes and the matcher scope remark.

Method: documentation only; no commands were run.
