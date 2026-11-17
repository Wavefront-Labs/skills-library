---
id: computing-software.cloud-infrastructure-engineering.docker.reading-image-config-with-inspect
name: reading-image-config-with-inspect
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-inspect, image-config-inspect, inspect-format, entrypoint, exposed-ports, image-metadata]
level: practitioner
status: docs-checked
description: "Read an image's runtime contract before running it: Entrypoint, Cmd, Env, User, WorkingDir, ExposedPorts, Volumes, Healthcheck, StopSignal, locally or straight from a registry."
sources: ["https://docs.docker.com/reference/cli/docker/image/inspect/", "https://github.com/opencontainers/image-spec/blob/main/config.md", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_config.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-inspect.1.md", "https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading image config with inspect

The image config is the contract between the image author and whoever runs it. Read it
before writing a Compose service or Kubernetes manifest for a third-party image.

## Local image
```bash
docker image inspect nginx:1.27 --format '{{json .Config}}'
```
One-liners:
```bash
docker image inspect -f '{{.Config.User}}' img                    # empty = root
docker image inspect -f '{{json .Config.Entrypoint}} {{json .Config.Cmd}}' img
docker image inspect -f '{{range $p, $_ := .Config.ExposedPorts}}{{$p}} {{end}}' img
docker image inspect -f '{{range .Config.Env}}{{println .}}{{end}}' img
docker image inspect -f '{{.Os}}/{{.Architecture}}{{if .Variant}}/{{.Variant}}{{end}}' img
```

## Remote image without pulling
```bash
crane config nginx:1.27
skopeo inspect --config docker://docker.io/library/nginx:1.27
docker buildx imagetools inspect nginx:1.27 --format '{{json .Image}}'      # .Image is the image config
```

## What each field means at runtime
| Field | Runtime effect | Override |
|---|---|---|
| `Entrypoint` | Executable always run | `--entrypoint` / `entrypoint:` |
| `Cmd` | Default args to Entrypoint (or the command if no Entrypoint) | trailing args / `command:` |
| `User` | UID[:GID] or name | `--user` / `user:` |
| `WorkingDir` | cwd | `-w` / `working_dir:` |
| `Env` | Defaults | `-e` / `environment:` |
| `ExposedPorts` | `EXPOSE` does not publish the port; `-P` publishes all exposed ports | `-p` |
| `Volumes` | From the `VOLUME` instruction: mount points for volumes | `-v name:/path` |
| `Healthcheck` | Health status | `--health-*`, `--no-healthcheck` |
| `StopSignal` | Signal sent by `docker stop` | `--stop-signal` |

## Gotchas
- Check `Volumes` before running a third-party image and mount a named volume over every
  listed path you care about.
- Multi-arch tags: local inspect shows the platform you pulled; remote tools show the index
  or need a platform.
- `docker inspect <name>` can match a container as well as an image; use `docker image inspect`.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), docker/cli system events reference, Compose and Scout CLI reference data, dive, uv and distroless READMEs, action repositories at their latest releases. Confirmed: docker image inspect --format, Config fields used in the templates, docker buildx imagetools inspect --format with .Name/.Manifest/.Image, skopeo inspect --config, crane config usage, EXPOSE and -P semantics, docker run option names (--entrypoint, --user, --workdir, --stop-signal, --no-healthcheck, --health-cmd, -P). Removed the jq filters, the anonymous-volume behaviour claim and the multi-platform key structure of imagetools output.

Method: documentation only; no commands were run.
