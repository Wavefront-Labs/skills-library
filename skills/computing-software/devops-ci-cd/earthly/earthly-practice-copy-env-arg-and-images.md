---
id: computing-software.devops-ci-cd.earthly.earthly-practice-copy-env-arg-and-images
name: earthly-practice-copy-env-arg-and-images
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, best-practices, copy, copy-dir, env, arg, save-image, build-context]
level: practitioner
status: docs-checked
description: "Earthfile practices: copy minimal files for cache, ENV versus ARG, COPY --dir, separate build and production images, outside-context files and manual cache."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthfile practices: COPY, ENV vs ARG, images

## COPY the minimum
Earthly treats `COPY` sources as build inputs; any change continues the build from that `COPY`. Avoid `COPY . .` and `COPY * ./`, and never copy `.git` without reason. Best form for Go:
```Dockerfile
COPY go.mod go.sum ./
RUN go mod download
COPY ./*.go ./
RUN go build ...
```
Use `COPY --dir dir-1 dir-2 dir-3 ./` to copy several directories in one command (it behaves like `cp`, not Dockerfile `COPY`).

## ENV vs ARG
`ENV` is stored in the final image and inherited via `FROM`, but cannot be overridden at call time or propagated with `BUILD +target --<key>=<value>`. `ARG` is overridable, expands in non-RUN commands and propagates between targets, but is not stored in the image. Use `ENV` for image config, `ARG` for build configurability.

## Separate build and production images
Build the binary in one target with `SAVE ARTIFACT ./build/app`, then start a fresh `FROM alpine:3.18`, install only production dependencies, `COPY +build/app /usr/bin/app`, set `ENTRYPOINT` and `SAVE IMAGE my-production-image:latest`.

## Files outside the build context
`COPY ../dir1/some-file.txt ./` does not work (the context of `./dir2/Earthfile` is `./dir2`). Add an Earthfile in `dir1` with a target that does `COPY some-file.txt ./` and `SAVE ARTIFACT ./some-file.txt`, then `COPY ../dir1+file/some-file.txt ./`. For files with no sensible Earthfile location use a `LOCALLY` target with `SAVE ARTIFACT $HOME/some-file.txt`, which is not allowed in `--strict` or `--ci`.

## Multi-line strings and commands
Open a quote on one line and close it on another for a multi-line `ARG` value. For commands, chain with `&&` and continue lines with `\`.

## SAVE IMAGE as a manual cache
For expensive steps that rarely change, push the base target as an image (`SAVE IMAGE --push earthly/blog-base-image:latest`) and `FROM` it later.

## Gotchas
- Downloading adds time; worth it only if the time saved clearly exceeds the pull.
- You must re-run the base target when it changes; a scheduled job reduces risk of inconsistency.
- Avoid non-deterministic ARGs, timestamps or generated IDs, which defeat caching.

## Checked

2026-11-07. Read docs/guides/best-practices.md in full. COPY, ENV, ARG and image practices match. Nothing removed.
Method: documentation only; no commands were run.
