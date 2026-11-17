---
id: computing-software.devops-ci-cd.renovate.docker-digest-pinning
name: docker-digest-pinning
category: computing-software
field: devops-ci-cd
product: renovate
tags: [docker, pin-digests, image-tags, renovate]
level: practitioner
status: docs-checked
description: "How Renovate updates Docker images, preserves version precision and suffixes, and pins digests with pinDigests."
sources:
  - https://docs.renovatebot.com/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate updates image references in Dockerfiles, Docker Compose files, dev containers, CircleCI config, Kubernetes manifests and Ansible files. It scans for files matching each manager's `managerFilePatterns`, parses image references, and queries the registry when the tag looks like a version such as `myimage:1.1.0`.

Behaviours to know:

- Precision is preserved. `myimage:1.1` only moves to `1.2` or `1.3`, never to `1.2.0`.
- Suffixes indicate compatibility. `1.2.0-alpine` goes to `1.2.1-alpine`, never to `1.2.1` or `1.2.1-stretch`.
- To treat suffixes as SemVer pre-releases, set `versioning` per package, for example `semver`, or `pep440` for the official `python` image.

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

`pinDigests` pins Docker images (and GitHub Actions) by SHA256 digest as well as tag, making them immutable; the `docker:pinDigests` preset enables it. The docs recommend pinning Docker images to a digest; Renovate keeps the tag in the `FROM` line for readability and raises PRs when the tagged image changes. To disable digest pinning add the `default:pinDigestsDisabled` preset; `docker:disable` and `docker:disableMajor` also exist.

## Checked

2026-11-03. Confirmed against the Renovate Docker page (supported file types, precision, suffix and `pep440` behaviour, digest pinning and updating, presets) and the configuration options page (`pinDigests` default `false`, the `docker:pinDigests` preset is described on the Docker page). Removed the unsupported `hostRules`, `registryAliases` and digest grouping advice.

Method: documentation only; no commands were run.
