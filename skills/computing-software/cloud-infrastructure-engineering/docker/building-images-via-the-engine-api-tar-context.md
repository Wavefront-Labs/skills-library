---
id: computing-software.cloud-infrastructure-engineering.docker.building-images-via-the-engine-api-tar-context
name: building-images-via-the-engine-api-tar-context
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-engine-api, api-build, build-endpoint, tar-context, dockerignore, x-registry-config, jsonmessage, docker-sdk]
level: advanced
status: docs-checked
description: "Build images through POST /build: packing a tar context that honours .dockerignore, query params, registry auth header, parsing the JSON stream for errors, and when to use BuildKit instead."
sources: ["https://docs.docker.com/reference/api/engine/version/v1.56/#tag/Image/operation/ImageBuild", "https://github.com/moby/moby/blob/master/client/image_build.go", "https://github.com/docker/docker-py/blob/main/docker/api/build.py", "https://docs.docker.com/build/concepts/context/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building images via the Engine API (tar context)

## The request
`POST /build` with the **build context as a tar archive** in the body (identity, gzip, bzip2
or xz compressed), `Content-Type: application/x-tar`.
```bash
tar -C ./app -cz . | curl -s --unix-socket /var/run/docker.sock \
  -H 'Content-Type: application/x-tar' --data-binary @- \
  'http://localhost/v1.47/build?t=app:api&dockerfile=Dockerfile&pull=1&rm=1&forcerm=1&buildargs=%7B%22VERSION%22%3A%221.2.3%22%7D'
```
Query parameters (API v1.56 reference): `t` (repeatable name:tag), `dockerfile` (path inside
the tar, default `Dockerfile`), `target`, `buildargs` (JSON map), `labels` (JSON map),
`nocache`, `pull`, `rm` (default true), `forcerm`, `platform`, `networkmode`, `cachefrom`
(JSON array of images), `remote` (git URL or HTTP(S) context URI used instead of a body),
`version` (builder backend).

## Apply .dockerignore yourself
The API reference describes the body only as a tar archive and says nothing about ignore
files. When you build the tar yourself, apply the ignore rules or you ship `.git`,
`node_modules` and secrets into the context (and into `COPY . .`). docker-py reads
`.dockerignore` for you when you pass `path=`. Keep the file named by `dockerfile` in the tar:
the daemon reads it from there.

```go
import ("github.com/moby/moby/client")

cli, err := client.New(client.FromEnv)
res, err := cli.ImageBuild(ctx, ctxTar, client.ImageBuildOptions{
    Tags: []string{"app:api"}, Dockerfile: "Dockerfile", Remove: true, PullParent: true,
    BuildArgs: map[string]*string{"VERSION": ptr("1.2.3")},
})
defer res.Body.Close()
// res.Body is the JSON message stream; decode it and treat any error message as failure
```
`ctxTar` is an `io.Reader` over your tar (built with a tar library after filtering paths with
your ignore rules, for example with `github.com/moby/patternmatcher/ignorefile`).
`ImageBuildOptions.BuildArgs` is a `map[string]*string` so that an empty value can be told
apart from an unset one.

## Reading the response
The body is a stream of JSON messages; the spec's message objects carry `stream`, `status`
and an `error`/`errorDetail` field. Do not rely on the HTTP status alone: decode the stream and
treat any `error` message as a failed build (in docker-py use `decode=True` on the low-level
`client.api.build(...)` stream and raise on `"error"`).

## Registry auth for private base images
Header `X-Registry-Config`: base64-encoded JSON object mapping registry to credentials:
```json
{"ghcr.io": {"username": "bot", "password": "<TOKEN>"}}
```
The reference says only the registry domain (and port if not 443) is needed, except Docker
Hub, which must be keyed `https://index.docker.io/v1/`. In the Go client, set
`ImageBuildOptions.AuthConfigs` (a `map[string]registry.AuthConfig`); the client builds the
header (URL-safe base64). docker-py looks up credentials from the Docker config itself.

## Python
```python
import docker
client = docker.from_env()
image, logs = client.images.build(path="./app", tag="app:api", rm=True, pull=True,
                                  buildargs={"VERSION": "1.2.3"})   # reads .dockerignore from path
# custom context: client.images.build(fileobj=tar_bytes, custom_context=True, encoding="gzip", tag=...)
```
`images.build` raises `docker.errors.BuildError` on failure.

## Classic builder vs BuildKit
The `version` query parameter selects the builder backend: `1` is the first-generation
classic builder, marked deprecated in the reference and the default; `2` is BuildKit. For
BuildKit features (`RUN --mount`, `--secret`, multi-platform, cache export) run
`docker buildx build` as a subprocess instead of the plain `/build` call.

## Verify
```bash
docker image inspect app:api -f '{{.Id}} {{.Created}}'
tar -tzf ctx.tgz | grep -E '^(\./)?(\.git|node_modules)/' && echo "ignore rules not applied"
```

## Checked

2026-10-26 against Docker Engine API v1.56 reference (docker/docs main, 2026-10-23), moby/moby client source and API changelog, docker-py source. Confirmed: `/build` query parameters and defaults, tar content types, `X-Registry-Config` format and Docker Hub key, `version` 1 (classic, deprecated, default) versus 2 (BuildKit), Go client API (`client.New`, `ImageBuild`, `ImageBuildOptions`, `AuthConfigs`), docker-py `.dockerignore` handling, custom_context/encoding and `BuildError`. Removed unconfirmed claims about CLI-side ignore filtering, the /session requirement, the Dockerfile re-add behaviour and the old Go helper packages.

Method: documentation only; no commands were run.
