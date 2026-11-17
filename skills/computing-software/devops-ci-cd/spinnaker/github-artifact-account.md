---
id: computing-software.devops-ci-cd.spinnaker.github-artifact-account
name: github-artifact-account
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [artifacts, github, access-token, accounts]
level: practitioner
status: docs-checked
description: "Let Spinnaker download files from GitHub: create a repo-scope token and add a github account to clouddriver-local.yml."
sources:
  - https://spinnaker.io/docs/setup/other_config/artifacts/
  - https://spinnaker.io/docs/setup/other_config/artifacts/github/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Artifacts are remote, deployable resources, and each type needs credentials to be downloaded or uploaded. The artifacts landing page has account guides for Git Repo, GitHub, GitLab, Bitbucket, Helm, HTTP, Maven, S3, GCS and Oracle Object Storage.

**GitHub account setup:**
1. You need a GitHub account. Generate an access token; it requires the **repo** scope.
2. Add the token either to a secrets manager (used by reference) or to a volume mounted into the clouddriver pods by modifying the clouddriver `deployment.yaml`.
3. Add this to `clouddriver-local.yml`:

```yaml
artifacts:
  enabled: true
  github:
    enabled: true
    accounts:
    - name: my-github-account
      tokenFile: /mnt/some/file|secretReference
```

The page says more options are available in the GitHub account definition code.

This account only covers downloading files from GitHub.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Configure Artifacts landing page and the Configure a GitHub artifact account page. Confirmed the repo scope and the clouddriver-local.yml block; the artifact types list is updated to match the landing page. Replaced the old Halyard commands (not on the current pages) and removed the Artifact Account stage field and webhook remarks, which those pages do not state.
