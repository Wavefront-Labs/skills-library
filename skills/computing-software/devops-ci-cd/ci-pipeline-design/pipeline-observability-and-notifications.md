---
id: computing-software.devops-ci-cd.ci-pipeline-design.pipeline-observability-and-notifications
name: pipeline-observability-and-notifications
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, pipeline-observability, ci-dashboards, pipeline-notifications, proactive-notification, alert-fatigue, prometheus, opentelemetry-ci]
level: practitioner
status: docs-checked
description: "Instrument the pipeline and notify well: GitLab and Jenkins Prometheus exporters, OpenTelemetry CI/CD conventions, DORA guidance on thresholds and alert fatigue."
sources: ["https://dora.dev/capabilities/monitoring-and-observability/", "https://dora.dev/capabilities/proactive-failure-notification/", "https://github.com/mvisonneau/gitlab-ci-pipelines-exporter", "https://plugins.jenkins.io/prometheus/", "https://opentelemetry.io/docs/specs/semconv/cicd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline observability and notifications

**Goal:** answer "is CI getting slower or flakier, and why?" from data, and tell the people
who can fix a broken build without drowning them.

## 1. Getting pipeline data out
- **GitLab:** `gitlab-ci-pipelines-exporter` monitors GitLab CI pipelines with Prometheus or
  any OpenMetrics-capable system. Its README example metrics include
  `gitlab_ci_pipeline_last_run_duration_seconds`, `gitlab_ci_pipeline_last_run_id` and
  `gitlab_ci_pipeline_last_run_status`, labelled by project and ref.
- **Jenkins:** the Prometheus plugin exposes an endpoint (default `/prometheus/`) that a
  Prometheus server can scrape.
- **OpenTelemetry:** the CI/CD semantic conventions define spans and metrics for CI/CD
  (the index page links to separate span and metric specifications). Read those pages for
  attribute names before emitting anything.

## 2. Monitoring principles (DORA monitoring and observability)
- The three common data types are metrics, logs and traces; a trace is built from spans with
  a shared parent.
- Avoid **cause-based alerting** (an alert for every possible error condition). Prefer
  **symptom-based alerting**, which fires when a user-facing symptom is visible or predicted;
  user-facing includes internal users. For CI, treat the developers waiting on the pipeline as
  the users (judgement).
- Give alerts several delivery paths; emailing a whole distribution list leads to diffusion of
  responsibility and ignored alerts. Too many non-actionable alerts cause alarm fatigue.
- Track methods that silence or suppress alerts so they are not too broad or used too often.

## 3. Notifications (DORA proactive failure notification)
- Use alerting rules with thresholds that actually predict a problem: find the level at which
  users are affected and alert at some percentage before it (their example: within 20% of the
  response time at which users get frustrated).
- Hold post-mortems and monitor the indicators that could have predicted the incident.
- If a notification needs no action or the same action every time, automate the response.
  Review notifications regularly and delete those nobody can act on. Disabling all alerts is
  bad practice.
- Measure with at least two methods: a threshold over a time window and a rate-of-change
  rule.
- Notify the people and teams who can fix the problem.

## Verify
- [ ] Pipeline duration and status are exported to a system you can chart over time.
- [ ] Every notification has an owner and an action; unactionable ones are removed.
- [ ] Alert suppression is tracked.

## Checked
Confirmed 2026-11-09 against the DORA proactive failure notification page (read in full), the DORA monitoring and observability page (alerting section, lines 200-224, and the metrics/logs/traces overview), the gitlab-ci-pipelines-exporter README (purpose and example metrics), the Jenkins Prometheus plugin page (default endpoint) and the OpenTelemetry CI/CD conventions index, from local text copies. The OpenTelemetry page fetched was only an index, so no attribute names are stated.
Removed as unconfirmed: the five-metric table with its "healthy" targets, GitHub Actions API and exporter advice, the Jenkins metric names, the otel-export-trace-action and otel-cli use and example, `cicd.*` attribute names, test-level telemetry store options, SLO numbers, notification routing recipes for GitHub, GitLab and Jenkins, and the 15-minute stop-the-line policy. The otel-export-trace-action source was never read and was dropped from `sources`.
Method: docs-checked 2026-11-09 against dora.dev monitoring-and-observability and proactive-failure-notification, the gitlab-ci-pipelines-exporter README, plugins.jenkins.io prometheus, opentelemetry.io cicd semconv
