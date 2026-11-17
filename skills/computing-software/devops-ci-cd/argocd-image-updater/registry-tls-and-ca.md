---
id: computing-software.devops-ci-cd.argocd-image-updater.registry-tls-and-ca
name: registry-tls-and-ca
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, registry-tls, ca-file, ca-data, insecure, argocd-tls-certs-cm, self-signed]
level: advanced
status: docs-checked
description: "Trust a private registry CA with ca_file, ca_data or the automatic argocd-tls-certs-cm lookup, and know why insecure is a last resort."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/registries.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registry TLS and custom CAs

Registry entries in `registries.conf` support these TLS properties:

- `insecure: true` turns off certificate verification. Default `false`. The docs say it should not be used in production.
- `ca_file`: path to a PEM CA bundle trusted in addition to the system store, for example `/app/config/certs/registry-ca.pem`.
- `ca_data`: the PEM data embedded in the configuration, used instead of mounting a file.

Automatic discovery: when `ca_file` is omitted, the updater also looks for `/app/config/tls/<registry-hostname>`. The shipped manifests mount Argo CD's `argocd-tls-certs-cm` ConfigMap at `/app/config/tls` (the mount is optional), so adding the certificate to that ConfigMap under the registry hostname is usually all that is needed.

Rules:

- CA file discovery and `ca_data` processing are skipped when `insecure` is `true`
- certificates are read when registry endpoints are built at startup, so restart the pod after changing them

```yaml
registries:
- name: RedHat Quay
  api_url: https://quay.io
  prefix: quay.io
  ca_file: /app/config/certs/quay-ca.pem
  credentials: env:REGISTRY_SECRET
```

Self-check: run `argocd-image-updater test <registry>/<repo>/<image>` and confirm tags are found without TLS errors.

## Checked

2026-11-08. Read in full: docs/configuration/registries.md. Confirmed insecure, ca_file, ca_data, the /app/config/tls/<registry-hostname> discovery, the optional mount, the skip-when-insecure rule and the restart note. Nothing removed.

Method: documentation only; no commands were run.
