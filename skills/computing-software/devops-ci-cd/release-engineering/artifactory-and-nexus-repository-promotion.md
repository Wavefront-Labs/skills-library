---
id: computing-software.devops-ci-cd.release-engineering.artifactory-and-nexus-repository-promotion
name: artifactory-and-nexus-repository-promotion
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, repository-promotion, artifact-promotion, artifactory]
level: practitioner
status: draft
description: "Promote build artifacts through dev/staging/release repositories in Artifactory or Nexus: build info, promotion APIs, staging moves, immutability and permissions."
sources: ["https://jfrog.com/help/r/jfrog-rest-apis/promote-docker-image", "https://help.sonatype.com/en/staging.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Artifactory and Nexus repository promotion

Pattern: builds publish to a `*-dev` (or staging) repository; promotion **moves or copies** the
exact artifact to `*-release`. Consumers in production resolve only from release repos.

## JFrog Artifactory
Publish with build info (links artifacts, dependencies, env, VCS):
```bash
jf rt upload "dist/*.tgz" libs-dev-local/app/1.4.2/ --build-name=app --build-number=$BUILD_ID
jf rt build-publish app $BUILD_ID
# promote the whole build
jf rt build-promote app $BUILD_ID libs-release-local --status=released --copy=true --props="qa=passed"
# docker image promotion
curl -u "$U:$T" -X POST "$ART/api/docker/docker-dev-local/v2/promote" -H 'Content-Type: application/json' \
  -d '{"targetRepo":"docker-release-local","dockerRepository":"api","tag":"1.4.2","copy":true}'
```
Release Bundles (v2) package and promote sets of artifacts through environments with signatures.

## Sonatype Nexus Repository Pro
Staging: tag components on upload, then
```bash
curl -u "$U:$T" -X POST "$NEXUS/service/rest/v1/staging/move/maven-releases?tag=app-1.4.2"
```
Nexus OSS lacks staging; copy via the components API or keep separate pipelines writing to release repos only after gates.

## Controls
- Release repos immutable: disallow redeploy/overwrite.
- Only the promotion service account can write to release repos; humans read only.
- Promotion records properties (`qa=passed`, `change=CHG-123`) for audit.
- Cleanup policies on dev repos only.

## Verify
- [ ] Production pulls fail for artifacts that were never promoted; release artifact checksum equals the dev one.
