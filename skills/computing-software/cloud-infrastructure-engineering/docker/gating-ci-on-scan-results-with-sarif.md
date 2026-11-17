---
id: computing-software.cloud-infrastructure-engineering.docker.gating-ci-on-scan-results-with-sarif
name: gating-ci-on-scan-results-with-sarif
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, vulnerability-scanning, sarif, scan-gating, github-code-scanning, trivy, docker-scout]
level: practitioner
status: docs-checked
description: "Fail builds on the right scan findings (fixable critical/high, new vs baseline) and publish SARIF to GitHub code scanning from Trivy, Grype or Docker Scout."
sources: ["https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/uploading-a-sarif-file-to-github", "https://github.com/aquasecurity/trivy-action", "https://github.com/docker/scout-action", "https://github.com/github/codeql-action/blob/main/upload-sarif/action.yml"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Gating CI on scan results with SARIF

## Gate policy that teams can live with
- Fail on **fixable** CRITICAL (and usually HIGH): `--ignore-unfixed`. Unfixable findings go
  to a report, not the gate.
- Gate PRs on **new** findings compared to the main branch image, so a fresh upstream CVE does
  not block unrelated work.
- Time-boxed exceptions in `.trivyignore`/VEX with an expiry and ticket reference.

## Trivy: gate and SARIF in one job
```yaml
permissions: { contents: read, security-events: write }
steps:
  - uses: docker/build-push-action@v6
    with: { load: true, tags: app:ci }
  - name: Gate
    uses: aquasecurity/trivy-action@v0.36.0   # the README pins a full tag
    with:
      image-ref: app:ci
      severity: CRITICAL,HIGH
      ignore-unfixed: true
      exit-code: "1"
      format: table
  - name: SARIF report (never fails)
    if: always()
    uses: aquasecurity/trivy-action@v0.36.0
    with:
      image-ref: app:ci
      format: sarif
      output: trivy.sarif
      exit-code: "0"
  - uses: github/codeql-action/upload-sarif@v4
    if: always()
    with: { sarif_file: trivy.sarif, category: container-image }
```
For SARIF the action reports every severity unless `limit-severities-for-sarif: true` is set.

## Docker Scout: compare against production
```yaml
- uses: docker/scout-action@v1
  with:
    command: compare
    image: app:ci
    to: registry://reg.example.com/app:main
    only-severities: critical,high
    only-fixed: true
    exit-code: true              # exit code 2 if vulnerability changes are detected
    write-comment: true          # PR comment with the diff
```
`command: cves` with `sarif-file: scout.sarif` produces SARIF for code scanning.

## Grype
```bash
grype app:ci --only-fixed --fail-on high -o sarif > grype.sarif
```

## Gotchas
- SARIF uploads from Actions need `security-events: write`.
- The upload action's `category` input is the string code scanning uses for matching analyses; set a stable one per image.
- GitHub rejects a gzip-compressed SARIF file over 10 MB; reduce results (for example by severity) when a large image exceeds it.
- Gate on the image you will ship (same digest), not a rebuild.

## Checked
Documentation release: aquasecurity/trivy-action v0.36.0 README, docker/scout-action v1.27.0 README, github/codeql-action upload-sarif action.yml (v4 line) and GitHub docs (SARIF support and file-too-large pages), checked 2026-10-26.
Confirmed: trivy-action inputs `image-ref`, `severity`, `ignore-unfixed`, `exit-code`, `format`, `output`, and `limit-severities-for-sarif`; scout-action `command` values (`cves`, `compare`), `to`, `only-severities`, `only-fixed`, `write-comment`, `sarif-file`; `exit-code` returns exit code 2 on changes; 10 MB gzip SARIF limit; `sarif_file` and `category` inputs.
Corrected: trivy-action pin from v0.28.0 to the current v0.36.0; upload-sarif major from v3 to v4; removed the "DB cached after first run", fork-PR upload and "never closes old alerts" claims as unsupported; the Scout `exit-code` comment now matches the README.
Method: documentation only; no commands were run.
