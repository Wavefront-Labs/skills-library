---
id: computing-software.cybersecurity-defensive.trivy.private-registry-login-and-credentials
name: private-registry-login-and-credentials
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-registry-login, trivy-username, trivy-password, password-stdin, docker-config, private-registry]
level: practitioner
status: docs-checked
description: "Authenticate Trivy to a private registry with trivy registry login, environment variables or multiple credential pairs, avoiding credential leakage across registries."
sources:
  - https://trivy.dev/latest/docs/guide/advanced/private-registries/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy can pull from a private registry without Docker or other tools installed, which suits CI.

Login: `trivy registry login` stores credentials in the Docker configuration file (`~/.docker/config.json`), whose path can be changed with `DOCKER_CONFIG`.
```shell
cat ~/my_password.txt | trivy registry login --username foo --password-stdin ghcr.io
trivy image ghcr.io/your/private_image
```

Passing credentials at scan time:
```shell
TRIVY_USERNAME=YOUR_USERNAME TRIVY_PASSWORD=YOUR_PASSWORD trivy image YOUR_PRIVATE_IMAGE
```
Warning from the page: credentials given through environment variables or CLI flags are tried against every registry met during the scan, which can expose them unintentionally. Set them only when necessary and prefer `trivy registry login`, which binds credentials to a specific registry. The `--password` flag exists but its use is not recommended. Credentials can also live in `trivy.yaml`.

Several credential sets: use comma-separated lists, and Trivy tries each pair in turn.
```shell
export TRIVY_USERNAME=USERNAME1,USERNAME2
export TRIVY_PASSWORD=PASSWORD1,PASSWORD2
```
The number of usernames and passwords must match, and `--password-stdin` does not support comma-separated passwords.

## Checked

2026-11-03. Read and confirmed against the Private Registries overview page (and ACR, ECR, GAR subpages) on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
