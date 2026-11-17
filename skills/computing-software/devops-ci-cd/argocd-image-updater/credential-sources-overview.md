---
id: computing-software.devops-ci-cd.argocd-image-updater.credential-sources-overview
name: credential-sources-overview
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, authentication, credentials, credential-sources, serviceaccount, per-image-credentials, per-registry-credentials]
level: practitioner
status: docs-checked
description: "How Argo CD Image Updater authenticates to Kubernetes and registries: ServiceAccount token, per-registry versus per-image credentials, and the four credential source types."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/authentication.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Authentication overview

Kubernetes: as an in-cluster workload the updater uses the token of the ServiceAccount `argocd-image-updater-controller`, created by the install manifests together with a Role and RoleBinding. In the default `argocd` namespace nothing more is needed. If Argo CD lives elsewhere, adapt the RoleBinding to bind the ServiceAccount in the correct namespace.

Registries: private registries or private repositories on public registries need credentials. They can be set:

- per registry (all requests to that registry use them; cached for a configurable time, useful for externally generated limited-lifetime tokens)
- per image (overrides the registry credentials for repositories that need other credentials)
- or a mix of both

Supported credential source notations (`secret:`, `env:` and `ext:` data must be `<username>:<password>`; a pull secret holds a Docker config JSON in `.dockerconfigjson`):

| Notation | Source |
|---|---|
| `pullsecret:<namespace>/<secret_name>` | Docker pull secret with `.dockerconfigjson` |
| `secret:<namespace>/<secret_name>#<field>` | field of a generic Secret |
| `env:<variable_name>` | environment variable |
| `ext:<absolute_path_to_script>` | script that prints credentials |

By default the updater can read secrets only from the namespace it is installed in. The per-image field is `commonUpdateSettings.pullSecret` and the per-registry field is `credentials`.

## Checked

2026-11-04. Confirmed against authentication.md (ServiceAccount argocd-image-updater-controller with Role and RoleBinding, per-registry versus per-image credentials and caching, the four notations, default same-namespace secret reading) and images.md / registries.md for the field names pullSecret and credentials.

Method: documentation only; no commands were run.
