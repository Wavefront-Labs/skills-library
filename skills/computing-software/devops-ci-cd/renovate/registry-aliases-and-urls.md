---
id: computing-software.devops-ci-cd.renovate.registry-aliases-and-urls
name: registry-aliases-and-urls
category: computing-software
field: devops-ci-cd
product: renovate
tags: [registry-aliases, registry-urls, default-registry-urls, renovate]
level: practitioner
status: docs-checked
description: "Redirect or replace package registries with registryAliases, registryUrls and defaultRegistryUrls."
sources:
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three options control which registries Renovate queries:

- `registryUrls` is a list of URLs to try for dependency lookup, typically set inside a `packageRules` entry. The field supports multiple URLs, but whether only the first or several are used depends on the datasource. Managers that cannot tell which registry a dependency uses skip it with `skipReason: unknown-registry`; setting `registryUrls` for it makes Renovate use them.
- `defaultRegistryUrls` is the fallback list for a datasource, used only when the manager extracted no `registryUrls` and none were applied through config. It works only if the datasource's `customRegistrySupport` is `true`.
- `registryAliases` maps an alias to a real registry. Renovate applies all alias objects top to bottom. Aliases support variables with defaults using the `:-` syntax, which is useful in Docker Compose files.

```json
{
  "registryAliases": {
    "$MY_REGISTRY": "registry.example.com/mirror"
  },
  "packageRules": [
    {
      "matchDatasources": ["maven"],
      "registryUrls": ["https://repo.example.com/maven2"]
    }
  ]
}
```

`registryAliases` works with specific managers only: `ansible`, `argocd`, `bazel-module`, `bitbucket-pipelines`, `circleci`, `crow`, `docker-compose`, `dockerfile`, `droneci`, `fleet`, `flux`, `github-actions`, `gitlabci`, `helm-requirements`, `helm-values`, `helmfile`, `helmsman`, `helmv3`, `kubernetes`, `terraform` and `woodpecker`. It can also be set inside one manager's object, for example `gitlabci`, and aliases can use variables with defaults such as `${CI_REGISTRY:-}`.

## Checked

2026-11-09: read the registryAliases, registryUrls and defaultRegistryUrls sections of https://docs.renovatebot.com/configuration-options/. Completed the manager list and removed the unsourced `hostRules` and release-list merging remarks.

Method: documentation only; no commands were run.
