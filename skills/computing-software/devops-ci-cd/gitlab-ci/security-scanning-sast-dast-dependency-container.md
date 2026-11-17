---
id: computing-software.devops-ci-cd.gitlab-ci.security-scanning-sast-dast-dependency-container
name: security-scanning-sast-dast-dependency-container
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, security-scanning, sast, dast, dependency-scanning, container-scanning, secret-detection, iac-scanning, api-security, fuzz-testing, security-templates, jobs-sast-gitlab-ci-yml, semgrep, gemnasium, trivy-gitlab, vulnerability-report, security-dashboard, mr-security-widget, scan-result-policies, merge-request-approval-policy, security-policies-project, vulnerability-dismissal, analyzer-variables, sast-excluded-paths, cs-image, dast-website, security-report-schema]
level: practitioner
status: gated
description: "Enable GitLab SAST, secret, dependency, container and DAST scanning with templates; tune noise, read the MR widget, and enforce with security policies."
sources: ["https://docs.gitlab.com/ee/user/application_security/", "https://docs.gitlab.com/ee/user/application_security/sast/", "https://docs.gitlab.com/ee/user/application_security/container_scanning/", "https://docs.gitlab.com/ee/user/application_security/dast/", "https://docs.gitlab.com/ee/user/application_security/policies/scan-result-policies.html", "https://docs.gitlab.com/ee/user/application_security/secret_detection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security scanning: SAST, DAST, dependency and container scanning

**Goal:** every MR shows new vulnerabilities it introduces, critical findings block merge by
policy, and the noise is tuned so developers keep reading the widget.

## 1. Enable with templates
```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml                  # Semgrep-based (plus language analyzers)
  - template: Jobs/Secret-Detection.gitlab-ci.yml
  - template: Jobs/Dependency-Scanning.gitlab-ci.yml   # Gemnasium; lockfile-based
  - template: Jobs/Container-Scanning.gitlab-ci.yml    # Trivy-based (the Grype analyzer is no longer maintained)
  - template: Jobs/SAST-IaC.gitlab-ci.yml              # KICS for Terraform/K8s/Dockerfile
  - template: DAST.gitlab-ci.yml                        # needs a running target
stages: [build, test, dast]   # templates use `test` (and `dast`); define the stages they expect
variables:
  SAST_EXCLUDED_PATHS: "spec, test, tests, tmp"      # the documented default; add paths as needed
  SECRET_DETECTION_HISTORIC_SCAN: "false"             # "true" once to scan full history, then off
  CS_IMAGE: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"        # container scanning target; default is $CI_APPLICATION_REPOSITORY:$CI_APPLICATION_TAG
  # severity threshold variable name and values: confirm in the container scanning docs (gated: unconfirmed, source is paywalled or blocked)
  DS_EXCLUDED_PATHS: "spec, test"
```
The `Jobs/*.gitlab-ci.yml` templates are the current versions; template rules, `allow_failure` behaviour and the policy-based blocking model below were not on the fetched pages (gated: unconfirmed, source is paywalled or blocked). Output: `artifacts: reports: sast: gl-sast-report.json`
etc. (security report schema), which feeds the MR widget and the vulnerability report.

SAST is available in all tiers (Free, Premium, Ultimate). Which scanners and which MR widget or vulnerability report features each tier gets: check each scanner's page for its Tier line (gated: unconfirmed, source is paywalled or blocked). The report is JSON, so on lower tiers you can parse it yourself.

## 2. Per-scanner notes
- **SAST**: Semgrep-based analyzer (and GitLab Advanced SAST in Ultimate); customise rules with a ruleset file `.gitlab/sast-ruleset.toml` (disable rules by rule ID, passthroughs). `SAST_ANALYZER_IMAGE_TAG` pins the analyzer version and must come after the template include.
  Monorepos: exclude paths with `SAST_EXCLUDED_PATHS` (comma-separated).
- **Secret Detection**: scans new commits; a one-time historic scan (`SECRET_DETECTION_HISTORIC_SCAN`) finds old leaks. Scan range, push protection and custom pattern syntax: see the secret detection docs (gated: unconfirmed, source is paywalled or blocked).
- **Dependency Scanning**: lockfile-based, with analyzers per language; the newer SBOM-based scanning reads CycloneDX files. Supported lockfiles, analyzer variables and Java build settings: see the dependency scanning docs (gated: unconfirmed, source is paywalled or blocked).
- **Container Scanning**: Trivy-based. Scans `CS_IMAGE` (default `$CI_APPLICATION_REPOSITORY:$CI_APPLICATION_TAG`, where the repository defaults to `$CI_REGISTRY_IMAGE/$CI_COMMIT_REF_SLUG`), so the image must be pushed first (use `needs:` on the build job). Use `CS_REGISTRY_USER`/`CS_REGISTRY_PASSWORD` for third-party registries. `CS_ANALYZER_IMAGE` sets the analyzer image; do not use its `:latest` tag. SBOM output and cluster image scanning: see the docs (gated: unconfirmed, source is paywalled or blocked).
- **DAST**: needs a running target (a review app). Variable names for target URL, full/active scan, authentication and API scanning, and which analyzer is current: see the DAST docs (gated: unconfirmed, source is paywalled or blocked). Run active scans only against non-production.
- **Coverage-guided fuzzing** and **API security testing** have their own templates; niche.

## 3. The MR widget and the vulnerability report
The widget compares the MR's reports against the target branch's latest reports, so run the scanners on the default branch first. Vulnerability statuses, dismissal reasons and audit behaviour: see the vulnerability report docs (gated: unconfirmed, source is paywalled or blocked).

## 4. Enforce with policies (Ultimate)
Security policies need a higher tier; confirm tier and menu path in the policy docs (gated: unconfirmed, source is paywalled or blocked). Two policy types:
- **Scan execution policy**: forces scanners to run on target projects/groups on a schedule
  or every pipeline (no `include:` needed; cannot be removed by editing `.gitlab-ci.yml`).
- **Merge request approval policy** (scan result policy): e.g. "require 1 approval from
  `@security` if the MR introduces ≥ 1 Critical/High vulnerability that is newly detected
  and not dismissed; also when there are no reports (prevents bypass by deleting the job)".
  Option names (vulnerability states, severity levels, age, fail-open/closed, bypass settings): see the policy schema docs (gated: unconfirmed, source is paywalled or blocked).
Start **warn-only** with an approver group who reads the findings for two weeks, then flip
to blocking. Policy YAML is version-controlled in the policy project and applied via MR.

## 5. Tuning noise
- `SAST_EXCLUDED_PATHS` / `DS_EXCLUDED_PATHS` for vendored and test code.
- Pin analyzer versions (`SAST_ANALYZER_IMAGE_TAG`, `CS_ANALYZER_IMAGE`) only when a release breaks you; otherwise float to get rule updates.
- Offline/air-gapped: mirror analyzer images and set `SECURE_ANALYZERS_PREFIX` to your registry; other scanners need their own offline settings (see their docs).
- Report size limits: check the docs (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Default branch pipeline has all scanner jobs green with report artifacts.
- [ ] A test MR adding an obviously insecure pattern shows a *new* finding in the widget.
- [ ] Container scanning targets the exact image digest built in this pipeline.
- [ ] Approval policy blocks a Critical finding and requires the security approver.
- [ ] Deleting the SAST job from `.gitlab-ci.yml` still runs it (scan execution policy).

## Checked

2026-11-02. Checked against the GitLab SAST and container scanning pages and the DAST/secret detection/security landing pages. Confirmed: SAST all tiers, `.gitlab/sast-ruleset.toml`, `SAST_EXCLUDED_PATHS` (default spec, test, tests, tmp), `SAST_ANALYZER_IMAGE_TAG` placement, `SECURE_ANALYZERS_PREFIX`, container scanning uses Trivy and Grype is no longer maintained, `CS_IMAGE` default, `CS_REGISTRY_USER`/`CS_REGISTRY_PASSWORD` for third-party registries, `CS_ANALYZER_IMAGE` not `:latest`. Fixed: Grype presented as an option, `vendor` in the default exclude list, job-token default for registry credentials. Removed: `SAST_SEMGREP_CUSTOM_RULES`, `CS_SEVERITY_THRESHOLD` threshold values, the 20 MB report limit and specific policy option names. Gated: the dependency scanning, secret detection, DAST, policy and vulnerability-report specifics, whose full pages were not fetched here and were replaced with pointers.

Method: documentation only; no commands were run.
