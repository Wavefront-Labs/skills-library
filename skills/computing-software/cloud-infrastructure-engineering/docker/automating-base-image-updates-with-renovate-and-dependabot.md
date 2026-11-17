---
id: computing-software.cloud-infrastructure-engineering.docker.automating-base-image-updates-with-renovate-and-dependabot
name: automating-base-image-updates-with-renovate-and-dependabot
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, base-image, base-image-updates, renovate-docker, dependabot-docker, digest-pinning, automation, dependency-updates, compose-image-updates]
level: practitioner
description: "Configure Renovate or Dependabot to bump Dockerfile FROM lines, Compose image tags and pinned digests automatically, with grouping, schedules and version constraints."
sources: ["https://docs.renovatebot.com/modules/manager/dockerfile/", "https://docs.renovatebot.com/docker/", "https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automating base image updates

**Goal:** pinned base images that still receive security rebuilds, via pull requests you can
review and CI can test, with no manual digest chasing.

## Renovate
`renovate.json`:
```json
{
  "extends": ["config:recommended", "docker:pinDigests"],
  "packageRules": [
    {"matchDatasources": ["docker"], "matchPackageNames": ["python"], "versioning": "pep440"}
  ]
}
```
- Renovate upgrades image references in Dockerfiles, Docker Compose files, dev containers,
  CircleCI config, Kubernetes manifests and Ansible configuration.
- The Dockerfile manager handles `FROM` (multi-stage, `--platform`, `AS <name>`), `COPY --from`,
  `RUN --mount` images, `# syntax=` images, and pinned `apk add` / `apt-get install` packages (the
  package lookups are skipped with `unknown-registry` until you give a `registryUrls` rule).
- Renovate expands variables and `ARG` directives in `FROM` (for example `ARG TAG=3.19.4` then
  `FROM alpine:${TAG}`).
- Digest pinning is recommended by the docs: with it, Renovate keeps the tag in the line
  (`FROM node:14.15.1@sha256:...`) and opens PRs when the tag's image changes. Disable it with
  `"ignorePresets": ["docker:pinDigests"]` or `default:pinDigestsDisabled`.
- Automerge of digest updates: add `default:automergeDigest` to `extends`
  (`default:automergeBranchPush` to commit straight to the base branch).
- Precision and suffixes: Renovate keeps the precision you wrote (`myimage:1.1` goes to
  `1.2`, not `1.2.0`) and treats suffixes as compatibility, so `1.2.0-alpine` becomes
  `1.2.1-alpine`, never `1.2.1` or `1.2.1-stretch`. Change the scheme per package with `versioning`
  (`semver`, `pep440`, built-in `loose`, or `regex`).
- Debian code names are understood: `debian:bullseye` can be offered `debian:bookworm`.
- Private registries: configure `hostRules`; the Renovate Docker page has recipes for ECR, GCR and others.

## Dependabot
`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: docker
    directory: /
    schedule: {interval: weekly}
  - package-ecosystem: docker-compose
    directory: /deploy
    schedule: {interval: weekly}
```
- Ecosystem names are `docker` (Dockerfiles) and `docker-compose` (Compose files, versions v2 and v3).
- `schedule.interval` accepts `daily`, `weekly`, `monthly`, `quarterly`, `semiannually`, `yearly`
  or `cron`.
- Use `directories` (supports globbing and `*`) instead of `directory` to cover several folders.
- `ignore` rules and `groups` exist; if a dependency matches both `allow` and `ignore`, it is ignored.
- Private registries go in the top-level `registries` key.

## Making the PRs safe to merge
- CI must **build and test** the image on the PR; otherwise a bumped base that drops a
  library ships to production untested.
- Rebuild and publish on merge so the fix actually reaches the registry.
- For digest-only bumps, automerge after CI is reasonable; for tag bumps, require review.
- A tag whose digest changes because the publisher rebuilt it is exactly the PR you want.

## Verify
Push an intentionally old base image reference; within the configured schedule a PR appears
proposing the newer digest or tag.

## Checked
Checked 2026-10-28 against the Renovate "Docker" and "Dockerfile" manager pages and the GitHub Docs
dependabot.yml reference: supported file types, FROM/ARG expansion, digest pinning and presets,
automerge presets, suffix and precision rules, versioning options, ecosystem names, schedule
intervals, `directories`, allow versus ignore precedence. Corrected: the earlier claim that Renovate
does not update ARG-driven FROM lines is wrong. Removed as unconfirmed: manager list entries for
`helm-values`, `bake` and `github-actions`, the schedule and `allowedVersions` rules, the `loose`
auto-detection claim, Dependabot date claims (digest updates 2022, Compose 2024), Dependabot
automerge and grouping limits, the `pinDigests: false` single-arch advice, Docker Hub rate-limit
advice and the stage-name parser claim.
Method: documentation only; no commands were run.
