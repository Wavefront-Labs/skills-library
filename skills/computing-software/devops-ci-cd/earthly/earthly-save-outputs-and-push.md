---
id: computing-software.devops-ci-cd.earthly.earthly-save-outputs-and-push
name: earthly-save-outputs-and-push
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, save-artifact, as-local, save-image, push, run-push, build, outputs]
level: practitioner
status: docs-checked
description: "Produce Earthly outputs: SAVE ARTIFACT AS LOCAL, SAVE IMAGE, BUILD to force outputs, and the --push flag for SAVE IMAGE and RUN --push side effects."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/basics/part-2-outputs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Save files and images, and push

Goal: get files and images out of a build, and gate external side effects behind `--push`.

## Local files
`SAVE ARTIFACT` alone only moves files between targets. Add `AS LOCAL` to write to your machine:

```Dockerfile
build:
    COPY main.go .
    RUN go build -o output/example main.go
    SAVE ARTIFACT output/example AS LOCAL local-output/go-example
```
`earthly +build` creates local-output/go-example.

## Images
`SAVE IMAGE go-example:latest` in a target makes `earthly +docker` produce that image, visible in `docker image ls` (or `podman image ls`).

## Outputs only when called directly
If a target is used via `FROM` or `COPY`, its outputs are NOT produced. Running `earthly +docker` where docker only does `COPY +build/example .` will not write local-output/go-example. The exception is `BUILD`:

```Dockerfile
docker:
    BUILD +build
    COPY +build/example .
    SAVE IMAGE go-example:latest
```

## Pushing
```Dockerfile
docker:
    SAVE IMAGE --push go-example:latest
```
`SAVE IMAGE --push` is not enough on its own; also run `earthly --push +docker`.

`RUN --push` runs commands with external effects only if the whole build succeeds and `--push` is passed:

```Dockerfile
release:
    RUN --push --secret GITHUB_TOKEN=GH_TOKEN github-release upload
migrate:
    FROM +build
    RUN --push bundle exec rails db:migrate
apply:
    RUN --push terraform apply -auto-approve
```
```bash
earthly --push +release
```

## Gotcha
Like saved files, `--push` commands take effect only when the target is called directly (`earthly --push +target`) or via `BUILD`; calling it through `FROM` or `COPY` does not invoke `--push`.

## Checked

2026-11-07. Read docs/basics/part-2-outputs.md in full. SAVE ARTIFACT, SAVE IMAGE, --push and output behaviour match. Nothing removed.
Method: documentation only; no commands were run.
