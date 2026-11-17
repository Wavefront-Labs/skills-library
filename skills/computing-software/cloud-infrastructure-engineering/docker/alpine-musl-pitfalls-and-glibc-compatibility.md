---
id: computing-software.cloud-infrastructure-engineering.docker.alpine-musl-pitfalls-and-glibc-compatibility
name: alpine-musl-pitfalls-and-glibc-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, image-slimming, alpine, musl, alpine-pitfalls, glibc-compat, gcompat, dns-musl, python-alpine-wheels, manylinux, musllinux]
level: practitioner
description: "Know when Alpine's musl libc breaks things (DNS, thread stacks, Python wheels, glibc-only binaries) and the fixes: musllinux wheels, explicit stack sizes, or a Debian slim base."
sources: ["https://wiki.musl-libc.org/functional-differences-from-glibc.html", "https://github.com/docker-library/docs/tree/master/alpine", "https://peps.python.org/pep-0656/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alpine and musl: pitfalls and compatibility fixes

**Goal:** use Alpine's small base where it works and recognise the symptoms when it does not,
instead of debugging musl for a day. The official image is built around musl libc and BusyBox.

## Where musl differs from glibc (the ones that bite)
- **DNS**: musl queries all `resolv.conf` nameservers in parallel and takes the first answer
  (it supports at most three), so nameservers must agree. The resolver supports `search`/`domain`
  since musl 1.1.13, but a name with at least `ndots` dots is only tried in the global namespace
  (glibc would fall back to the search list). `search` lines over 256 characters are ignored.
  DNS over TCP is supported only from musl 1.2.4, so older musl cannot handle large responses
  (DNSSEC-sized packets); check which musl version your Alpine tag ships.
- **Threads/stack**: new threads get a 128k default stack on musl, against a glibc default of
  roughly 2-10 MB (taken from `RLIMIT_STACK`). Code that recurses deeply in threads can overflow.
  Fix in the program: `pthread_attr_setstacksize`, or link with `-Wl,-z,stack-size=N` (musl 1.1.21+).
- **Locale/iconv**: musl's default locale is `C.UTF-8` and its `iconv` covers fewer encodings
  than glibc's.
- **Binaries**: programs linked against glibc cannot run unchanged on a musl-only image.

## Symptoms and fixes
| Symptom | Cause | Fix |
|---|---|---|
| `exec /bin/foo: no such file or directory` though file exists | dynamic binary built for glibc (its loader is missing) | rebuild for musl, or use a Debian-based image |
| `pip install` compiles for minutes / fails on `gcc` | wheels tagged `manylinux` do not apply to musl | use a `-slim` Debian Python image, or a package that ships `musllinux` wheels (PEP 656) |
| Slow/flaky lookups in a container | musl resolver behaviour above | use fully qualified names, avoid long search lists, keep nameservers consistent |
| `ps`, `grep` options differ | BusyBox utilities | install the full tool via `apk add` or switch base |

## When to choose Alpine anyway
Static binaries, shell-based tooling images, or anything where the vendor publishes an alpine
tag and tests it. Distroless can be a better "small" answer for compiled languages because it
avoids musl entirely.

## apk idioms
```dockerfile
RUN apk add --no-cache ca-certificates tzdata
```
`--no-cache` avoids keeping the package index in the layer (the official image page shows
`apk add --no-cache`). Pin an explicit Alpine tag rather than `latest`.

## Gotchas
- Alpine's `/bin/sh` is BusyBox: scripts written for bash may need bash installed.
- `adduser` flags differ from Debian's; check `adduser --help` in the image.

## Verify
`docker run --rm img ldd /path/bin` shows the musl loader; a `pip install` of a C-extension
package finishes without invoking a compiler.

## Checked
2026-11-01. Confirmed on the musl "functional differences from glibc" wiki: parallel
nameserver queries, three-nameserver limit, search/ndots behaviour, 256-character search
limit, TCP DNS from 1.2.4, 128k thread stack versus glibc 2-10 MB, stack-size link option
since 1.1.21, `C.UTF-8` default locale, smaller iconv. Confirmed on PEP 656: musllinux wheel
tags. Confirmed on the Docker official alpine page: musl and BusyBox, `apk add --no-cache`.
Removed: the Alpine version that ships musl 1.2.4, mimalloc and LD_PRELOAD advice, gcompat,
image sizes, pip and JDK version specifics, the `-virtual` build-deps pattern, the
`frolvlad` image, `set -o pipefail` and `[[ ]]` claims, the ldconfig/getent claim, and the
wrong "setlocale returns C" statement (musl defaults to `C.UTF-8`).
Method: documentation only; no commands were run.
