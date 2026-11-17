---
id: computing-software.software-engineering.crystal.alpine-static-build
name: alpine-static-build
category: computing-software
field: software-engineering
product: crystal
tags: [alpine-static-build, docker-static, static-build, alpine, musl, docker, static-binary, scratch, openssl-static, release, crystal]
level: practitioner
status: draft
description: "Build a fully static Crystal binary in an Alpine container using --static --release with static libs for ssl, yaml, pcre and gc."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static binaries on Alpine with musl

Goal: ship one file.

- Use the official image `crystallang/crystal:<version>-alpine`, which includes static libs for gc, pcre2, libevent, openssl, libyaml, zlib (confirm per release).
- Build: `shards build --release --static --no-debug` (or `crystal build --static --release`).
- Verify static: `ldd bin/app` prints "not a dynamic executable"; `file bin/app` says statically linked.
- Run in `FROM scratch` or `alpine`; copy CA certs (`/etc/ssl/certs/ca-certificates.crt`) and tzdata/zoneinfo if used.
- glibc distros: full static linking is not supported by glibc (NSS, dlopen); use musl.

Gotchas:
- Extra C libs need their `.a` archives (install `-static` packages, e.g. `apk add openssl-libs-static`).
- The musl DNS resolver and `getaddrinfo` behave slightly differently (no search domains in some cases).
- Native libs that use dlopen cannot be static.

Verify: run the binary in a `scratch` container.
