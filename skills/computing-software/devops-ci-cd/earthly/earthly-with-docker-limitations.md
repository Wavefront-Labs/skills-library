---
id: computing-software.devops-ci-cd.earthly.earthly-with-docker-limitations
name: earthly-with-docker-limitations
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, with-docker, from-dockerfile, run-entrypoint, docker-sock, limitations, docker-network]
level: advanced
status: docs-checked
description: "Limits of WITH DOCKER in Earthly (one RUN, no docker.sock, no docker build, network quirks) and the alternatives RUN --entrypoint and FROM DOCKERFILE."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/docker-in-earthly.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WITH DOCKER limitations and alternatives

Goal: know what will not work inside `WITH DOCKER` in Earthly and what to use instead.

## Limitations stated in the docs

- Only one `RUN` is allowed inside the clause (one cache layer for the whole clause). Chain commands instead:
  ```Dockerfile
  WITH DOCKER
      RUN command1 && \
          command2 && \
          command3
  END
  ```
- Prefer a supported dind image such as `earthly/dind:alpine-3.19-docker-25.0.5-r0` or `earthly/dind:ubuntu-23.04-docker-25.0.2-1`. If you need another environment (e.g. `sbt test` or `go test` with a compose stack), put the test in an image, `--load` it, and run it as a container.
- Declare external images with `--pull` or `--compose`; otherwise `docker run` re-pulls every time because daemon cache is not preserved.
- `docker build` cannot build Dockerfiles; use `FROM DOCKERFILE`.
- The daemon state cannot be inspected from the host (no `docker logs` on the host). Use interactive mode and look from inside the build environment.
- Mounting `/var/run/docker.sock` to use the host daemon is not possible; it would make builds depend on host state.
- External networks (the Docker default) can fail with 100% packet loss; internal ones do not. Use `docker network create --internal ...` or `internal: true` in compose (issue 3495).

## Alternative to docker run

```Dockerfile
FROM hello-world
RUN --entrypoint
```

replaces `WITH DOCKER --pull hello-world` + `docker run hello-world`. Limits: no `-v` style volume mounts (use `COPY`), no multiple parallel containers.

## Alternative to docker build

`docker build` loses layer caching (only `--pull` persists) and its images cannot be exported except as a TAR. Emulate `docker build -t my-image:latest .` with:

```Dockerfile
FROM DOCKERFILE .
SAVE IMAGE my-image:latest
```

## Checked

2026-11-07. Read docs/guides/docker-in-earthly.md in full. Each limitation, the RUN --entrypoint and FROM DOCKERFILE alternatives, and the cited issue match. Nothing removed.
Method: documentation only; no commands were run.
