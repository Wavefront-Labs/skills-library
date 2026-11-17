---
id: computing-software.cloud-infrastructure-engineering.docker.dockerfile-location-flag-and-stdin-builds
name: dockerfile-location-flag-and-stdin-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, build-context, dockerfile-flag, dockerfile-stdin, dockerfile-inline, docker-build, heredoc]
level: practitioner
status: docs-checked
description: "Point docker build at a Dockerfile outside the context with -f, pipe a Dockerfile on stdin with or without a context, and use Compose dockerfile_inline and Bake equivalents."
sources: ["https://docs.docker.com/build/concepts/context/", "https://docs.docker.com/reference/cli/docker/buildx/build/#file", "https://docs.docker.com/reference/compose-file/build/#dockerfile_inline", "https://docs.docker.com/build/bake/reference/#targetdockerfile-inline"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dockerfile location and stdin builds

The Dockerfile and the context are independent inputs. Choosing them separately keeps contexts
small and Dockerfiles organised.

## -f with a separate context
```bash
docker build -f docker/api.Dockerfile -t api ./services/api
```
- `-f [PATH|URL|-]` sets the Dockerfile; if unspecified, a file named `Dockerfile` at the root of
  the build context is used. The accepted forms are a local path, a remote URL or `-` for stdin.
- A Dockerfile-specific ignore file (`<name>.Dockerfile.dockerignore` style, next to the
  Dockerfile) takes precedence over the context's `.dockerignore`.

## Dockerfile from stdin
```bash
# Dockerfile on stdin, local directory as context
docker build -f- -t probe . <<'EOF'
FROM busybox
COPY . /src
EOF

# No filesystem context: a text file (here stdin) is treated as the Dockerfile
docker build -t myimage:latest - <<EOF
FROM busybox
RUN echo "hello world"
EOF

# Remote context, Dockerfile on stdin
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```
`docker build - < context.tar.gz` is different: stdin is a tarball used as the filesystem
context, and the Dockerfile is resolved from inside it (`--file` names it relative to the tarball
root). A remote Dockerfile can also be passed as the context URL or with `-f <URL>`.

## Compose and Bake
```yaml
services:
  probe:
    build:
      context: .
      dockerfile: docker/probe.Dockerfile        # relative paths resolve from the context
  tiny:
    build:
      dockerfile_inline: |
        FROM busybox
        RUN echo hello
```
```hcl
target "tiny" {
  dockerfile-inline = "FROM busybox\nRUN echo hello"
}
```
Compose rejects a service that sets both `dockerfile` and `dockerfile_inline`.

## Gotchas
- With no filesystem context, `COPY` of local files fails with a "not found" error; the build has
  nothing to copy from. `COPY --from` still works.
- Compose resolves `dockerfile` relative to `context`.
- Shell here-documents expand `$VAR` unless the delimiter is quoted (`<<'EOF'`).

## Verify
`docker build -f docker/api.Dockerfile --progress=plain ./services/api` shows the
"load build definition" and "transferring context" steps.

## Checked

Checked 2026-10-23 against docker/docs "Build context" (stdin, tarballs, empty context, remote context with Dockerfile from stdin), the `docker buildx build --file` reference, the Compose `build.dockerfile` and `dockerfile_inline` reference and the Bake `dockerfile-inline` reference.
Confirmed: `-f [PATH|URL|-]` forms and default, stdin Dockerfile with local, remote and empty context, tarball context, COPY failing without a context, Compose and Bake inline Dockerfiles. Removed unconfirmed claims: the legacy builder inside-context requirement, a Dockerfile outside the context, `apk add` and `jq` examples, and the Compose-versus-CLI resolution comparison.

Method: documentation only; no commands were run.
