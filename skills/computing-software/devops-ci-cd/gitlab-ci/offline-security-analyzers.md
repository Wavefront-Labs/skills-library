---
id: computing-software.devops-ci-cd.gitlab-ci.offline-security-analyzers
name: offline-security-analyzers
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, analyzer-offline, secure-analyzers-prefix, air-gapped-scanning, analyzer-image-mirror]
level: advanced
status: docs-checked
description: "Run GitLab security scanners in offline or air-gapped environments: mirroring analyzer images, SECURE_ANALYZERS_PREFIX, advisory database updates and per-scanner variables."
sources: ["https://docs.gitlab.com/user/application_security/offline_deployments/", "https://docs.gitlab.com/user/application_security/sast/#running-sast-in-an-offline-environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline analyzers and SECURE_ANALYZERS_PREFIX

## 1. Mirror the images
Copy the analyzer images the templates use into your internal registry; the offline deployment docs list the images and versions for each scanner.
Re-run the copy on a schedule so rule and database updates arrive.

## 2. Point the templates at the mirror
```yaml
variables:
  SECURE_ANALYZERS_PREFIX: "registry.internal.example.com/security-products"
include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Dependency-Scanning.gitlab-ci.yml
  - template: Jobs/Container-Scanning.gitlab-ci.yml
```
Container scanning has its own `CS_ANALYZER_IMAGE` if it lives elsewhere.

## 3. Per-scanner offline settings
- Dependency, container and DAST scanning have their own offline settings: follow the offline deployment page for each scanner.
- Set `SECURE_LOG_LEVEL: debug` to see what tries to reach the internet.

## 4. Gotchas
- Using `latest` mirror tags while templates pin a major version → analyzer/template mismatch errors.
- Stale mirrors mean missing new CVEs; alert if the mirror job fails.

## Verify
- [ ] Jobs log `Pulling docker image registry.internal.example.com/security-products/...`.
- [ ] Network egress logs show no calls to gitlab.com from scanner jobs.

## Checked

2026-11-02. Confirmed: `SECURE_ANALYZERS_PREFIX` overrides the registry that provides the default analyzer images; `CS_ANALYZER_IMAGE` exists for container scanning; `SECURE_LOG_LEVEL: debug` (GitLab SAST and offline deployment docs). Removed: image list and versions, skopeo loop, GEMNASIUM_DB_UPDATE_DISABLED, 7-day threshold, per-scanner offline claims (not found in fetched pages).

Method: documentation only; no commands were run.
