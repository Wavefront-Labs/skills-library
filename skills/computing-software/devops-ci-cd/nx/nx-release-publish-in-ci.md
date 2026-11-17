---
id: computing-software.devops-ci-cd.nx.nx-release-publish-in-ci
name: nx-release-publish-in-ci
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, ci, github-actions, npm, provenance, docker]
level: practitioner
status: docs-checked
description: "Move nx release publishing into CI: --skip-publish locally, nx release publish on tag, NODE_AUTH_TOKEN, npm provenance, the 3-tag GitHub limit and Docker publishing."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/publish-in-ci-cd.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: version and tag locally, publish from a pipeline.

1. Locally: `nx release --skip-publish` (skips the "Do you want to publish these versions?" prompt; commits version and changelog changes and creates the tag).
2. `git push && git push --tags`.
3. CI runs `nx release publish` (publish step only; runs the `nx-release-publish` target per project).

GitHub Actions example essentials: trigger `on: push: tags: ['v*.*.*']`; `permissions: contents: read, id-token: write`; checkout with `fetch-depth: 0`; `actions/setup-node` with `registry-url: https://registry.npmjs.org/`; install; `npx nx release publish` with env `NODE_AUTH_TOKEN: ${{ secrets.NPM_ACCESS_TOKEN }}` and `NPM_CONFIG_PROVENANCE: true`.

Token: create an npm Granular Access Token with read/write on the packages and their org, store it as a repo secret (the name NPM_ACCESS_TOKEN only has to match the workflow). Provenance needs `NPM_CONFIG_PROVENANCE=true` plus `id-token: write`.

Independent versioning gotcha: one tag per project, and GitHub does not fire `push` workflows when more than 3 tags are pushed at once. Workarounds: a `workflow_dispatch` trigger run manually after pushing; trigger on push to `main` with `paths: ['**/package.json']` and add logic to detect a release; or push tags in batches of 3 or fewer.

Docker (experimental; supported in standard CI such as GitHub Actions, GitLab CI and Jenkins; for Nx Cloud Agents the page says to contact Nx Enterprise support): images are built with `npx nx run-many -t docker:build`, tagged at version time, pushed at publish time. Log in to the registry first, then:

```shell
npx nx release version --dockerVersionScheme=production
npx nx release publish
```
Alternate registry: `{ "release": { "docker": { "registryUrl": "ghcr.io" } } }`. Changelog afterwards: `npx nx release changelog <version>`.

## Checked

2026-11-07. Confirmed against Publish in CI/CD: --skip-publish and the publish prompt, nx release publish running nx-release-publish per project, the GitHub Actions workflow (tag trigger v*.*.*, contents read and id-token write permissions, fetch-depth 0, setup-node registry-url, NODE_AUTH_TOKEN from a secret, NPM_CONFIG_PROVENANCE), the Granular Access Token advice and secret naming note, the more-than-3-tags push limitation with its three workarounds, the Docker flow (docker:build, tag at version time, push at publish time, --dockerVersionScheme=production, registryUrl ghcr.io, nx release changelog <version>). Removed: the claim that Docker publishing does not work with Nx Cloud Agents (the page only says to contact support), and the invented dry-run Verify step.

Method: documentation only; no commands were run.
