---
id: computing-software.cloud-infrastructure-engineering.docker.multi-stage-dockerfiles
name: multi-stage-dockerfiles
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, multi-stage-build, buildkit, docker-buildx, layer-caching, cache-mounts, secret-mounts, distroless, alpine, slim-images, chainguard, non-root, dockerignore, digest-pinning, sbom, provenance, podman, buildah, hadolint, trivy, cache-from, cache-to]
level: practitioner
status: docs-checked
description: "Write small, fast-building, secure Dockerfiles: multi-stage builds, cache-friendly layer order, BuildKit cache and secret mounts, distroless or slim runtime, non-root, digest pins."
sources: ["https://docs.docker.com/build/building/multi-stage/", "https://docs.docker.com/build/building/best-practices/", "https://docs.docker.com/build/cache/optimize/", "https://docs.docker.com/build/building/multi-platform/", "https://github.com/GoogleContainerTools/distroless"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-stage Dockerfiles: small, cacheable, non-root images

**Goal:** builds that reuse cache on every code-only change, runtime images that contain
only the app and its runtime, and nothing that runs as root or leaks build secrets.

## 1. The shape
```dockerfile
# syntax=docker/dockerfile:1
FROM node AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev

FROM deps AS build
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs22-debian13:nonroot AS runtime
WORKDIR /app
COPY --from=deps  /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
EXPOSE 8080
CMD ["dist/server.js"]
```
Only the final stage ships; build tools and dev dependencies stay behind. Build a specific
stage with `docker build --target build .` (useful for tests). Distroless runtime images ship
language-specific default entrypoints (for example `node`), so `CMD` carries just the script.

## 2. Order layers for the cache
- Copy dependency manifests first, install, then copy source, so a source edit reuses the
  dependency layer.
- A changed instruction or input invalidates that layer and every layer after it.
- Combine `apt-get update` and `apt-get install` in one `RUN` (and clean `/var/lib/apt/lists/*`
  there); a separate `update` layer can go stale.
- BuildKit builds only the stages the target depends on.

## 3. BuildKit mounts
- **Cache mounts** keep package caches across builds without adding to layers. Examples from
  the Docker docs: npm `target=/root/.npm`, pip `target=/root/.cache/pip`, Go
  `target=/go/pkg/mod` and `target=/root/.cache/go-build`, apt
  `target=/var/cache/apt,sharing=locked` (plus `/var/lib/apt`).
- **Secret mounts** for credentials, never `ARG`/`ENV`:
  `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci` with
  `docker build --secret id=npmrc,src=$HOME/.npmrc .`
- **Bind mounts** use files without copying them: `--mount=type=bind,source=go.sum,target=go.sum`.
- In CI use an external cache backend, for example
  `docker buildx build --cache-from type=registry,ref=registry.example.com/app:cache --cache-to type=registry,ref=registry.example.com/app:cache,mode=max .`
  (or `type=gha` on GitHub Actions); see the cache backend docs for what each exports.

## 4. Choose the runtime base
- **Distroless** (`gcr.io/distroless/static-debian13`, `base-debian13`, `java21-debian13`,
  `nodejs22-debian13`, `python3-debian13` and others): no package manager or shell; tags
  include `latest`, `nonroot`, `debug` and `debug-nonroot`. Use `debug` variants for
  troubleshooting. Entrypoint must be exec/vector form.
- A slim distribution image keeps a shell and package manager; pick the smallest base that
  runs your app.
- `FROM scratch` for fully static binaries; add CA certificates and `/etc/passwd` entries yourself.
- Check current tags in each project's README; distroless moved from `debian12` to `debian13`
  tags.

## 5. Security and reproducibility
- Run as non-root with `USER`: create the user and group in the Dockerfile (for example
  `groupadd -r` / `useradd --no-log-init -r`), and consider an explicit UID/GID since
  auto-assigned IDs are not deterministic across rebuilds. If the user has no primary group the
  process runs with the root group.
- Pin base images by digest (`FROM image:tag@sha256:...`) for reproducibility and let Dependabot
  or Renovate open update pull requests; pinning opts you out of automatic base-image fixes
  unless something updates the digest.
- Use `.dockerignore` to exclude files the build does not need (`.git`, `node_modules`, env
  files); it shrinks the context and keeps secrets out of `COPY . .`.
- Use `COPY --chown=<uid>:<gid>` so ownership is set on the copy itself.
- Exec-form `CMD`/`ENTRYPOINT` so the app is PID 1 and receives `SIGTERM`; `docker run --init`
  (Compose `init: true`) runs an init that forwards signals and reaps processes.
- Attach attestations with `docker buildx build --sbom=true --provenance=mode=max`.

## Gotchas
- `ARG` values appear in `docker history`; deleting a file in a later layer does not remove it
  from the earlier one.
- An `ARG` declared before `FROM` is out of scope inside a stage unless redeclared there.
- `COPY . .` before dependency install defeats caching on every commit.
- Multi-platform: `--platform=$BUILDPLATFORM` on build stages with cross-compilation avoids
  running the build under emulation, which the Docker docs say is slower for compute-heavy tasks such as compilation.
- Distroless images have no shell, so shell-based `HEALTHCHECK CMD` and `sh -c` entrypoints fail.

## Verify
- [ ] `docker history` shows no compilers, package caches or secrets in the final image.
- [ ] A one-line source change reuses the dependency layer.
- [ ] `docker inspect --format '{{.Config.User}}' <IMAGE>` shows a non-root user.
- [ ] Base images are pinned by digest and covered by an update bot.
- [ ] `.dockerignore` excludes `.git` and env files.

Related: computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes

## Checked

Checked 2026-10-23 against docker/docs (multi-stage builds, build best practices incl. USER and digest pinning, cache optimisation mount examples, multi-platform builds), the Dockerfile reference and the GoogleContainerTools/distroless README.
Fixed: distroless tags now use `debian13` (the README no longer lists `debian12`), and the nonroot/debug tag variants confirmed; removed the `USER nonroot` line. Confirmed cache mount examples for npm, pip, Go and apt (`sharing=locked`), secret mounts, `--cache-from/--cache-to` registry syntax, digest pinning, explicit UID/GID advice, `--no-log-init`. Removed unconfirmed claims about Alpine musl differences, Chainguard/Hardened Images licensing, hadolint/trivy/dive, tini, Kubernetes `runAsNonRoot` internals and cache-mount export behaviour.

Method: documentation only; no commands were run.
