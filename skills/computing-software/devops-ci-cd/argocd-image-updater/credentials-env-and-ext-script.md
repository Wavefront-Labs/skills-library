---
id: computing-software.devops-ci-cd.argocd-image-updater.credentials-env-and-ext-script
name: credentials-env-and-ext-script
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, env-credentials, ext-script, external-script, credentials, ecr, short-lived-token]
level: practitioner
status: docs-checked
description: "Feed registry credentials from an environment variable (env:NAME) or an executable script (ext:/absolute/path) and learn the script contract, caching and cost trade-offs."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/authentication.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Credentials from env vars and scripts

Environment variable: reference with `env:<name_of_environment_variable>`. The value must be `<username>:<password>`:

```
DOCKER_HUB_CREDS=someuser:s0m3p4ssw0rd
env:DOCKER_HUB_CREDS
```

Handy for tests with `argocd-image-updater test --credentials env:...`, or when the variable is mounted into the pod from a Secret.

Script: reference with `ext:<full_path_to_script>`, for example `ext:/usr/local/bin/creds.sh`. Contract:

- the updater passes no arguments
- the script prints exactly one line to stdout, `<username>:<password>`, with a newline
- the path must be absolute and the file executable (`+x`)
- on Kubernetes the script must exist in the container file system: mount it from a ConfigMap (with an executable mode) or copy it with an init container

```bash
#!/bin/sh
echo "someuser:s0mep4ssw0rd"
```

Scripts suit registries that need short-lived tokens issued by a third party, such as ECR on AWS.

Cost and caching: at image level (`pullSecret: ext:...`) the script runs on every check and the result is not cached. To execute once and cache, configure it at registry level and add `credsexpire`.

## Checked

2026-11-04. Confirmed against authentication.md (env: and ext: notation, script contract of no arguments and one newline-terminated line, ECR example, init container or ConfigMap mount, cost warning), images.md (ext: script run every time, not cached) and registries.md (credsexpire, Credentials caching).

Method: documentation only; no commands were run.
