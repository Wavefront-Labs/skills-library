---
id: computing-software.devops-ci-cd.ci-pipeline-design.centralised-ci-log-shipping
name: centralised-ci-log-shipping
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, ci-log-shipping, pipeline-observability, job-log]
level: advanced
status: docs-checked
description: "Ship CI job logs to central storage (Loki, Elasticsearch, S3) for search and retention beyond the CI tool: export via APIs/webhooks, redaction and retention rules."
sources: ["https://docs.github.com/en/rest/actions/workflow-runs#download-workflow-run-logs", "https://docs.gitlab.com/administration/cicd/job_logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centralised CI log shipping

CI tools keep logs for limited periods (GitHub default 90 days, configurable; other tools have their own settings) and search across runs is poor.

## Collection patterns
1. **Webhook + fetch**: on `workflow_run`/`workflow_job` completed (GitHub) or job events (GitLab),
   a small service downloads logs:
   ```bash
   gh api repos/ORG/REPO/actions/runs/$RUN_ID/logs > run.zip       # zip of per-job logs
   # GitLab: fetch job logs through its jobs API (see the GitLab docs)
   ```
   then pushes lines to Loki/Elasticsearch with labels repo, workflow, job, run_id, sha, conclusion.
2. **Runner-side**: a node agent on self-hosted runners ships runner and job output. Good for runner health, not complete step logs.
3. **Jenkins**: use a logging plugin that stores build logs in an external backend.

## Redaction
Masking in the CI UI does not apply to raw downloads in all tools; secrets printed before masking
or transformed values are in the raw log. Run a redaction pass (a secret scanner or regex) before indexing and
restrict index access.

## Retention and cost
- Hot searchable for 30 days, archive (object storage with lifecycle rules) for compliance periods.
- Index only failed jobs fully; sample or drop successful verbose logs.

## Verify
- [ ] Searching an error string returns matching jobs across repos for the last 30 days; no secrets in sampled logs.

## Checked

2026-10-28. Confirmed: GitHub keeps build logs and artifacts for 90 days by default and the period is customizable (removing-workflow-artifacts page); the `workflow_job` webhook and `workflow_run` event exist; the REST `actions/runs/{run_id}/logs` endpoint downloads run logs. Removed: the 1-400 day range, the GitLab trace endpoint, `_diag`, the named agents and Jenkins plugins, and the gitleaks and S3 references.

Method: documentation only; no commands were run.
