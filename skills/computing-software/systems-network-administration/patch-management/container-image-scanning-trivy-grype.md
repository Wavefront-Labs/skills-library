---
id: computing-software.systems-network-administration.patch-management.container-image-scanning-trivy-grype
name: container-image-scanning-trivy-grype
category: computing-software
field: systems-network-administration
product: patch-management
tags: [trivy, grype, container-image-scanning, image-patching, vulnerability-scanning, ci-pipeline, containers]
level: practitioner
status: docs-checked
description: "Scan container images for vulnerable packages with Trivy and Grype: CI gating on fixable high and critical findings, ignore files, offline databases and registry scanning."
sources:
  - https://trivy.dev/latest/docs/
  - https://trivy.dev/latest/docs/references/configuration/cli/trivy_image/
  - https://trivy.dev/latest/docs/configuration/filtering/
  - https://github.com/anchore/grype
  - https://goharbor.io/docs/main/administration/vulnerability-scanning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scanning images with Trivy or Grype

**Goal:** know which images carry vulnerable OS packages and libraries, and stop new ones reaching production.

## Trivy
```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 registry.example/app:1.4.2
trivy image --format json -o app.json registry.example/app:1.4.2
trivy fs --scanners vuln,secret,misconfig .
trivy k8s --report summary                  # running workloads in the current kube context
```
`--ignore-unfixed` hides findings with no available fix, so the gate fails only on actionable issues. Suppress accepted findings with `.trivyignore`, or with `.trivyignore.yaml`, whose entries can carry a `statement` and an `expired_at` date (yyyy-mm-dd) so exceptions expire.

## Grype
```bash
grype registry.example/app:1.4.2 --only-fixed --fail-on high
grype sbom:app.cdx.json
```
`--only-fixed` lists only vulnerabilities with a fix, and `--fail-on <severity>` sets the failure threshold. Exceptions go in `.grype.yaml` `ignore:` rules; a match must meet all criteria in a rule (for example vulnerability ID, package, or fix-state).

## In CI
- Scan after build, before push to the production registry; fail on fixable High/Critical.
- Also scan nightly: new CVEs appear for unchanged images. Rebuild on the newest base image when findings appear.

## Registry and runtime
Harbor scans with Trivy when Trivy was enabled at install (`--with-trivy`); the project setting "Prevent vulnerable images from running" blocks pulls of images at or above a chosen severity. Check your cloud registry's own scanning documentation for continuous scanning.

## Air-gapped
Run `trivy image --download-db-only` on a connected host, transfer the database as described in the Trivy air-gap guide, and scan with `--skip-db-update` on hosts that cannot update.

## Gotchas
- Distroless and scratch images have few OS packages but language dependencies still matter: Trivy's `--pkg-types` defaults to `os,library`, so leave `library` enabled.
- Scanner results differ; standardise on one for gating, use the other for cross-checks.

## Verify
A deliberately old base image fails the CI gate; the nightly report lists running images with fixable criticals and their owners.

## Checked
Date: 2026-10-27. Documentation checked: Trivy CLI reference for `trivy image`, `trivy filesystem` and `trivy kubernetes` (`--ignore-unfixed`, `--exit-code`, `--severity`, `--scanners`, `--pkg-types`, `--download-db-only`, `--skip-db-update`, `--report summary`), Trivy filtering page (`.trivyignore`, `.trivyignore.yaml`, `expired_at`), Grype option definitions in the upstream source (`--only-fixed`, `--fail-on`, `ignore` rules, `sbom:` input), Harbor vulnerability scanning and project configuration pages. Fixed `trivy k8s ... cluster` (the documented form takes no `cluster` argument) and removed the ORAS and cloud-registry claims, which were not confirmed.

Method: documentation only; no commands were run.
