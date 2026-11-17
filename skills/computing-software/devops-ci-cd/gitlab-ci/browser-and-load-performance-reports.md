---
id: computing-software.devops-ci-cd.gitlab-ci.browser-and-load-performance-reports
name: browser-and-load-performance-reports
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, browser-performance-report, load-performance-report, sitespeed-io, k6-load-test, performance-widget]
level: advanced
status: docs-checked
description: "Add browser (sitespeed.io) and load (k6) performance testing to merge requests with the browser_performance and load_performance artifact reports and degradation thresholds."
sources: ["https://docs.gitlab.com/ci/testing/browser_performance_testing/", "https://docs.gitlab.com/ci/testing/load_performance_testing/", "https://docs.gitlab.com/ci/yaml/artifacts_reports/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# browser_performance and load_performance reports (Premium)

The MR widget compares the MR's metrics with the target branch's latest result and flags degradations.

## 1. Browser performance (sitespeed.io)
```yaml
include:
  - template: Verify/Browser-Performance.gitlab-ci.yml
browser_performance:
  variables:
    URL: $REVIEW_APP_URL
    SITESPEED_OPTIONS: "-n 3"
    DEGRADATION_THRESHOLD: 5          # ignore score drops smaller than 5 points
  needs: [deploy-review]
```
Produces `browser-performance.json` as `artifacts:reports:browser_performance`. Runs Docker-in-Docker (needs a dind-capable runner).
Custom tool: any job can emit the report format:
```yaml
  artifacts:
    reports:
      browser_performance: browser-performance.json
```

## 2. Load performance (k6)
```yaml
include:
  - template: Verify/Load-Performance-Testing.gitlab-ci.yml
load_performance:
  variables:
    K6_TEST_FILE: tests/load/checkout.js
    K6_OPTIONS: "--duration 30s"
```
The template writes `load-performance.json`, uploaded as `artifacts:reports:load_performance`; the MR widget compares it with the target branch.

## 3. Gotchas
- Load test against review apps, not shared staging (noisy neighbours skew results) — and never prod.
- Results vary between runs; use multiple iterations (`-n`) and thresholds that tolerate noise.

## Verify
- [ ] MR widget shows the performance comparison; a deliberate slowdown is flagged.

## Checked

2026-11-02. Confirmed: template names Verify/Browser-Performance and Verify/Load-Performance-Testing, `SITESPEED_OPTIONS`, `DEGRADATION_THRESHOLD`, `K6_TEST_FILE`, `K6_OPTIONS`, output files browser-performance.json / load-performance.json, Docker-in-Docker use, Premium/Ultimate tier (GitLab browser and load performance testing docs). Removed: --mobile, --vus, k6 threshold snippet, widget metric list, specific noise percentage, unconfirmed comparison claims.

Method: documentation only; no commands were run.
