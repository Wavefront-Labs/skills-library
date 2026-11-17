---
id: computing-software.cloud-infrastructure-engineering.docker.git-url-tarball-and-stdin-build-contexts
name: git-url-tarball-and-stdin-build-contexts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, build-context, git-build-context, remote-context, stdin-context, tarball-context, build-from-url, subdirectory-context]
level: practitioner
description: "Build directly from a Git URL (with ref and subdirectory), a remote tarball, or a Dockerfile on stdin with no context, and handle auth, submodules and .dockerignore in each case."
sources: ["https://docs.docker.com/build/concepts/context/", "https://docs.docker.com/build/building/secrets/#git-authentication-for-remote-contexts", "https://docs.docker.com/reference/dockerfile/#buildkit-built-in-build-args"]
status: docs-checked
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Git, tarball and stdin build contexts

**Goal:** build an image from a repository or archive without cloning it yourself, or build a
one-off image with no context at all.

## Git URL context
```sh
docker build https://github.com/user/myrepo.git                        # default branch, root
docker build https://github.com/user/myrepo.git#container:docker       # #ref:dir (branch, tag or commit; subdirectory)
docker build https://github.com/user/myrepo.git#:docker                # default branch, subdirectory
docker build 'https://github.com/user/myrepo.git?branch=container&subdir=docker'   # URL queries (recommended)
docker build 'https://github.com/user/myrepo.git?tag=v1.0&checksum=<sha>'          # verify the resolved commit
```
The builder performs a shallow clone (HEAD commit only) on the **builder** host and clones
submodules recursively. In `#ref:dir`, `ref` is a branch, tag or commit hash and `dir` a
subdirectory. A commit hash in a fragment must be the full 40-character SHA-1; with URL queries
a short hash works for `checksum` (alias `commit`) but `ref` needs the full hash. URL queries
are `branch`, `tag`, `ref` (for example `pull/42/head`), `subdir`, `checksum`.
If the checksum does not match, the build fails.

BuildKit does not keep `.git` in Git contexts by default; set
`--build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1` to keep it (for builds that run `git rev-parse`).

Auth for private repositories:
- SSH: buildx detects SSH or `git@` addresses and uses `$SSH_AUTH_SOCK`;
  `docker buildx build --ssh default git@github.com:user/private.git`.
- HTTP token: BuildKit has two pre-defined secrets, `GIT_AUTH_TOKEN` (Basic auth with the fixed
  username `x-access-token`) and `GIT_AUTH_HEADER` (a raw authorization header value, for any
  Git provider):
  `GIT_AUTH_TOKEN=<token> docker buildx build --secret id=GIT_AUTH_TOKEN https://github.com/user/private.git`
  GitLab CI job tokens are not compatible with `GIT_AUTH_TOKEN`; use a personal access token.
- Never use `--build-arg` for secrets.

Pin to a commit when you need reproducibility: a branch ref moves.

## Tarball context
```sh
docker build http://server/context.tar.gz          # remote tarball, fetched by the builder host
docker build - < context.tar.gz                    # tarball on stdin
```
Tarballs must be standard tar archives, compressed with `xz`, `bzip2`, `gzip` or uncompressed.
The Dockerfile is resolved from the tarball; `--file` names it relative to the tarball root. The
download for a remote tarball happens where the BuildKit daemon runs, which with a remote Docker
context or builder is not necessarily your machine.

## Stdin Dockerfile, no context
```sh
docker build -t myimage:latest - <<EOF
FROM busybox
RUN echo "hello world"
EOF
```
A text file as the context (stdin or a remote text file URL) is interpreted as a Dockerfile and
the build has no filesystem context, so `COPY` of local files fails. `COPY --from=<image>` and
`ADD <url>` do not need a local context.

Stdin Dockerfile with a local or remote context:
```sh
docker build -f- . <<'EOF'
FROM busybox
COPY . /src
EOF
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

## Combining with named contexts
`--build-context name=<source>` adds an additional named context usable as `COPY --from=name`,
keeping the main context local.

## Gotchas
- The builder, not the client, needs network access to the Git host or tarball URL.
- Shell here-documents expand `$VAR` unless the delimiter is quoted.

## Verify
`docker build --progress=plain https://github.com/user/myrepo.git#<sha>` shows
`[internal] load git source` for the repository.

## Checked

Checked 2026-10-23 against docker/docs "Build context" (Git repositories, URL fragments and queries, keep `.git`, private repositories, remote tarballs, empty context, remote context with stdin Dockerfile), "Build secrets" (Git authentication for remote contexts) and the Dockerfile reference built-in build args.
Confirmed: shallow clone and recursive submodules, `#ref:dir` and URL query forms, 40-character hash rule, `checksum`, `BUILDKIT_CONTEXT_KEEP_GIT_DIR`, SSH auto-detection, `GIT_AUTH_TOKEN` and `GIT_AUTH_HEADER` semantics, tarball formats and builder-side download, no-context behaviour. Removed unconfirmed claims: `.dockerignore` application inside the cloned subdirectory, Git LFS handling, URL-prefix detection rules, `-f` relative to the subdirectory, identical layer digests, and the `GITHUB_TOKEN` env mapping.

Method: documentation only; no commands were run.
