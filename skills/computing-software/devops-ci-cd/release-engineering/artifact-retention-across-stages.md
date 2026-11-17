---
id: computing-software.devops-ci-cd.release-engineering.artifact-retention-across-stages
name: artifact-retention-across-stages
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, artifact-retention-policy, retention-policy, artifact-cleanup, ecr-lifecycle-policy, artifactory-cleanup, release-retention]
level: practitioner
status: docs-checked
description: "Define retention for build artifacts per stage: keep releases and deployed versions, expire snapshots and PR builds, registry lifecycle rules, and legal or audit holds."
sources:
  - https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html
  - https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/removing-workflow-artifacts
  - https://jfrog.com/help/r/jfrog-platform-administration-documentation/cleanup-policies
  - https://help.sonatype.com/en/cleanup-policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Artifact retention across stages

Without retention, registries and artifact stores grow forever (cost, slow cleanup, slower scans). With careless retention, you delete the image production is running, or the release an auditor asks for.

## Policy by stage
| Stage | Example rule |
|---|---|
| PR / branch builds | delete after 7-14 days or when the branch is deleted |
| main snapshots | keep last 30 builds or 30 days |
| staging candidates | keep last 20 or 90 days, plus anything currently deployed |
| releases (GA) | keep for support window + audit requirement; immutable |
| CI logs and test artifacts | 30-90 days unless attached to a release |
Never delete anything currently deployed in any environment: generate a "protected digests" list from clusters/deploy records before cleanup.

## Registry lifecycle rules
**ECR**
```json
{"rules":[
 {"rulePriority":1,"description":"keep releases","selection":{"tagStatus":"tagged","tagPatternList":["v*"],"countType":"imageCountMoreThan","countNumber":9999},"action":{"type":"expire"}},
 {"rulePriority":2,"description":"pr builds","selection":{"tagStatus":"tagged","tagPrefixList":["pr-"],"countType":"sinceImagePushed","countUnit":"days","countNumber":14},"action":{"type":"expire"}},
 {"rulePriority":3,"description":"untagged","selection":{"tagStatus":"untagged","countType":"sinceImagePushed","countUnit":"days","countNumber":3},"action":{"type":"expire"}}]}
```
Rules are evaluated by priority; an image matched by a higher-priority rule is not considered by lower ones, so the "keep releases" rule with a huge count protects `v*` tags. Preview with `aws ecr start-lifecycle-policy-preview`.
- GHCR: `actions/delete-package-versions` with `min-versions-to-keep` and `ignore-versions: '^v\d+'`.
- Artifactory: Cleanup Policies (see JFrog's cleanup policies page); make sure release repositories are excluded.
- Nexus: cleanup policies per repository (see Sonatype's cleanup policies page).
- GitHub Actions artifacts and logs: 90 days by default, configurable at repository, organization and enterprise level.

## Mechanics that bite
- Deleting a tag may not free storage until the registry runs its own cleanup; check your registry's docs.
- Multi-arch indexes reference child manifests; in ECR an image referenced by a manifest list cannot be expired by a lifecycle rule. Use tools that understand OCI indexes.
- Signatures and attestations are separate artifacts and must be retained with their image.
- Legal hold: some industries require keeping exactly what shipped; use immutable repos or object lock for release artifacts.

## Verify
- [ ] Dry-run/preview of each rule shows no deployed or released digests selected.
- [ ] Storage growth flattens after rules apply; restoring a 2-year-old release still works.

## Checked

2026-10-28. Confirmed against the ECR lifecycle policy docs: `tagPatternList` or `tagPrefixList` (not both), `imageCountMoreThan`, `sinceImagePushed` with `countUnit`, `tagStatus` untagged, `rulePriority` (a lower number takes precedence; an image matched by a higher-priority rule cannot be expired by a lower one), the lifecycle policy preview, and manifest-list references; GitHub docs for the 90-day default artifact and log retention; `actions/delete-package-versions` inputs `min-versions-to-keep` and `ignore-versions`. `aws ecr start-lifecycle-policy-preview` passed the command check. Removed: the 1-7 year figure, JFrog CLI and AQL, Nexus compact task detail, `retention-days`, garbage-collection tool names and the `.sig` tag naming.

Method: documentation only; no commands were run.
