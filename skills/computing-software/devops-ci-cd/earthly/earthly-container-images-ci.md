---
id: computing-software.devops-ci-cd.earthly.earthly-container-images-ci
name: earthly-container-images-ci
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthly-earthly-image, buildkitd, no-buildkit, buildkit-host, privileged, docker-image, ci]
level: practitioner
status: docs-checked
description: "Run earthly in containerised CI with the earthly/earthly image (embedded BuildKit, Docker socket, satellites) or the standalone earthly/buildkitd image and its env vars."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/use-earthly-ci-image.md
  - https://github.com/earthly/earthly/blob/main/docs/docker-images/all-in-one.md
  - https://github.com/earthly/earthly/blob/main/docs/docker-images/buildkit-standalone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# earthly/earthly and earthly/buildkitd images

Goal: use Earthly inside a container for CI. Pin the image version in CI (the earthly/earthly examples use `v0.8.13`; the buildkitd examples use `v0.7.19`).

## earthly/earthly
Its entrypoint (`/usr/bin/earthly-entrypoint.sh`) starts BuildKit, then runs `earthly` with your arguments. It needs either `--privileged` (embedded BuildKit) or `NO_BUILDKIT=1`. Source goes in `/workspace` (default working dir).

Embedded BuildKit:
```bash
docker run --privileged -t -v $(pwd):/workspace -v earthly-tmp:/tmp/earthly:rw earthly/earthly:v0.8.13 +for-linux
```
Host Docker socket (BuildKit started in the host Docker):
```bash
docker run -t -v $(pwd):/workspace -v /var/run/docker.sock:/var/run/docker.sock -e NO_BUILDKIT=1 earthly/earthly:v0.8.13 +for-linux
```
Satellite with no local code (remote target ref):
```bash
docker run -t -e NO_BUILDKIT=1 -e EARTHLY_TOKEN=<my-token> earthly/earthly:v0.8.13 --ci --org <my-org> --sat <my-sat> github.com/earthly/earthly+for-linux
```
Non-build commands: `docker run -t -e NO_BUILDKIT=1 -e EARTHLY_TOKEN=<my-token> earthly/earthly:v0.8.13 secret get foo`. Use `-w /my-dir` for another directory. Using the `earthly` binary itself as entrypoint does not start BuildKit in the container.

Remote daemon: set `BUILDKIT_HOST` and no BuildKit is started.

## Must-haves
- Mount a Docker volume at `/tmp/earthly`; without it BuildKit can use excessive disk, run very slowly or fail, in some environments with `rm: can't remove '/var/earthly/dind/...': Resource busy`.
- The image has a Docker CLI but no daemon; supply one via `DOCKER_HOST` or the socket mount.
- `-t` (or `FORCE_COLOR`) gives colored output.

Env vars (earthly/earthly): `GLOBAL_CONFIG`, `GIT_CONFIG`, `NO_BUILDKIT`, `DOCKER_HOST`, `BUILDKIT_HOST`, `EARTHLY_ADDITIONAL_BUILDKIT_CONFIG`, `BUILDKIT_TCP_TRANSPORT_ENABLED` (must be `true` for an external buildkitd), `BUILDKIT_TLS_ENABLED`, `CNI_MTU`, `EARTHLY_RESET_TMP_DIR`, `NETWORK_MODE` (default `cni`), `CACHE_SIZE_MB` (default `0`, adaptive), `GIT_URL_INSTEAD_OF`, `IP_TABLES`.

## earthly/buildkitd (shared BuildKit)
Only tested with its matching earthly version. Always `--privileged`.
```bash
docker run --privileged -t -v earthly-tmp:/tmp/earthly:rw -e BUILDKIT_TCP_TRANSPORT_ENABLED=true -p 8372:8372 earthly/buildkitd:v0.7.19
```
Point clients with `EARTHLY_BUILDKIT_HOST=tcp://fast-builder:8372` or `docker-container://<container-name>` locally. Hosts `127.0.0.1`, `::1/128` or `localhost` count as local, so Earthly manages the container itself; use another hostname. Here `CACHE_SIZE_MB` `0` means unbounded.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: ci-integration/use-earthly-ci-image.md, docker-images/all-in-one.md, docker-images/buildkit-standalone.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: version pin note now says earthly/earthly examples use v0.8.13 and the buildkitd examples use v0.7.19.

Method: documentation only; no commands were run.
