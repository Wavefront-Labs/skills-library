---
id: computing-software.qa-testing-engineering.cypress.cypress-docker-images
name: cypress-docker-images
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-docker, cypress-included, cypress-factory, docker-ci]
level: practitioner
status: docs-checked
description: "Run Cypress in Docker with official images (cypress/base, cypress/browsers, cypress/included, cypress/factory), pin versions, mount the project and fix permission issues."
sources:
  - https://github.com/cypress-io/cypress-docker-images
  - https://github.com/cypress-io/cypress-docker-images/blob/master/included/README.md
  - https://github.com/cypress-io/cypress-docker-images/blob/master/factory/README.md
  - https://docs.cypress.io/app/continuous-integration/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cypress Docker images

| Image | Contains | Use |
|---|---|---|
| `cypress/base:<node>` | OS dependencies and Node, no Cypress, no browsers | you install Cypress via npm |
| `cypress/browsers:<tag>` | base plus Chrome, Firefox and Edge (Edge on amd64; arm64 per the repo README) | install Cypress yourself, run real browsers |
| `cypress/included:<tag>` | browsers plus the Cypress binary, `ENTRYPOINT` `cypress run` | run tests without npm install of Cypress |
| `cypress/factory` | a template image configured with build `ARG`s (`NODE_VERSION`, `CYPRESS_VERSION`, `CHROME_VERSION`, ...) | custom images |

## cypress/included
```bash
docker run -it --rm -v "$PWD":/e2e -w /e2e --entrypoint cypress cypress/included:<cypress-version> run -b chrome --spec "cypress/e2e/smoke/*"
```
The image `ENTRYPOINT` is `cypress run`, which uses the default Electron browser (deprecated as a test browser in Cypress 16); to pass options such as `-b chrome`, override the entrypoint with `--entrypoint cypress` and give `run ...` as shown. Remove `cypress` from your project's `package.json` to avoid a version mismatch with the image. The app under test must be reachable from the container, for example through a compose network service name.

## docker compose
```yaml
services:
  web: { build: ., ports: ["3000:3000"] }
  e2e:
    image: cypress/included:<cypress-version>
    depends_on: [web]
    environment: { CYPRESS_baseUrl: http://web:3000 }
    working_dir: /e2e
    volumes: ["./:/e2e"]
    entrypoint: ["cypress"]
    command: ["run", "-b", "chrome"]
```

## factory
```dockerfile
ARG NODE_VERSION=<exact node version>
ARG CHROME_VERSION=<exact chrome version>
ARG CYPRESS_VERSION=<cypress version>
FROM cypress/factory:<factory-version>
COPY . /app
WORKDIR /app
RUN npm ci
```
Versions must be exact (no wildcards or shorthands). Specify a fixed `cypress/factory` tag rather than `latest`.

## Gotchas
- Pin full tags (`cypress-<cypress version>-node-<node version>-chrome-<chrome version>-ff-<firefox version>-edge-<edge version>`): the short `<cypress version>` tag is moveable and can pick up newer browsers, and `latest` is updated without notice.
- Browser crashes can mean too little CPU or memory on the machine (the Cypress CI guide lists crashes as a sign); check with `cypress info`.
- Chrome for Testing is not included in `cypress/browsers` or `cypress/included`; add it with the factory `CHROME_FOR_TESTING_VERSION` build argument.

## Verify
`docker run --rm --entrypoint cypress cypress/included:<v> info` prints the Cypress and browser versions; the test run passes in the container.

## Checked
Checked against the Cypress documentation sources (cypress-io/cypress-documentation, docs/, last commit 2026-10-24, which document Cypress 16; latest release v16.2.0) and the cypress-io/cypress-docker-images repository (README, included and factory docs, last commit 2026-10-23). Confirmed: image purposes, ENTRYPOINT `cypress run`, `--entrypoint cypress` for options, tag formats and pinning advice, factory build arguments and exact-version rule, Chrome for Testing note, Electron deprecation, `cypress info`. Removed the unconfirmed `--ipc=host`/`--shm-size` and root-ownership advice and the pinned example versions.

Method: documentation only; no commands were run.
