---
id: computing-software.cloud-infrastructure-engineering.rancher.bootstrap-password-set-and-retrieve
name: bootstrap-password-set-and-retrieve
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [bootstrap-password, first-login, admin, helm, docker, password-length]
level: intro
status: docs-checked
description: "Set or retrieve the Rancher bootstrap password for the first admin: the bootstrapPassword chart value, how to retrieve it, and password length rules."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/bootstrap-password
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The bootstrap password is for the first admin account. If you do not set one, Rancher generates a random password. It can be any length, but when you reset the admin password after first login the new one must be at least 12 characters.

The minimum password length for user accounts is configurable to any positive integer from 2 to 256, with no decimals or leading zeroes.

To set it, pass `bootstrapPassword` to the chart:

```bash
helm install rancher rancher-<chart-repo>/rancher \
  --set bootstrapPassword=<password>
```

After installation the Rancher UI shows instructions for retrieving it that match your installation method. On Kubernetes, read it from the `bootstrap-secret` secret in `cattle-system` with `kubectl get secret --namespace cattle-system bootstrap-secret -o go-template='{{ .data.bootstrapPassword|base64decode}}{{ "\n" }}'`. For Docker installs the page says the password is stored in the container logs.

The first login prompts for a reset, so the bootstrap value is temporary.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Setting up the Bootstrap Password. Removed the Docker -e CATTLE_BOOTSTRAP_PASSWORD and docker logs grep commands (not on the page; it only says the password is in the container logs).

Method: documentation only; no commands were run.
