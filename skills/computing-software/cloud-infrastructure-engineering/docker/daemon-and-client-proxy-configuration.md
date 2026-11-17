---
id: computing-software.cloud-infrastructure-engineering.docker.daemon-and-client-proxy-configuration
name: daemon-and-client-proxy-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, proxy, http-proxy, corporate-proxy, daemon-proxies-key, dockerd-proxy, config-json-proxies, client-proxy, no-proxy]
level: practitioner
description: "Configure HTTP(S) proxies separately for dockerd pulls (daemon.json proxies or systemd env) and for containers and builds (~/.docker/config.json proxies) with correct NO_PROXY."
sources: ["https://docs.docker.com/engine/daemon/proxy/", "https://docs.docker.com/engine/cli/proxy/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Daemon and client proxy configuration

Two independent settings, and people configure the wrong one:
- **Daemon proxy**: used by dockerd for `pull`/`push`/`login`.
- **Client (container) proxy**: env vars injected into containers and builds.

## Daemon
`daemon.json` (the recommended way; or `dockerd --http-proxy` and `--https-proxy`):
```json
{ "proxies": {
    "http-proxy": "http://proxy.corp:3128",
    "https-proxy": "http://proxy.corp:3128",
    "no-proxy": "localhost,127.0.0.1,.corp,registry.internal,10.0.0.0/8"
} }
```
Alternative: environment variables in the daemon's start-up environment (`HTTP_PROXY`, `http_proxy`, `HTTPS_PROXY`, `https_proxy`, `NO_PROXY`, `no_proxy`), for example a systemd drop-in
```ini
# /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://proxy.corp:3128"
Environment="HTTPS_PROXY=http://proxy.corp:3128"
Environment="NO_PROXY=localhost,127.0.0.1,.corp,registry.internal"
```
`systemctl daemon-reload && systemctl restart docker`. Settings in daemon.json take
precedence over the environment. Rootless: same drop-in under `~/.config/systemd/user/docker.service.d/`, with `systemctl --user` and no `sudo`.
Docker Desktop ignores `proxies` in daemon.json; use the proxy settings in Docker Desktop instead. In systemd values, double-escape special characters such as `#?!()[]{}` as `%%`.

## Containers and builds
`~/.docker/config.json` of the user running the docker CLI:
```json
{ "proxies": { "default": {
    "httpProxy": "http://proxy.corp:3128",
    "httpsProxy": "http://proxy.corp:3128",
    "noProxy": "localhost,127.0.0.1,.corp,*.svc"
} } }
```
The CLI sets `HTTP_PROXY`/`http_proxy` etc. (also `ftpProxy` and `allProxy` keys) in `docker run` containers and as build
arguments for `docker build`; it applies only to new containers and builds, with no daemon restart. The `default` key covers all daemons; to configure one daemon use its address instead (for example `"tcp://docker-daemon1.example.com": {...}`).

Ad hoc: `docker build --build-arg HTTPS_PROXY=... .` or `docker run --env HTTPS_PROXY=...`. Proxy build args are predefined, need no `ARG` declaration, and are not included in the build output.

## NO_PROXY gotchas
- Include registry mirrors, internal registries, `localhost`, `127.0.0.1`, and service
  names your containers call (`db`, `.internal`).
- There is no standard for how clients parse proxy variables, so format support varies by tool; list hostnames and domains as well as any IP ranges.
- For the daemon, a domain matches itself and its subdomains, a leading dot (`.corp`) matches subdomains only, and `*` disables proxying.
- The CLI config sets both the uppercase and lowercase variables for containers and builds.

## Gotchas
- Proxy settings may hold credentials: environment variables are stored in plain text in the container configuration and can be read through the API or committed with `docker commit`.
- Do not use `ENV` in a Dockerfile for proxy settings; use build arguments, as the proxy value is otherwise embedded in the image.

## Verify
```sh
docker run --rm alpine sh -c 'env | grep -i _PROXY'
docker pull alpine:3.20
```

## Checked

Checked against docker/docs `engine/daemon/proxy.md` and `engine/cli/proxy.md` (latest commit 2026-10-23, Engine 29).

- `proxies` keys in daemon.json (`http-proxy`, `https-proxy`, `no-proxy`), daemon.json taking precedence over environment variables, restart needed, and Docker Desktop ignoring daemon.json proxies.
- `~/.docker/config.json` keys `httpProxy`, `httpsProxy`, `ftpProxy`, `noProxy`, `allProxy`, the `default` key and per-daemon address keys, new containers and builds only.
- Rootless drop-in path `~/.config/systemd/user/docker.service.d/` and the `%%` escaping rule.
- Removed as unconfirmed: the "Engine 23+" gate, CIDR support by client library, `docker info` proxy lines, the TLS-intercept CA advice and the claim about `docker history`.

Method: documentation only; no commands were run.
