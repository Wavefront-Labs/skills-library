---
id: computing-software.devops-ci-cd.renovate.renovate-docker-and-compose
name: renovate-docker-and-compose
category: computing-software
field: devops-ci-cd
product: renovate
tags: [docker-compose, kubernetes, managerfilepatterns, renovate]
level: practitioner
status: docs-checked
description: "Make Renovate find image references in Compose, Kubernetes and custom file names with managerFilePatterns."
sources:
  - https://docs.renovatebot.com/docker/
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate upgrades Docker image references in Dockerfiles, Docker Compose files (`docker-compose.yml`, `compose.yml`), dev containers and GitHub Codespaces images, CircleCI config, Kubernetes manifests and Ansible configuration. Each manager looks only at files matching its `managerFilePatterns`; patterns you add extend the defaults and cannot remove them. The `kubernetes` manager has an empty default list, so you must tell Renovate which files to check. If your files use unusual names, extend the pattern for that manager.

```json
{
  "dockerfile": {
    "managerFilePatterns": ["/(^|/)Containerfile$/", "/\\.dockerfile$/"]
  },
  "kubernetes": {
    "managerFilePatterns": ["/^k8s/.+\\.ya?ml$/"]
  }
}
```

Notes:

- Patterns are RE2 regexes (between slashes) or globs.
- The docs recommend pinning images to an exact digest (`pinDigests`, default `false`) so builds are immutable; Renovate keeps the tag in the `FROM` line next to the digest and then opens PRs when the digest changes.
- Renovate preserves version precision: `myimage:1.1` is only upgraded to `myimage:1.2` or `1.3`, never to `1.2.0`.
- Suffixes are treated as compatibility markers: `1.2.0-alpine` goes to `1.2.1-alpine`, never to `1.2.1` or `1.2.1-stretch`. If an image uses SemVer pre-release suffixes, override `versioning` in a `packageRules` entry, for example:

```json
{
  "packageRules": [
    {
      "matchDatasources": ["docker"],
      "matchPackageNames": ["foo/bar"],
      "versioning": "semver"
    }
  ]
}
```

The docs name `pep440` for the official `python` image, plus `loose` and `regex` versioning as fallbacks. `registryAliases` (supported by managers including `docker-compose`, `dockerfile`, `kubernetes` and `devcontainer`) sets aliases for registries, and supports variables with `:-` defaults, which is useful for Compose files. Private registries and Docker Hub credentials are configured with `hostRules`.

## Checked

2026-11-09: read https://docs.renovatebot.com/docker/ through the digest pinning section, the managerFilePatterns, pinDigests and registryAliases sections of https://docs.renovatebot.com/configuration-options/. Removed the custom-manager, digest-grouping and pull-through mirror claims (not on the pages) and replaced the manager list with the page's.

Method: documentation only; no commands were run.
