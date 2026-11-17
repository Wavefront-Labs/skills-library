---
id: computing-software.devops-ci-cd.argocd-image-updater.config-configmap-keys
name: config-configmap-keys
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, configmap, argocd-image-updater-config, config-keys, log-level, git-config, registries-conf]
level: practitioner
status: docs-checked
description: "Reference of the argocd-image-updater-config ConfigMap keys named in the docs: log level, namespaces, git identity, commit signing, registries.conf, webhook and TLS keys."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/registries.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/webhook.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# argocd-image-updater-config keys

The ConfigMap `argocd-image-updater-config` is the file-based counterpart to most CLI flags. Keys that the docs mention:

| Key | Purpose |
|---|---|
| `log.level` | `trace`, `debug`, `info`, `warn`, `error` (default `info`) |
| `argocd.namespace` | namespace where Argo CD runs |
| `watch.namespaces` | namespaces to watch, comma separated |
| `git.user`, `git.email` | commit author (defaults `argocd-image-updater`, `noreply@argoproj.io`) |
| `git.commit-message-template` | Go `text/template` for commit messages |
| `git.commit-signing-key` | GnuPG key ID or private SSH key path |
| `git.commit-signing-method` | `openpgp` (default) or `ssh` |
| `git.commit-sign-off` | `"true"` to sign off commits |
| `registries.conf` | multi-line YAML registry list |
| `webhook.enable`, `webhook.port` | run-command webhook server |
| `webhook.ratelimit-allowed` | webhook rate limit; 0 disables it (the webhook page says requests per hour in prose but its sample comment says per second) |
| `disable-tls`, `tls.cert-path`, `tls.key-path`, `tls.min-version`, `tls.max-version`, `tls.ciphers`, `tls.curve-preferences` | webhook TLS |

Webhook secrets are not in this ConfigMap; they live in the `argocd-image-updater-secret` Secret.

Registry changes (`registries.conf`) need a pod restart to take effect. Equivalent environment variables exist for many flags, for example `ARGOCD_NAMESPACE`, `GIT_COMMIT_USER` and `GIT_COMMIT_EMAIL`.

## Checked

2026-11-04. Confirmed key by key against installation.md (log.level, argocd.namespace, watch.namespaces, default info), update-methods.md (git.user, git.email, git.commit-message-template, git.commit-signing-key, git.commit-signing-method default openpgp, git.commit-sign-off), registries.md (registries.conf, restart needed), webhook.md (webhook.enable, webhook.port, webhook.ratelimit-allowed, disable-tls and the tls.* keys, argocd-image-updater-secret) and the run command page (flag defaults and environment variables). Added the page's own inconsistency about the rate-limit unit.

Method: documentation only; no commands were run.
