---
id: computing-software.devops-ci-cd.gitlab-ci.debugging-pipelines-and-job-logs
name: debugging-pipelines-and-job-logs
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, pipeline-debugging, ci-debug-services, job-log, job-log-sections, section-start, collapsible-sections, ci-lint, pipeline-editor, full-configuration, workflow-name, yaml-invalid, no-pipeline, rules-debugging, simulate-pipeline, raw-log, ff-timestamps]
level: practitioner
status: docs-checked
description: "Debug GitLab CI: pipeline not created or duplicated, CI Lint simulation, collapsible log sections, timestamps, workflow:name, and common config errors."
sources: ["https://docs.gitlab.com/ci/debugging/", "https://docs.gitlab.com/ci/yaml/lint/", "https://docs.gitlab.com/ci/pipeline_editor/", "https://docs.gitlab.com/ci/jobs/job_logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging pipelines and job logs

**Goal:** diagnose "no pipeline", "wrong jobs ran" and "it works locally" in minutes,
without leaking secrets in the process.

## 1. Syntax first
- A syntax problem shows a `yaml invalid` badge and the pipeline does not start.
- The pipeline editor is the recommended editing experience: keyword completion, validation and
  a visualisation of the file. Editors with Schemastore support use the GitLab CI/CD schema.
- CI Lint checks pasted snippets; when a `.gitlab-ci.yml` exists in the project it can also
  **simulate** creating a full pipeline for deeper verification. The pipeline editor's *Full
  configuration* tab shows the expanded configuration (after `include` and `extends`).
- Give every pipeline type a readable name with `workflow:name` and `workflow:rules:variables`
  so the pipeline list shows "Merge request pipeline" and so on.

## 2. No pipeline, or the wrong jobs
- A pipeline does not run if no jobs are added after evaluating `rules`, `only/except` and
  `workflow:rules`. If the wrong type ran (branch instead of merge request), check the rules.
- A pipeline with only `.pre` and `.post` jobs does not run.
- Do not mix `rules` with `only/except` in one pipeline; `rules` is preferred.
- `changes:` is always true in some pipeline types, including scheduled and tag pipelines; pair
  it with an `if` that limits it to branch or merge request pipelines.
- Two pipelines on a branch with an open MR are usually a branch pipeline plus an MR pipeline,
  caused by `rules`; fix with `workflow:rules`. The warning "Job may allow multiple pipelines to
  run for a single action" appears when a `rules` entry has `when` but no `if`.
- A UTF-8 byte order mark in `.gitlab-ci.yml` can drop config silently; the pipeline editor
  cannot display it, so check with an external tool.
- Pipelines with more jobs than the instance limit fail to start; split into parent-child
  pipelines. Rule evaluation that takes too long fails with `seed_timeout`: "Pipeline creation
  timed out while evaluating rules" (remove always-excluded jobs or reduce `parallel:matrix`).
- "The parsed YAML is too big": reduce includes and repeated script, use child pipelines.
- `config contains unknown keys` means a typo or wrong indentation. A job needs `script` or
  `trigger`.
- Several `!reference` tags in one array work for `script`, `rules` and `stages` only.

## 3. Reading logs
- Collapsible sections: print `\e[0Ksection_start:UNIX_TIMESTAMP:NAME\r\e[0KHEADER` and
  `\e[0Ksection_end:UNIX_TIMESTAMP:NAME\r\e[0K` from `script`; add `[collapsed=true]` after the
  name to collapse by default. The name may use only letters, numbers, `_`, `.` and `-`. The
  `0` in `\e[0K` is required.
- *Show complete raw* in the log page shows the markers.
- `FF_SCRIPT_SECTIONS` (bash only, introduced 16.5, off by default) turns multi-line script
  commands into collapsible sections.
- Log lines carry ISO 8601 timestamps by default; GitLab says they add about 10% log storage.
  `FF_TIMESTAMPS: false` disables them (Runner 18.7 or later required for this control).
- A running job's log can lag up to 60 seconds on first view, then about 3 seconds.
- `CI_DEBUG_SERVICES: "true"` streams service container logs into the job log, and can reveal
  masked variables, so use it only while debugging.

## 4. Techniques that cost little
- Export the variables available in a failing job and compare with what you expect.
- Add an empty-by-default variable such as `DEBUG_VARS` to a command, then run the pipeline
  manually with `--verbose`.
- Print dependency versions in `before_script`; pin images (`alpine:$ALPINE_VERSION`, not
  `latest`) and update deliberately.
- Prefer `--verbose` over `--silent`; save tool output as artifacts (never tokens or
  passwords) and list `reports:` files in `paths:` if you want to download them.
- Reproduce the job's script inside its container image locally.

## 5. Common messages
- Failed to pull image from another project's registry: the job token allowlist of the image
  project must list the running project; project access tokens cannot reach other projects.
- Intermittent pull failures: runners cache images, so users without access to the image
  project fail only on runners that have never cached it.
- `Project <group/project> not found or access denied` with `include`: check the path format
  and that the running user is a member.

## Verify
- [ ] CI Lint simulation shows the expected job set.
- [ ] Full configuration confirms template rules were kept or replaced as intended.
- [ ] No debug variable remains on shared branches.

## Checked
2026-10-31. Confirmed on the Debugging CI/CD pipelines, Job logs and Pipeline editor pages:
everything listed above. Removed as unconfirmed on the fetched pages: CI_DEBUG_TRACE, glab
commands, jobs and lint API calls and failure_reason values, runner-stuck diagnosis, runner debug
flags, shell and after_script semantics, log size cap, gitlab-runner exec removal.
Method: documentation only; no commands were run.
