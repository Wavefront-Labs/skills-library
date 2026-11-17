---
id: computing-software.cloud-infrastructure-engineering.docker.debian-slim-variants-and-when-to-use-them
name: debian-slim-variants-and-when-to-use-them
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, image-slimming, slim-variant, debian-slim, python-slim, node-slim, bookworm-slim, image-size, base-image]
level: practitioner
description: "What the -slim tags of debian/python/node actually strip, when slim beats alpine or distroless, and how to add back exactly the packages an app needs."
sources: ["https://hub.docker.com/_/debian", "https://hub.docker.com/_/python", "https://hub.docker.com/_/node"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debian slim variants

**Goal:** a glibc base that is much smaller than the full tag without the musl or no-shell
trade-offs. Compare real sizes with `docker image ls` rather than trusting a number.

## What "slim" removes
`debian:<suite>-slim` is a slimmer Debian base with extra files that are normally not needed
in containers (such as man pages and documentation) removed; Docker Hub calls the tags an
experiment that is subject to change. `python:<version>-slim` drops the common Debian packages
of the default tag (which is built on buildpack-deps) and keeps only the minimal packages
needed to run Python, so it has none of the Debian packages needed to compile extension
modules. Consequence: `pip install` works when a built distribution (wheel) exists and may
fail when it must build from a source distribution. The full tags exist mainly so arbitrary
installs with native builds work out of the box.

## Tag anatomy
`python:3.12-slim-bookworm` = version + variant + Debian suite codename. A codename-less
`-slim` tag follows the repository's current default Debian release and **changes base OS when
a new Debian release lands** (at the time of the check `python:3.12-slim` pointed at the
trixie variant); Docker Hub advises naming the suite explicitly to minimise breakage. Check the
tag list on Docker Hub for which aliases a short tag such as `node:22-slim` maps to today.

## Pattern: build in full, run in slim
```dockerfile
FROM python:3.12-bookworm AS build
WORKDIR /app
RUN python -m venv /venv && /venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
 && rm -rf /var/lib/apt/lists/*
COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH
COPY . /app
WORKDIR /app
USER 1000
CMD ["python", "app.py"]
```
Only the **runtime** libraries (`libpq5`, not `libpq-dev`) go into the slim stage. Find them
with `ldd` on the compiled extension (`find /venv -name '*.so' | xargs ldd | grep 'not found'`).

## Slim vs alternatives
| Need | Pick |
|---|---|
| shell, apt, glibc, debuggable, small | `-slim` |
| smallest glibc, no shell, nonroot, low CVE | distroless or Chainguard |
| smallest overall, static binary, you accept musl | alpine |
| compiling native deps | full tag in a build stage only |

Slim images still carry Debian's own package set and its CVE findings; scan the candidate
images before choosing on security grounds.

## Gotchas
- `apt-get install` in slim needs `apt-get update` first and `--no-install-recommends`;
  recommends pull in exactly the bloat slim removed.
- Slim has only minimal packages: do not assume `curl` or `git` exist. A `HEALTHCHECK CMD curl`
  fails if it is absent; use the interpreter (`python -c` / `node -e`) for the request, or
  install `curl` explicitly.
- Installing from git URLs or compiling native modules belongs in a full build stage.

## Verify
`docker image ls` shows slim at a fraction of the full tag; the app's native extensions import
without `ImportError: libxxx.so: cannot open shared object file`.

## Checked
2026-11-01. Confirmed on the Docker Hub official-image pages for debian, python and node: slim
tags exist; debian slim removes man pages and documentation and is described as experimental;
python slim drops the default tag's common packages and cannot compile extensions, so pip
installs depend on wheels; suite names such as bookworm and trixie identify the Debian release
and should be named explicitly; the codename-less python slim tag currently points at trixie.
Removed: the compressed-size figures, the dpkg exclude file path, the locales claim, the ruby
tag, the claim that slim lacks specific tools and header files by name, the CVE count, the
package-count check, and trivy.
Method: documentation only; no commands were run.
