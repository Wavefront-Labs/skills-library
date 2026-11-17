---
id: computing-software.devops-ci-cd.verdaccio.throwaway-registry-for-e2e
name: throwaway-registry-for-e2e
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [e2e-testing, throwaway-registry, ci-registry, e2e-registry, runserver, verdaccioctl, registry-cli, github-actions]
level: advanced
status: docs-checked
description: "Publish and install against a disposable Verdaccio in CI: Docker service container, open publish config, dummy token, ping wait loop, and EPUBLISHCONFLICT."
sources:
  - https://verdaccio.org/docs/e2e/
  - https://verdaccio.org/docs/github-actions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A throwaway registry tests the real tarball (files, exports, workspace ranges) without burning npmjs versions or leaking tokens.

Config (publish open only because it is discarded):
```yaml
storage: ./storage
uplinks:
  npmjs:
    url: https://registry.npmjs.org/
packages:
  '@my-company/*':
    access: $all
    publish: $all
    unpublish: $all
  '**':
    access: $all
    proxy: npmjs
log: { type: stdout, format: pretty, level: warn }
```
Run: `docker run -d --name verdaccio -p 4873:4873 -v "$PWD/verdaccio.yaml:/verdaccio/conf/config.yaml" verdaccio/verdaccio:6` (no data volume, so each run starts empty). Wait with:
```
until npx @verdaccio/registry-cli ping -r http://localhost:4873; do sleep 0.5; done
```
In GitHub Actions use a `services: verdaccio: image: verdaccio/verdaccio:6, ports: 4873:4873` container (default config allows anonymous publish).

Gotchas:
- npm refuses to publish without a token even if allowed: add `//localhost:4873/:_authToken=e2e-dummy-token` (not validated; the key must match host and port).
- A second publish of the same version gives `EPUBLISHCONFLICT`; use empty storage or `npm version "1.0.0-e2e.$(date +%s)" --no-git-tag-version`.
- Install the package in a fresh directory with `--min-release-age=0` and its own `.npmrc`.
- `verdaccioctl login` 1.1.0 only works for non-existing users and still exits 0.
- `verdaccio_started` is sent to a forking parent process.

## Checked

2026-11-04. Confirmed against the Verdaccio End-to-end testing page (config, ping wait loop, GitHub Actions service container and anonymous publish, dummy auth token, EPUBLISHCONFLICT, fresh directory with its own .npmrc, verdaccioctl login 1.1.0 behaviour, verdaccio_started). Nothing removed.
Method: documentation only; no commands were run.
