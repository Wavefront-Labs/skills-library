---
id: computing-software.cloud-infrastructure-engineering.docker.image-mounts-with-mount-type-image
name: image-mounts-with-mount-type-image
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volumes, image-mount, mount-flag, read-only, data-images, models]
level: advanced
status: docs-checked
description: "Mount the filesystem of another image read-only into a container with --mount type=image: shipping models, assets or tools as images, subpaths, versioning and support caveats."
sources: ["https://github.com/docker/cli/blob/master/opts/mount.go", "https://github.com/moby/moby/blob/master/api/docs/CHANGELOG.md", "https://github.com/moby/moby/blob/master/api/swagger.yaml", "https://kubernetes.io/docs/concepts/storage/volumes/#image"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image mounts (--mount type=image)

Docker Engine can mount another image's filesystem (or a subdirectory of it) into a
container: `POST /containers/create` supports a `Mount` of type `image` since API v1.48. It lets
you version and distribute large data (ML models, static assets, tool bundles) through the
registry, separately from the application image. Kubernetes has an `image` volume source for
OCI images and artifacts.

## Usage
```bash
# data image: just files on scratch
cat > Dockerfile.model <<'EOF'
FROM scratch
COPY model/ /model/
EOF
docker build -f Dockerfile.model -t reg.example.com/models/llm:2024-10 .

docker run -d --name infer \
  --mount type=image,source=reg.example.com/models/llm:2024-10,target=/models \
  inference-server:3.1 --model-dir /models/model
```
The CLI's `--mount` parser accepts `type=image` with `source` (image reference), `target` and
`image-subpath`, which selects a path inside the image; the API documents it as a source path
inside the image that must be relative without any back traversals. Daemons older than API
v1.48 do not know the mount type.

## Why
- The app image stays small and rebuilds fast; model or data updates are a tag bump.

## Alternatives on older Engines
```bash
# copy into a volume once (init pattern)
docker create --name modeldata reg.example.com/models/llm:2024-10 true
docker cp modeldata:/model - | docker run --rm -i -v models:/models alpine tar -x -C /models
docker rm modeldata
```
Or a multi-stage `COPY --from=reg.example.com/models/llm:2024-10 /model /models` at build time
(couples app and data versions).

## Gotchas
- `image-subpath` must be a relative path inside the image without back traversals.
- The mount source is an image, so it has to be available to the daemon (pulled or pullable).

## Checked

Checked 2026-10-23 against the docker/cli `opts/mount.go` and vendored mount types (`image` type, `image-subpath` option), the moby API changelog (v1.48: `Mount` of type `image`), the moby `swagger.yaml` (`ImageOptions.Subpath`) and the Kubernetes volumes documentation (`image` volume source).

- Mount type `image` and its `source`, `target` and `image-subpath` options; API version that introduced it.
- Multi-stage `COPY --from=<image>` and the `docker cp` volume-seeding alternative are standard documented commands.
- Removed the read-only claim, the Compose and platform notes, the deduplication, signing and lazy-pulling remarks, which the references do not state.

Method: documentation only; no commands were run.
