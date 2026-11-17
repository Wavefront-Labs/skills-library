---
id: computing-software.devops-ci-cd.spinnaker.helm-artifact-account
name: helm-artifact-account
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [artifacts, helm, chartmuseum, basic-auth, accounts]
level: practitioner
status: docs-checked
description: "Configure a Helm artifact account against a chart repository (Nexus, JFrog, Chartmuseum) using basic authentication in clouddriver-local.yml, plus the igor trigger setting."
sources:
  - https://spinnaker.io/docs/setup/other_config/artifacts/helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stages that consume artifacts can read charts directly from a Helm provider. The provider can be an artifact repository such as Nexus, JFrog or Chartmuseum. **Basic auth is the only supported authentication mechanism** for a Helm artifact account, and it is only needed if the files are hidden behind basic auth.

**Credentials file:**
1. Collect the basic-auth `$USERNAME` and `$PASSWORD`.
2. Pick a `$USERNAME_PASSWORD_FILE` location on disk and run `echo ${USERNAME}:${PASSWORD} > $USERNAME_PASSWORD_FILE`.
3. Add the credentials either to a secrets manager (used by reference) or to a volume mounted into the clouddriver pods by modifying the clouddriver `deployment.yaml`.

**Account**, in `clouddriver-local.yml`:

```yaml
artifacts:
  enabled: true
  helm:
    enabled: true
    accounts:
    - name: my-helm-account
      username-password-file: <secret-manager|/mnt/secret/filename>
```

**Triggering a pipeline from Helm changes** needs Igor, which polls Clouddriver for Helm artifact accounts and tracks new Helm resources. Add to `igor-local.yml`:

```yaml
helm:
  enabled: true
```

When Igor finds new Helm resources for the account it triggers any pipeline with a Helm trigger and tracks completion so it does not refire. The page points to more options in the code base.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Configure Helm Artifact account page. Confirmed the repository types, basic-auth-only statement, file format, clouddriver and igor settings. Replaced the old Halyard commands (not on the current page) with the clouddriver-local.yml block, and removed the generic permissions advice and the Bake stage chart packaging claim, which the page does not state.
