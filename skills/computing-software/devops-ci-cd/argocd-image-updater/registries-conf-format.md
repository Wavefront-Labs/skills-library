---
id: computing-software.devops-ci-cd.argocd-image-updater.registries-conf-format
name: registries-conf-format
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, registries-conf, registry-config, registries-conf-path, api-url, prefix, configmap]
level: practitioner
status: docs-checked
description: "Write registries.conf for Argo CD Image Updater: name, prefix, api_url, credentials, and loading it from a ConfigMap or --registries-conf-path."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/registries.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# registries.conf format

The file is YAML with a top-level `registries` list. Properties per entry:

- `name` (mandatory): informational label
- `prefix` (mandatory): DNS name used as lookup prefix, unique in the file
- `api_url`: HTTP or HTTPS URL of the registry API
- `defaultns`: default namespace (Docker Hub: `library`)
- `default`: `true` to make this the default registry
- `credentials`: credential source (for example `pullsecret:argocd/dockerhub-secret`)
- `credsexpire`: credential lifetime such as `5h`
- `insecure`: skip TLS verification (default `false`)
- `ca_file`, `ca_data`: custom CA, see the registry TLS skill
- `limit`: requests per second (default `20`)

```yaml
registries:
- name: Docker Hub
  prefix: docker.io
  api_url: https://registry-1.docker.io
  credentials: secret:foo/bar#creds
  defaultns: library
  default: true
- name: RedHat Quay
  api_url: https://quay.io
  prefix: quay.io
  credentials: env:REGISTRY_SECRET
```

Loading: from the CLI use `--registries-conf-path <path>` (default `/app/config/registries.conf`; pass an empty string to use built-in defaults). In Kubernetes put the content as a multi-line string under key `registries.conf` in the `argocd-image-updater-config` ConfigMap.

The pod must be restarted for registry changes to apply.

## Checked

2026-11-08. Read in full: docs/configuration/registries.md and docs/install/cmd/run.md. Confirmed each property with its default, the example, the --registries-conf-path default and empty-string behaviour, the registries.conf ConfigMap key and the restart note. Nothing removed.

Method: documentation only; no commands were run.
