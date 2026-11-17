---
id: computing-software.devops-ci-cd.gitlab-ci.glab-ci-trace-and-live-log-debugging
name: glab-ci-trace-and-live-log-debugging
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, glab-ci-trace, glab, job-logs, ci-debugging]
level: practitioner
status: gated
description: "Watch and capture GitLab CI job logs from the terminal with glab ci trace, status and view, and debug a failing job locally."
sources: ["https://gitlab.com/gitlab-org/cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glab ci trace

**Goal:** follow a running job's log, and find the failing line fast, without the browser.

## Commands (GitLab CLI)
```bash
glab auth login                      # once, per host
glab ci status                       # current branch pipeline summary
glab ci trace                        # pick a job interactively and stream its log
glab ci trace build                  # by job name (or by numeric job id)
glab ci view                         # interactive pipeline TUI
glab ci run -b main                  # new pipeline
glab ci retry <job-id>
```
Flags differ by version; run `glab ci trace --help`. The `glab ci` command forms above are unconfirmed (gated: unconfirmed, source is paywalled or blocked)

## Debug flow
1. `glab ci status` then `glab ci trace <failed-job>`: read from the first `ERROR`/non-zero exit.
2. GitLab supports custom collapsible sections in job logs; set `CI_DEBUG_TRACE: "true"` (debug logging) only in a private rerun and treat the log as sensitive.
3. Reproduce locally: run the job image (`docker run -it --rm <image> sh`), export the same variables, paste `script` lines.
4. Save logs: `glab ci trace build > build.log` (redirect only after checking for secrets).

## Gotchas
Treat logs as sensitive: derived or encoded forms of secrets are not masked.

## Verify
The log you read matches the web UI for the same job id.

## Checked

2026-11-02. Confirmed: `CI_DEBUG_TRACE` is the debug logging variable; collapsible sections and non-zero-exit handling are documented (GitLab CI/CD YAML reference and predefined variables). Gated: `glab ci` command forms (the glab docs on gitlab.com returned 403/stub). Removed: section_start marker, log-size truncation claim, masking statement.

Method: documentation only; no commands were run.
