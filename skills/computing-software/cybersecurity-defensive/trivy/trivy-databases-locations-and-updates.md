---
id: computing-software.cybersecurity-defensive.trivy.trivy-databases-locations-and-updates
name: trivy-databases-locations-and-updates
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-db, trivy-java-db, trivy-checks, db-repository, skip-db-update, download-db-only, trivy-clean]
level: practitioner
status: docs-checked
description: "Manage Trivy's vulnerability, Java and checks databases: registries, alternative repositories with fallback, skip-update flags, download-only and removal."
sources:
  - https://trivy.dev/latest/docs/guide/configuration/db/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The databases are fetched and maintained automatically, so normally you do not notice them. The page also notes that its connectivity list is not exhaustive, since some features need extra external resources.
Trivy needs three OCI-packaged databases, fetched automatically as required: the vulnerability DB (`trivy-db`, used only for vulnerability scanning), the Java DB (`trivy-java-db`, identifies JAR artifacts) and the checks bundle (`trivy-checks`, misconfiguration logic). They are published to GHCR (`ghcr.io/aquasecurity/...`), Docker Hub (`aquasec/...`) and AWS ECR (`public.ecr.aws/aquasecurity/...`). By default Trivy tries `mirror.gcr.io/aquasec` first, then `ghcr.io/aquasecurity`.

Alternative locations: `--db-repository`, `--java-db-repository`, `--checks-bundle-repository`. The flag can repeat; on transient errors (429, 5xx) Trivy falls back in order. The checks bundle does not support fallback lists because the embedded checks are the fallback. Setting these flags overrides the defaults, so include the official locations if you want them kept. Without a tag, the db images use the schema number, not `latest`.

```
trivy image --db-repository my.registry.local/trivy-db --db-repository registry.gitlab.com/gitlab-org/security-products/dependencies/trivy-db alpine
```

Skip updates: `--skip-db-update`, `--skip-java-db-update`, `--skip-check-update`. Update only: `--download-db-only`, `--download-java-db-only` (there is no checks-only download).

Remove: `trivy clean` with `--all`, `--checks-bundle`, `--java-db`, `--scan-cache` or `--vuln-db`.

## Checked

2026-11-03. Read and confirmed against the Trivy Databases page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
