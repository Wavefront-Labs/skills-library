---
id: computing-software.cloud-infrastructure-engineering.docker.pulling-by-digest-pull-policy-and-platform
name: pulling-by-digest-pull-policy-and-platform
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, pull, digest, pull-by-digest, digest-reference, pull-policy, pull-platform, multi-arch]
level: practitioner
description: "Pull and run images by @sha256 digest, control when Docker and Compose re-pull with --pull and pull_policy, and fetch a specific architecture with --platform."
sources: ["https://docs.docker.com/reference/cli/docker/image/pull/", "https://docs.docker.com/reference/cli/docker/container/run/#pull", "https://docs.docker.com/reference/compose-file/services/#pull_policy", "https://docs.docker.com/docker-hub/usage/pulls/", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_digest.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pull by digest, pull policy and --platform

## Digests
```sh
docker pull nginx@sha256:<index-digest>
docker run --rm nginx:1.27@sha256:<index-digest>
docker images --digests nginx
docker inspect -f '{{json .RepoDigests}}' nginx:1.27
```
- Use the **index** digest (multi-arch) so each host resolves its own platform; a
  platform-specific manifest digest pins one architecture.
- `RepoDigests` lists registry digests for images pulled from or pushed to a registry.
- Resolve the digest in CI with `crane digest <image>` or
  `docker buildx imagetools inspect <image>` and deploy by digest.

## Pull policy
`docker run --pull` and `docker create --pull` accept `always`, `missing` (the default) and
`never`: `missing` pulls only if the image is not present locally, `always` pulls before
running, `never` does not pull. `docker build --pull` always attempts to pull a newer version of
the `FROM` image.

Compose `pull_policy:` values (Compose file reference): `always`, `never`, `missing`
(default unless you also use the build specification; `if_not_present` is an alias; the
`latest` tag is always pulled even with `missing`), `build`, `daily`, `weekly` and
`every_<duration>`.

## Platform
```sh
docker pull --platform linux/arm64 nginx:1.27
docker run --platform linux/amd64 app:1
docker image inspect -f '{{.Os}}/{{.Architecture}}{{if .Variant}}/{{.Variant}}{{end}}' nginx:1.27
```
`--platform` is "Set platform if server is multi-platform capable". Compose: `platform:
linux/amd64` per service uses the `os[/arch[/variant]]` syntax. The Docker CLI also reads the
`DOCKER_DEFAULT_PLATFORM` environment variable (see the docker/cli source for where it applies).
Which platforms one tag can hold locally depends on the image store: the containerd image
store supports multi-platform images; with classic storage drivers see
`save-and-load-specific-platforms`.

## Gotchas
- Running an image for a platform that differs from the host's may require emulation, which is
  slower.
- Docker Hub counts pulls toward rate limits, and a pull of a multi-arch image counts as one
  pull for each different architecture (Docker Hub usage docs); a mirror or pull-through
  cache reduces pulls.
- With `docker run` and the default `missing` policy, a local `latest` is never refreshed;
  use `--pull always` when you want the newest image.

## Verify
`docker inspect -f '{{index .RepoDigests 0}}' <image>` equals the digest in your manifest.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed: docker run/create --pull values and default, docker build --pull, --platform option text, docker images --digests, Compose pull_policy values and behaviour and platform syntax, Docker Hub usage docs (multi-arch pulls count per architecture), crane digest usage. Removed the unconfirmed claims that HEAD requests are free for pulls (the docs say HEAD only avoids counting for limit-check requests), the warning text, the classic-store one-platform-per-tag statement and the imagetools Manifest.Digest format.

Method: documentation only; no commands were run.
