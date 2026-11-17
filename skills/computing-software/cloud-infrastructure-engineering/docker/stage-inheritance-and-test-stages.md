---
id: computing-software.cloud-infrastructure-engineering.docker.stage-inheritance-and-test-stages
name: stage-inheritance-and-test-stages
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, multi-stage, stage-inheritance, test-stage, lint-stage, from-stage, ci-gate]
level: practitioner
description: "Derive stages from earlier stages (FROM build AS test) to run tests, lint and scans inside the build, and make the runtime image depend on them so they gate production."
sources: ["https://docs.docker.com/build/building/multi-stage/#use-a-previous-stage-as-a-new-stage", "https://docs.docker.com/reference/dockerfile/#from", "https://docs.docker.com/build/building/best-practices/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deriving stages from previous stages (test and lint stages)

**Goal:** run unit tests and linters *inside* the Docker build so a production image cannot be
produced unless they passed, with no extra CI plumbing.

## The shape
```dockerfile
# syntax=docker/dockerfile:1
FROM node AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS build
COPY . .
RUN npm run build

FROM build AS test
RUN npm test && touch /tests-passed

FROM build AS lint
RUN npm run lint && touch /lint-passed

FROM node AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
# make runtime depend on test and lint so they must succeed first:
COPY --from=test /tests-passed /tmp/tests-passed
COPY --from=lint /lint-passed /tmp/lint-passed
CMD ["node", "dist/server.js"]
```
`FROM <stage>` starts a new stage from the filesystem and config of an earlier stage. `test` and
`lint` branch off `build`.

## Making tests gate production
With BuildKit only the stages the target depends on are built. The `COPY --from=test` lines create
that dependency, so building `runtime` forces `test` and `lint` to complete, and a failing test
fails the build. Avoid piping test output through another command in the `RUN` (a pipeline
reports the last command's status). To get real artefacts out for CI, copy them to a scratch stage
and use `docker build --target test --output type=local,dest=reports .` (local exporter).

## Where this is the wrong tool
- Tests that need sibling containers such as a database: use Compose or Testcontainers after the
  build instead.
- Tests needing secrets: `RUN --mount=type=secret` keeps the secret out of the image, but do not
  print it to the build log.

## Cache behaviour
Instructions are cached while their inputs are unchanged, and a changed instruction invalidates
every later instruction in that stage. Keep `COPY . .` as late as possible and exclude files
the tests do not need with `.dockerignore`.

## Gotchas
- A stage derived from another inherits its `USER`, `WORKDIR` and `ENV`; `runtime` starts from
  a fresh base, so redeclare `NODE_ENV` and similar there.
- The final image contains only what the last stage has; anything from `test` or `lint` reaches it
  only through `COPY --from`.

## Verify
Break a test on purpose and run `docker build -t app .`: the build must fail with the test output.

## Checked

Checked 2026-10-23 against docker/docs "Multi-stage builds" (using a previous stage as a new stage, BuildKit versus legacy builder), the Dockerfile reference (FROM, COPY --from, ENV) and best practices.
Confirmed: `FROM <stage>` semantics, BuildKit builds only the stages the target depends on, so a COPY --from dependency forces the stage to run. Fixed a real bug in the example: piping `npm test` through `tee` hid test failures, and the `/dev/null` copy target was replaced by marker files. Removed parallel-execution, `RUN --network=host` and `docker history` claims and pinned image tags.

Method: documentation only; no commands were run.
