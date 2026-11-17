---
id: computing-software.devops-ci-cd.gitlab-ci.pipeline-cancel-retry-and-delete-via-api
name: pipeline-cancel-retry-and-delete-via-api
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, pipelines-api-cancel, retry-pipeline-api, delete-pipelines, glab-ci, jobs-api-play]
level: practitioner
status: docs-checked
description: "Operate pipelines from scripts: cancel, retry, delete pipelines and play/retry/erase jobs with the REST API and glab ci, plus bulk cleanup of old pipelines."
sources: ["https://docs.gitlab.com/api/pipelines/", "https://docs.gitlab.com/api/jobs/", "https://gitlab.com/gitlab-org/cli/-/tree/main/docs/source/ci"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancel, retry and delete pipelines via API

## 1. Pipelines
```bash
API="$CI_API_V4_URL/projects/$PID"; H="PRIVATE-TOKEN: $T"
curl -s -H "$H" "$API/pipelines?ref=main&status=running" | jq '.[].id'
curl -X POST   -H "$H" "$API/pipelines/$P/cancel"      # cancels running/pending jobs
curl -X POST   -H "$H" "$API/pipelines/$P/retry"       # retries failed and canceled jobs
curl -X DELETE -H "$H" "$API/pipelines/$P"             # Owner role; deletes jobs, logs, artifacts
```
List filters: `ref`, `sha`, `status`, `source`, `updated_before`, `username`, `name`, `scope` (`running|pending|finished|branches|tags`).

## 2. Jobs
```bash
curl -X POST -H "$H" "$API/jobs/$J/play"                     # start a manual job
curl -X POST -H "$H" "$API/jobs/$J/play" --json '{"job_variables_attributes":[{"key":"TARGET","value":"eu"}]}'
curl -X POST -H "$H" "$API/jobs/$J/retry"
curl -X POST -H "$H" "$API/jobs/$J/cancel"
curl -X POST -H "$H" "$API/jobs/$J/erase"                    # remove log + artifacts (leaked secret!)
```

## 3. glab
The GitLab CLI has `glab ci` subcommands for the same operations; check `glab ci --help` for the flags in your version (not verified here).

## 4. Bulk cleanup
```bash
# delete pipelines older than 180 days (paginate, throttle)
curl -s -H "$H" "$API/pipelines?updated_before=$(date -u -d '180 days ago' +%FT%TZ)&per_page=100" |
  jq -r '.[].id' | while read p; do curl -s -X DELETE -H "$H" "$API/pipelines/$p"; sleep 0.2; done
```

## Gotchas
- Only one retry of a pipeline runs at a time; a second call returns 409 Conflict.

## Verify
- [ ] `pipelines?status=running` empty after cancel; deleted pipelines 404.

## Checked

2026-11-02. Confirmed: cancel, retry, delete pipeline endpoints (delete needs the Owner role), list filters including `scope` values and `updated_before`, job play/retry/cancel/erase endpoints, `job_variables_attributes`, 409 on concurrent retry (GitLab Pipelines and Jobs API docs). Removed: glab command forms, automatic pipeline cleanup menu path, CI_JOB_TOKEN, original-YAML and async-cancel claims.

Method: documentation only; no commands were run.
