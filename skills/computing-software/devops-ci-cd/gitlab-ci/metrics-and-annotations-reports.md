---
id: computing-software.devops-ci-cd.gitlab-ci.metrics-and-annotations-reports
name: metrics-and-annotations-reports
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, metrics-report, annotations-report, artifacts-reports, merge-request-widget, external-link]
level: practitioner
status: docs-checked
description: "Use artifacts reports metrics (OpenMetrics-style text compared against the target branch) and annotations (external links on the job page) in GitLab CI."
sources: ["https://docs.gitlab.com/ci/testing/metrics_reports/", "https://docs.gitlab.com/ci/yaml/artifacts_reports/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics and annotations reports

## Metrics report (Premium and Ultimate)
Plain text, one metric per line `<name> <value>`; the OpenMetrics text format meets this requirement.
```yaml
metrics:
  stage: test
  script:
    - echo 'memory_usage_bytes 2621440' > metrics.txt
    - echo 'response_time_seconds 0.234' >> metrics.txt
    - echo '# EOF' >> metrics.txt
  artifacts:
    reports:
      metrics: metrics.txt
```
- The MR widget compares the source branch pipeline with the target branch baseline: added, removed, changed, unchanged. Values are compared as strings.
- If the baseline pipeline has no metrics artifact, every metric shows as new. Run the job on the default branch too.
- The widget appears only when the source pipeline has completed with the artifact.

## Annotations report
A JSON file of named sections, each a list of annotations keyed by type. The supported type is `external_link` with `label` and `url`.
```json
{ "preview": [ { "external_link": { "label": "Review app", "url": "https://review.example.com/" } } ] }
```
```yaml
artifacts:
  reports:
    annotations: annotations.json
```
Each link appears on the job output page.

## Gotchas
Do not put secrets in either file; both are visible to project members. Pick stable metric names so diffs are meaningful.

## Verify
MR shows the metrics widget with deltas; the job page shows the annotation links.

## Checked

2026-11-02. Confirmed: metrics file format and default `metrics.txt`, string comparison, widget order added/removed/changed/unchanged, behaviour when baseline has no metrics, widget appears only when the pipeline is complete, Premium/Ultimate tier (GitLab metrics reports docs); `external_link` annotation with `label` and `url`, shown on the job output page (GitLab artifacts reports docs). Removed: comment-line handling and unique-section-name claims.

Method: documentation only; no commands were run.
