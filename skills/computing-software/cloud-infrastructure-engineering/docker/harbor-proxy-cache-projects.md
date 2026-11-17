---
id: computing-software.cloud-infrastructure-engineering.docker.harbor-proxy-cache-projects
name: harbor-proxy-cache-projects
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, harbor, harbor-proxy-cache, pull-through-cache, registry-mirror, rate-limit, docker-hub]
level: advanced
status: docs-checked
description: "Set up Harbor proxy cache projects for Docker Hub, GHCR or Quay: registry endpoints, pull paths incl. library/, caching behaviour, retention, and limits vs a daemon mirror."
sources: ["https://goharbor.io/docs/main/administration/configure-proxy-cache/", "https://goharbor.io/docs/main/administration/configuring-replication/create-replication-endpoints/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Harbor proxy cache projects

A proxy cache project in Harbor fetches images from an upstream registry on first pull and
serves them from Harbor afterwards. Unlike `registry-mirrors` in `daemon.json` (Docker Hub
only), Harbor can proxy the registries listed under Setup.

## Setup
1. **Administration > Registries > New Endpoint**: choose a provider supported for proxy cache (Harbor,
   Docker Hub, Docker registry, AWS ECR, Azure Container Registry, Google Container Registry / Artifact
   Registry, GitHub Container Registry, JFrog Artifactory; the proxy cache page also lists Quay), URL
   and credentials. Users of the proxy project can pull anything the endpoint's access account can
   reach, so use least-privilege credentials.
2. **Projects > New Project**: enable **Proxy Cache**, select the endpoint, optionally set the
   bandwidth limit to the upstream (-1 means no limit), name it e.g. `dockerhub`. Set public or keep
   private with robot accounts.
3. Pull through it:
```bash
docker pull harbor.example.com/dockerhub/library/nginx:1.27      # Hub official images live under library/
docker pull harbor.example.com/dockerhub/goharbor/harbor-core:dev
docker pull harbor.example.com/ghcr/org/app:1.2                  # project proxying ghcr.io
```

## Behaviour
- First pull of an uncached image is fetched from the target and cached. Later pulls check the target's
  latest manifest: unchanged means the cached image is served, changed means the new image is pulled,
  served and cached; if the target is unreachable the cached image is served; if the image is gone from
  the target nothing is served.
- Since Harbor v2.1.1 the check is a HEAD request, which does not trigger the Docker Hub rate limiter;
  pulling an updated image does count towards it.
- You cannot push to a proxy cache project; it otherwise supports the same features as a normal project.
- Harbor creates a 7 day retention policy by default for each new proxy cache project; review it so the
  cache does not grow unbounded.
- The proxy follows upstream authentication challenges (`WWW-Authenticate: Bearer realm=...`), and the
  token service can be on a different host (as with Docker Hub); only configure endpoints inside your
  trust boundary.

## Point clients at it
- Rewrite image references in manifests/Compose (`harbor.example.com/dockerhub/...`). This is
  explicit and works everywhere.
- containerd (Kubernetes nodes) can map `docker.io` to the proxy project via `hosts.toml` with the
  server URL carrying the `/v2/<proxy_project>` path and `override_path = true` (the field marks that the
  API root is defined in the URL path); see the containerd mirror skill.

## Gotchas
- Official Docker Hub images are under `library/`; the Harbor replication docs call this out for filters.
- Robot accounts need pull permission on the proxy project; anonymous pulls require the
  project to be public.

## Checked

2026-10-26. Documentation release: Harbor website docs main (goharbor/website, last commit 2026-10-15), containerd/containerd docs/hosts.md main. Confirmed: supported proxy cache registries, new proxy project fields (endpoint and bandwidth, -1 for no limit), pull flow and the four scenarios, HEAD check since v2.1.1 and rate limiter note, no push to proxy projects, default 7 day retention, authentication challenge note, containerd override_path meaning and default false. Removed unconfirmed claims: proxying "any OCI registry", digest-pull behaviour, the `not found` error for missing library/, and the statement about Docker's registry-mirrors path handling.

Method: documentation only; no commands were run.
