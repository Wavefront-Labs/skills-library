---
id: computing-software.devops-ci-cd.gitlab-ci.jobs-api-and-failure-reasons
name: jobs-api-and-failure-reasons
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, jobs-api, failure-reason, rest-api, jq, triage]
level: practitioner
status: docs-checked
description: "Query GitLab CI job and pipeline status through the REST jobs API, read failure_reason values, and script failure triage with jq."
sources: ["https://docs.gitlab.com/api/jobs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jobs API and failure reasons

**Goal:** find which jobs failed and why, programmatically.

## Calls
```bash
API="https://gitlab.example.com/api/v4"; H="PRIVATE-TOKEN: $GITLAB_TOKEN"
curl -sH "$H" "$API/projects/$PID/pipelines/$PIPE/jobs?scope[]=failed" \
 | jq -r '.[] | [.id,.name,.stage,.failure_reason,.runner] | @tsv'
curl -sH "$H" "$API/projects/$PID/jobs/$JOB/trace" | tail -n 80     # job log
curl -sH "$H" -X POST "$API/projects/$PID/jobs/$JOB/retry"
```
- Use a token with the scope each endpoint's docs require; never print the token.
- `scope[]` filters (for example `pending`, `running`) are documented on the jobs endpoints; paginate large listings.
- `GET /projects/:id/jobs` lists all jobs; the pipeline-scoped endpoint is cheaper.

## failure_reason values worth knowing
`script_failure` (script failed, or the runner could not pull the image on some executors), `runner_system_failure` (runner problem, retry-able), `api_failure`, `unmet_prerequisites`, `data_integrity_failure`, `stale_schedule`, and the timeout reasons `no_updates_running`, `server_timeout_running`, `stuck_pending_with_matching_runners`, `stuck_pending_no_matching_runners`. In the GitLab docs version checked, `stuck_or_timeout_failure` and `job_execution_timeout` are deprecated in 19.1 in favour of those values, and some `runner_system_failure` / `script_failure` cases move to `runner_external_dependency_failure`, `runner_interrupted` and `runner_configuration_error`. The exact set varies by version; read it from your instance's `retry:when` docs.

## Use it
- `retry: { max: 2, when: [runner_system_failure, no_updates_running] }` in YAML retries only infrastructure-type failures, never script failures. (`stuck_or_timeout_failure` still works on older versions but is deprecated from 19.1.)
- Group failures by `failure_reason` and runner to separate flaky infra from code bugs.

## Verify
Counts per `failure_reason` match the pipeline page.

## Checked

2026-11-02. Confirmed: failure_reason values and the 19.1 deprecations/splits listed above (GitLab CI/CD YAML reference, retry:when); jobs list and trace endpoints, retry endpoint (GitLab Jobs API). Removed: `read_api`/`api` scope claim, `missing_dependency_failure`, runner description field, pagination header claim. Note: the retry example in the original used a value now deprecated.

Method: documentation only; no commands were run.
