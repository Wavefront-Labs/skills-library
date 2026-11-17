---
id: computing-software.cloud-infrastructure-engineering.docker.from-platform-flag-and-stage-naming-rules
name: from-platform-flag-and-stage-naming-rules
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, from-platform-flag, from-instruction, stage-name, buildplatform, targetplatform, build-checks]
level: practitioner
status: docs-checked
description: "Use FROM --platform correctly (BUILDPLATFORM vs TARGETPLATFORM vs constants) and name stages so build checks pass: lowercase, unique, no reserved names."
sources: ["https://docs.docker.com/reference/dockerfile/#from", "https://docs.docker.com/reference/dockerfile/#automatic-platform-args-in-the-global-scope", "https://docs.docker.com/reference/build-checks/from-platform-flag-const-disallowed/", "https://docs.docker.com/reference/build-checks/reserved-stage-name/", "https://docs.docker.com/build/building/multi-platform/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FROM --platform and stage naming rules

Form: `FROM [--platform=<platform>] <image>[:<tag>|@<digest>] [AS <name>]`

## When to pass --platform
| Value | Use |
|---|---|
| omitted | The target platform of the build request is used (the `--platform` given to the build command) |
| `--platform=$BUILDPLATFORM` | Toolchain stages that cross-compile: run natively, emit binaries for `$TARGETOS/$TARGETARCH` |
| `--platform=$TARGETPLATFORM` | Redundant: same as omitting it (build check `RedundantTargetPlatform`) |
| `--platform=linux/amd64` (constant) | Forces one platform, which prevents a multi-platform build from this Dockerfile; build check `FromPlatformFlagConstDisallowed` warns. Prefer omitting it and passing `--platform` on the command line |

```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang AS build
ARG TARGETOS TARGETARCH
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o /out/app ./cmd/app

FROM scratch AS final
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
`BUILDPLATFORM`, `TARGETPLATFORM`, `TARGETOS`, `TARGETARCH` and the other automatic platform ARGs
are defined in the global scope, so they work in `FROM` without an `ARG` line; inside a stage,
redeclare one without a value (`ARG TARGETARCH`) to read it.

## Stage naming rules
- Names are referenced by `FROM <name>`, `COPY --from=<name>`, `RUN --mount=from=<name>` and
  `--target <name>`.
- Use lowercase stage names: the `StageNameCasing` check requires them.
- Keep keyword casing consistent: mixing `FROM` with `as` (or `from` with `AS`) triggers
  `FromAsCasing`.
- Names must be unique (`DuplicateStageName`; duplicate names make the build fail) and must not
  be the reserved words `scratch` or `context` (`ReservedStageName`).

## Gotchas
- `--platform=$BUILDPLATFORM` stages run on the build node, so keep steps that must run the
  target-platform binary in a stage without the flag.
- A constant `--platform` pins the stage to one platform, so a multi-platform build from that
  Dockerfile cannot produce the other variants.
- An `ARG` used in an image reference must give a valid reference when no build args are passed
  (`InvalidDefaultArgInFrom`); an undeclared one triggers `UndefinedArgInFrom`.

## Verify
```bash
docker build --check .      # runs build checks without building
docker buildx build --platform linux/amd64,linux/arm64 -t <registry>/<repo>:<tag> --push .
docker buildx imagetools inspect <registry>/<repo>:<tag>   # lists the platforms in the index
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (FROM, ARG and FROM, automatic platform ARGs; moby/buildkit docs main) and the BuildKit rule pages for FromPlatformFlagConstDisallowed, RedundantTargetPlatform, ReservedStageName, StageNameCasing, FromAsCasing, DuplicateStageName, InvalidDefaultArgInFrom and UndefinedArgInFrom.
Confirmed: `--platform` default is the target platform; `$BUILDPLATFORM` use for cross-compiling stages; `$TARGETPLATFORM` is redundant; a constant platform blocks multi-platform builds; reserved names are `scratch` and `context`; global-scope ARG redeclaration. Removed unconfirmed claims about stage names shadowing images, `COPY --from=<index>` and pinned base-image tags.

Method: documentation only; no commands were run.
