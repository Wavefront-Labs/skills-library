---
id: computing-software.cloud-infrastructure-engineering.docker.pinning-os-and-language-packages-in-images
name: pinning-os-and-language-packages-in-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, reproducible-builds, pinned-packages, apt-pinning, pip-hashes, snapshot-debian, lockfiles, dockerfile]
level: advanced
status: docs-checked
description: "Pin apt/apk package versions or snapshot mirrors and install language deps from hash-locked lockfiles so rebuilds of a Dockerfile give the same software."
sources: ["https://docs.docker.com/build/building/best-practices/#apt-get", "https://snapshot.debian.org/", "https://pip.pypa.io/en/stable/topics/secure-installs/", "https://github.com/reproducible-containers/repro-sources-list.sh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pinning OS and language packages in images

## apt: version pins
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl=7.88.1-10+deb12u8 ca-certificates=20230311 \
 && rm -rf /var/lib/apt/lists/*
```
Exact apt version pins are fragile: when the mirror no longer carries that version the build fails. Docker's best practices page recommends pinning base image versions (tag plus digest) rather than relying on mutable tags.

## apt: snapshot mirror (stable over time)
Debian 12 and later keep their sources in `/etc/apt/sources.list.d/debian.sources`; the snapshot archive base is `http://snapshot.debian.org/archive/`.
```dockerfile
ARG SNAPSHOT=20261001T000000Z
RUN sed -i "s|http://deb.debian.org/debian|http://snapshot.debian.org/archive/debian/${SNAPSHOT}|g; \
            s|http://deb.debian.org/debian-security|http://snapshot.debian.org/archive/debian-security/${SNAPSHOT}|g" \
      /etc/apt/sources.list.d/debian.sources \
 && apt-get update \
 && apt-get install -y --no-install-recommends curl
```
`repro-sources-list.sh` from reproducible-containers automates this from `SOURCE_DATE_EPOCH` (default: timestamp of the sources file). If apt rejects an old snapshot's Release file as expired, check the apt documentation for the validity setting.
Bump `SNAPSHOT` deliberately to take security fixes - pinning means you now own patch cadence.

## apk
Pin the Alpine minor tag plus digest (`FROM alpine:3.21@sha256:<digest>`), as the Docker best practices page shows, and accept package drift, or vendor packages. Digest pins opt you out of automated security fixes; Dependabot with `package-ecosystem: "docker"` can raise update PRs.

## pip with hashes
```sh
pip-compile --generate-hashes -o requirements.txt requirements.in   # pip-tools
```
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes --no-deps -r requirements.txt
```
`--require-hashes` forces hash-checking mode: pip's secure-installs page says it protects against remote tampering and network issues, using local `--hash` entries per requirement. `--no-deps` stops pip fetching unchecked dependencies.

## Verify
Rebuild with `--no-cache` later and compare the installed package lists (`dpkg-query -W` output) of both images.

## Checked
2026-10-28. Confirmed against Docker build best practices (pinning base images, digests, Dependabot), the repro-sources-list.sh README (snapshot URL, debian.sources, SOURCE_DATE_EPOCH) and pip's secure-installs page (`--require-hashes`, `--no-deps`). Removed unconfirmed claims: Debian/Alpine mirror retention behaviour, `Check-Valid-Until` flag, example version strings, uv/Poetry/npm/Go/Maven pinning notes, Renovate.
Method: documentation only; no commands were run.
