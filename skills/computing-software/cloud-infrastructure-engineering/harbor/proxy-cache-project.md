---
id: computing-software.cloud-infrastructure-engineering.harbor.proxy-cache-project
name: proxy-cache-project
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [proxy-cache, pull-through, docker-hub-rate-limit, registry-endpoint, harbor]
level: practitioner
status: docs-checked
description: "Create a Harbor proxy cache project over a registry endpoint, use the pull prefix, and know how upstream updates, outages and retention behave."
sources:
  - https://goharbor.io/docs/main/administration/configure-proxy-cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A proxy cache project pulls from a target registry through a registry endpoint and caches the images. Supported targets: Harbor, Docker Hub, Docker registry, AWS ECR, Azure Container Registry, Google Container Registry, Quay, GitHub Container Registry and JFrog Artifactory. You cannot push to a proxy cache project; otherwise it behaves like a normal project.

Setup:
1. Create a registry endpoint first (Administration, Registries).
2. Projects, **New Project**, switch on the **Proxy Cache** slider and choose the endpoint. Bandwidth is the pull speed limit to the upstream registry; `-1` means no limit.
3. Pull with the project as prefix:
`docker pull <harbor_server_name>/<proxy_project_name>/goharbor/harbor-core:dev`

Behaviour on later pulls:
- Upstream unchanged: the cached image is served.
- Upstream changed: the new image is pulled, served and cached.
- Upstream unreachable: the cached image is served.
- Image gone upstream: nothing is served.

Since v2.1.1 Harbor sends a HEAD request to check whether layers changed, which does not trigger the Docker Hub rate limiter.

Gotchas: every user with access to the project can pull anything the endpoint access account can pull, so use least-privilege credentials. Harbor follows the upstream `WWW-Authenticate: Bearer realm` challenge for tokens, and that token service may be on another host, so only configure trusted endpoints. Each new proxy cache project gets a 7 day tag retention policy by default.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Configure Proxy Cache.
Method: documentation only; no commands were run.
