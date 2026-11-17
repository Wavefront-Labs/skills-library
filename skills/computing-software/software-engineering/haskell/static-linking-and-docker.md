---
id: computing-software.software-engineering.haskell.static-linking-and-docker
name: static-linking-and-docker
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, static-binary, musl, alpine, docker-multistage, -optl-static, ghc-static, distroless, glibc, static-linking-and-docker, haskell-deployment]
level: advanced
status: draft
description: "Build static Haskell binaries (musl/Alpine with -optl-static), multi-stage Docker images, and deal with glibc NSS and dynamic linking issues."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static binaries and Docker

**Goal:** ship a single self-contained executable or a small image.

## Static via Alpine (musl)
```dockerfile
# build stage (use an image that has GHC and cabal for Alpine, e.g. one built via ghcup; tag choice is yours)
FROM <alpine-ghc-cabal-image> AS build
RUN apk add --no-cache zlib-dev zlib-static gmp-dev ncurses-static libffi-dev
WORKDIR /src
COPY *.cabal cabal.project* ./
RUN cabal update && cabal build --only-dependencies -j      # cache dependencies layer
COPY . .
RUN cabal build -j --enable-executable-static \
      --ghc-options='-optl-static -optl-pthread' exe:myapp \
 && cp "$(cabal list-bin exe:myapp)" /myapp
FROM scratch                                   # or alpine:3.x for a shell / certs
COPY --from=build /myapp /myapp
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
ENTRYPOINT ["/myapp"]
```
Cabal has `--enable-executable-static`; Stack: `ghc-options: -optl-static`, `cc-options: -static`, `ld-options: -static` plus building in a musl container.

## Glibc dynamic images
For Debian/Ubuntu runtime images: copy the binary and install only `libgmp10`, `libffi8`, `zlib1g`, `ca-certificates` (names vary by release). Use `ldd ./myapp` to list shared libraries.

## Gotchas
- glibc static linking breaks `getaddrinfo`/NSS (name resolution warnings); musl avoids it. Linking warnings about `getpwnam` are expected with glibc.
- `-threaded` + static on musl works; `-fllvm` or TH-heavy projects need extra care (Template Haskell needs dynamic libraries on the build host).
- Image size: strip (`strip myapp`), `-split-sections` plus `-optl-Wl,--gc-sections`, UPX is optional (can break some runtimes).
- Cache layers: build dependencies before copying source. Pin base image digests.
- Run as non-root; set RTS options via `ENV GHCRTS=...` only if `-rtsopts` is on, preferably bake `-with-rtsopts`.
- ARM builds: use native runners or `docker buildx` for multi-arch.

## Self-check
- [ ] `ldd ./myapp` says "not a dynamic executable" for the static build.
- [ ] Container starts as non-root with only CA certs present.
