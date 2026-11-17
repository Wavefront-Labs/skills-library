---
id: computing-software.cloud-infrastructure-engineering.docker.choosing-distroless-variants
name: choosing-distroless-variants
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, image-slimming, distroless, distroless-variants, static-vs-base, distroless-debug, distroless-cc, nonroot-tag, gcr-distroless]
level: practitioner
description: "Pick the right gcr.io/distroless variant (static, base, cc, java, python, nodejs; :debug and :nonroot tags) for a binary's runtime needs, and know what each one omits."
sources: ["https://github.com/GoogleContainerTools/distroless", "https://github.com/GoogleContainerTools/distroless/blob/main/base/README.md", "https://github.com/GoogleContainerTools/distroless/blob/main/cc/README.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing a distroless variant

**Goal:** match the distroless image to what the binary links against, so it runs — and
nothing else is in the image.

## The ladder (smallest first)
| Image | Contains | Use for |
|---|---|---|
| `static-debian13` | ca-certificates, a `/etc/passwd` entry for root, `/tmp`, tzdata | fully static binaries: Go with CGO_ENABLED=0 |
| `base-nossl-debian13` | static + glibc | libc-dependent binaries that do not need libssl |
| `base-debian13` | static + glibc + libssl (Debian 13 also adds libssl's dependencies zlib and libzstd) | Go apps needing libc/cgo and most other apps |
| `cc-debian13` | everything in base, plus libgcc1 and its dependencies | "mostly-statically compiled" Rust and D binaries |
| `java-base-debian13`, `java17-debian13`, `java21-debian13`, `java25-debian13` | Java runtime variants | JARs |
| `python3-debian13` | Python 3 runtime | python apps |
| `nodejs22-debian13`, `nodejs24-debian13`, `nodejs26-debian13` | Node.js runtime | node apps |

Each image comes in tags `latest`, `nonroot`, `debug` and `debug-nonroot`. Per-architecture tags add a suffix
(`gcr.io/distroless/static-debian13:latest-amd64`); tags not listed in the project's README are deprecated and no longer
updated. Images without a distribution suffix currently select Debian 13 but that will move to a newer Debian, so
name the suffix explicitly. Check the project README for the current list before pinning; older `-debian12`
images are no longer listed.

## Decide by ldd, not by guesswork
`ldd` is a shell script and is not in the distroless images, so run it in the builder stage:
```sh
ldd ./app
#   not a dynamic executable            -> static
#   libc.so.6 only                      -> base-nossl
#   libssl                              -> base
#   libgcc                              -> cc
```
Anything else (libz, libsqlite3, libpq, libmagic, image libs) is not listed in any variant's contents (Debian 13 `base` does
add zlib and libzstd as libssl dependencies); either build statically, copy the `.so` files from the builder into the same
paths, or switch to a slim Debian base.

## Entry point rules
No shell exists (except `:debug`), so `ENTRYPOINT` must be in vector (exec) form: `ENTRYPOINT ["/app"]`, not
`ENTRYPOINT "/app"`. Static, base and cc images have an empty entrypoint, so give `CMD` in vector form too. Images with
a language runtime (java, nodejs, python3) have a language-specific default entrypoint: read the project README
examples for the right `CMD`.

## Typical Dockerfile
```dockerfile
FROM golang:1.23 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app .

FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
Multi-stage builds need Docker 17.05 or higher.

## What you give up
- No package manager or shell (and no `ldd`); healthchecks must be done by the orchestrator or inside your own binary.
- Debugging: use the `:debug` tag, which provides a busybox shell
  (`docker run --entrypoint=sh -ti img`); for an existing tag use `debug-<tag>`, e.g. `debug-nonroot`. Do not ship
  `:debug` to production.

## Gotchas
- Images are signed with cosign (keyless); verify before building on one:
  `cosign verify $IMAGE_NAME --certificate-oidc-issuer https://accounts.google.com --certificate-identity keyless@distroless.iam.gserviceaccount.com`.
- `python3` variant: no package install at runtime; build dependencies in a builder stage and copy them in, matching
  the Python minor version.
- Debian 13 `base` does not include OpenSSL legacy algorithms; add the `openssl-legacy-provider` yourself if needed.

## Verify
`docker run --rm img` starts; `docker run --rm --entrypoint sh img` fails (the non-debug image has no shell).
The smallest image, `static-debian13`, is about 2 MiB per the project README.

## Checked
2026-10-28. Confirmed against the distroless README and its base and cc READMEs: image list, tags, Debian 13 default,
static/base/base-nossl/cc contents, entrypoint rules, debug tag naming, ldd absence, cosign verify command, Docker 17.05
for multi-stage builds, about 2 MiB static size. Removed (not stated in those pages): `-debian12` names, uid 65532,
`nonroot` user name and `HOME`, libstdc++ in cc, `/busybox/sh` path, scanner and CVE-count claims, `-ldflags`, size
guess, `docker image inspect` check.
Method: documentation only; no commands were run.
