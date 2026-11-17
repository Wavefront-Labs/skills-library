---
id: computing-software.devops-ci-cd.gitlab-ci.cyclonedx-reports-and-dependency-list
name: cyclonedx-reports-and-dependency-list
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, cyclonedx-report, dependency-list, sbom-artifact-report, gl-sbom]
level: advanced
status: docs-checked
description: "Publish CycloneDX SBOMs as artifacts:reports:cyclonedx so GitLab builds the project and group dependency list, with licenses and vulnerabilities, from your own generators."
sources: ["https://docs.gitlab.com/ci/yaml/artifacts_reports/#artifactsreportscyclonedx", "https://docs.gitlab.com/user/application_security/dependency_list/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CycloneDX reports and the dependency list (Ultimate)

## 1. Report keyword
```yaml
sbom:
  script:
    - ./generate-sbom.sh gl-sbom-all.cdx.json   # your CycloneDX generator
  artifacts:
    reports:
      cyclonedx: [gl-sbom-*.cdx.json]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```
The docs use names such as `gl-sbom-npm-npm.cdx.json` and the pattern `gl-sbom-*.json`; the report can be a list of file names, a pattern, or both.

## 2. Dependency list
Secure → **Dependency list** shows components (name, version, packager, location, license,
vulnerabilities) from the **latest default-branch pipeline** with CycloneDX reports. Group-level
list aggregates projects — use it to answer "who uses log4j 2.14?".

## 3. Making it accurate
- An SBOM from lockfiles differs from an SBOM of the built image; generate both if you need OS packages.
- The CycloneDX spec version must be 1.4, 1.5 or 1.6; validate with `cyclonedx-cli validate`.
- Follow the GitLab CycloneDX property taxonomy so GitLab can show details and enable security features (see the dependency list page).

## 4. Gotchas
- The dependency list uses CycloneDX reports from the latest default branch pipeline.
- `artifacts:expire_in` overrides the instance default expiry for the artifacts.

## Verify
- [ ] Dependency list populated after a default-branch pipeline; a known package shows the right version.

## Checked

2026-10-28. Confirmed on the CycloneDX artifacts:reports page and the dependency list page: artifacts:reports:cyclonedx with a file list or pattern such as gl-sbom-*.json, example names gl-sbom-npm-npm.cdx.json, Ultimate tier, dependency list built from the latest default branch pipeline, spec versions 1.4/1.5/1.6, cyclonedx-cli validate, GitLab CycloneDX property taxonomy, artifacts:expire_in. Removed: the syft image and command, the export API endpoint, the metadata.component and input_file property claims, report size limits, MR-pipeline claim.
Method: documentation only; no commands were run.
