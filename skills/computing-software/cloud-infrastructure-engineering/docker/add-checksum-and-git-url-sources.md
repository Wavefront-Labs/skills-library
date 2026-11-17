---
id: computing-software.cloud-infrastructure-engineering.docker.add-checksum-and-git-url-sources
name: add-checksum-and-git-url-sources
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, add, add-checksum, add-git-url, keep-git-dir, remote-url, supply-chain]
level: practitioner
status: docs-checked
description: "Fetch remote files and Git repos in a Dockerfile with ADD: --checksum verification, git refs and subdirs, --keep-git-dir, private repos over SSH, and cache behaviour."
sources: ["https://docs.docker.com/reference/dockerfile/#add", "https://docs.docker.com/reference/dockerfile/#add---checksum", "https://docs.docker.com/reference/dockerfile/#add---keep-git-dir", "https://docs.docker.com/build/building/secrets/#git-authentication-for-remote-contexts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADD --checksum and Git URL sources

`ADD` can fetch remote files and Git repositories without a `RUN`. Use it when you want
BuildKit to do the download and verify it.

## Remote file with checksum
```dockerfile
# syntax=docker/dockerfile:1
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/linux-0.01.tar.gz /src/
```
- For HTTP sources the checksum is the SHA-256 content digest, formatted `sha256:<hash>`;
  SHA-256 is the only supported hash algorithm.
- A remote tar archive is **not** unpacked by default (local tar files are). Use
  `ADD --unpack=true <url> <dest>` to download and unpack it.
- A remote file gets permissions 600 (override with `--chmod`); if the response has a
  `Last-Modified` header it sets the file's `mtime`, which is not part of the cache decision.
- `ADD` does not support authentication for URLs natively; use the `HTTP_AUTH_TOKEN_<host>` or
  `HTTP_AUTH_HEADER_<host>` build secrets, or fetch with a tool in a `RUN`.

## Git repository
```dockerfile
ADD https://github.com/moby/buildkit.git#v0.14.1 /src/buildkit          # tag
ADD https://github.com/org/repo.git#main:docs /src/docs                 # branch + subdir
ADD --keep-git-dir=true https://github.com/org/repo.git#v1.2.0 /src     # keep .git for git describe
```
- URL fragments select a branch, tag, commit or subdirectory (`#<ref>:<subdir>`). Pin a tag or
  commit SHA; a branch moves.
- The `.git` directory is excluded by default; `--keep-git-dir=true` preserves it.
- For Git sources `--checksum` is the commit SHA, either the full SHA or a prefix of one or more
  characters, for example `ADD --checksum=be1f38e https://github.com/moby/buildkit.git#v0.26.2 /`.
- Files from a Git repository get permissions 644 (755 if the executable bit is set in the
  repository); directories get 755.

## Private repositories
```dockerfile
ADD git@github.com:org/private.git#v2.0.0 /src
```
```bash
docker buildx build --ssh default .        # forwards your ssh-agent to the git fetch
```
For HTTPS tokens BuildKit has the predefined build secrets `GIT_AUTH_TOKEN` (Basic
authentication with the fixed user `x-access-token`) and `GIT_AUTH_HEADER` (a raw authorization
header value); the Docker docs list fetching private Git repositories with `ADD` as a use.

## ADD vs COPY vs RUN curl
- Local files: use `COPY`; `ADD` unpacks local tar archives by default (`--unpack=false` stops it).
- Remote artifact you want verified: `ADD --checksum`.
- Downloads needing post-processing in one layer: a tool in `RUN`, with a secret mount for
  credentials.

## Verify
```bash
docker run --rm <image> ls -la /src            # .git present only with --keep-git-dir
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (`ADD`, `ADD --checksum`, `ADD --keep-git-dir`, `ADD --unpack`; moby/buildkit main branch) and the Docker docs "Build secrets" page.

- `--checksum` for HTTP (`sha256:<hash>` only) and Git (commit SHA or prefix) sources; remote archives not unpacked by default; mode 600 and `Last-Modified` handling; Git fragments and file modes; `.git` excluded unless `--keep-git-dir=true`.
- `--ssh default` for SSH Git sources; `GIT_AUTH_TOKEN` / `GIT_AUTH_HEADER` for private Git repositories including `ADD`, and `HTTP_AUTH_TOKEN_<host>` / `HTTP_AUTH_HEADER_<host>` for `ADD` URLs.
- Removed the `curl | sha256sum` hint, the claim that BuildKit re-checks URLs every build, the "only instruction that fetches" claim and the grep-based verification.

Method: documentation only; no commands were run.
