---
id: computing-software.devops-ci-cd.argocd-image-updater.registry-defaults-and-rate-limit
name: registry-defaults-and-rate-limit
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, default-registry, defaultns, rate-limit, registries-conf, docker-hub, registry-config]
level: practitioner
status: docs-checked
description: "Set the default registry, default namespace and per-registry rate limit in registries.conf, with the one-default rule and mismatch risk."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/registries.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Default registry, default namespace, rate limit

Default registry. Most container engines treat `argoproj/argocd` and `docker.io/argoproj/argocd` as the same image. If your cluster defaults to another registry, mark it:

```yaml
registries:
- name: RedHat Quay
  api_url: https://quay.io
  prefix: quay.io
  default: true
```

Now `argoproj/argocd` means `quay.io/argoproj/argocd`. Rules and risks:

- only one registry may have `default: true`; with more than one, the configuration is not loaded
- the setting must match your cluster's default registry, or workloads break
- without any configuration `docker.io` is the default

Default namespace. Set `defaultns` when the registry has an implicit namespace. Canonical case: Docker Hub with `defaultns: library`, so `docker pull nginx` resolves to `docker.io/library/nginx`.

Rate limit. `limit` is an integer of requests per second for that registry; the default is `20`. For example `limit: 10` caps `quay.io` at 10 requests per second. The limit counts every HTTP request, and inspecting one tag can take several requests. Raise it only if the registry imposes no limits and with care. The `test` command has `--rate-limit` to override it (default 20).

## Checked
2026-11-08. Confirmed against the Argo CD Image Updater registries page and test command page: the `default: true` example and its meaning, one default only (otherwise the configuration is not loaded), the cluster-mismatch warning, `docker.io` as the implicit default, `defaultns: library`, `limit` in requests per second with default 20 counting all HTTP requests, and `test --rate-limit` (default 20). Nothing removed.
Method: documentation only; no commands were run.
