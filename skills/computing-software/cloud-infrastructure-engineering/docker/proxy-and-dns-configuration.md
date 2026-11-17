---
id: computing-software.cloud-infrastructure-engineering.docker.proxy-and-dns-configuration
name: proxy-and-dns-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, proxy, http-proxy, https-proxy, no-proxy, dns-config, corporate-proxy, daemon-json, config-json, systemd-drop-in, resolv-conf, dns-search, build-proxy, mitm-ca]
level: practitioner
status: docs-checked
description: "Docker behind a corporate proxy: the three separate proxy layers (daemon pulls, build RUN steps, containers), daemon.json dns settings, and trusting a MITM CA for registries and builds."
sources: ["https://docs.docker.com/engine/daemon/proxy/", "https://docs.docker.com/engine/cli/proxy/", "https://docs.docker.com/engine/network/#dns-services", "https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://docs.docker.com/engine/security/certificates/", "https://docs.docker.com/engine/network/ca-certs/", "https://docs.docker.com/reference/dockerfile/#predefined-args"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy and DNS configuration

**Goal:** `docker pull`, `RUN apt-get` inside builds, and `curl` inside running containers
all reach the internet through the corporate proxy, and container DNS resolves internal
names — without hardcoding proxy settings into images.

## Three different things need proxy config
1. **The daemon** (image pulls/pushes, registry auth) — `daemon.json` (recommended):
   ```json
   {"proxies": {"http-proxy": "http://proxy.corp:3128",
                "https-proxy": "http://proxy.corp:3128",
                "no-proxy": "localhost,127.0.0.0/8,registry.corp,.corp.internal,10.0.0.0/8"}}
   ```
   Restart `dockerd`. Docker Desktop ignores these `daemon.json` proxies. Alternatively, on systemd a drop-in
   `/etc/systemd/system/docker.service.d/http-proxy.conf` with
   `[Service]` `Environment="HTTP_PROXY=..." "HTTPS_PROXY=..." "NO_PROXY=..."`, then
   `systemctl daemon-reload && systemctl restart docker`. Daemon configuration takes precedence over environment variables.
2. **Containers and build steps** (the client injects env vars) — `~/.docker/config.json`:
   ```json
   {"proxies": {"default": {"httpProxy": "http://proxy.corp:3128",
                            "httpsProxy": "http://proxy.corp:3128",
                            "noProxy": "localhost,127.0.0.1,.corp.internal"}}}
   ```
   The CLI sets `HTTP_PROXY`/`http_proxy` etc. in every `docker run` container and as
   build args for every `docker build`. The settings apply to new containers and builds only. In the image history, the proxy build args
   are **not** persisted (proxy args are special-cased out of `docker history`),
   which is exactly why this beats `ENV HTTP_PROXY` in a Dockerfile.
3. **One-off**: `docker build --build-arg HTTP_PROXY=... --build-arg HTTPS_PROXY=...` and
   `docker run -e HTTP_PROXY=...`. Same exclusion from history applies to these predefined args.

Never put `ENV HTTP_PROXY` in a Dockerfile: the image then fails everywhere the proxy
isn't reachable, and credentials in the URL ship with the image.

## NO_PROXY gotchas
- `NO_PROXY` entries can be IP prefixes, domain names (a leading `.` matches subdomains only) or `*`; ports are accepted (daemon documentation). Clients differ in what they honour, so list hosts explicitly where in doubt.
- Inside a container, `localhost` is the container, so `NO_PROXY=localhost` doesn't exclude
  other containers; add the Compose service names (and subnets, if your clients honour CIDR entries).
- Registry mirrors on the LAN must be in the daemon's `no-proxy` or pulls hairpin through
  the proxy.
- The CLI sets both the upper-case and lower-case variants (`HTTP_PROXY` and `http_proxy`, and so on).

## MITM / TLS-inspecting proxies
Symptom: `x509: certificate signed by unknown authority` on pull, or `SSL certificate
problem` in `RUN curl`.
- Daemon/registry: add the corporate root CA to the host's trust store (see your OS documentation) and restart docker. Per-registry only:
  `/etc/docker/certs.d/<registry>:<port>/ca.crt` (`.crt` files in that directory are treated as CA roots).
- Builds (Debian-based images): `COPY corp.crt /usr/local/share/ca-certificates/` then `RUN update-ca-certificates`
  early in the Dockerfile. Docker's guidance is to follow MITM-certificate best practice, since a compromised CA lets attackers intercept traffic.

## DNS
Containers on the default bridge get a copy of the host's `/etc/resolv.conf` minus loopback
addresses; if no usable nameserver remains Docker falls back to 8.8.8.8/8.8.4.4 and internal names stop
resolving (when `127.0.0.53` is the host's only nameserver, Docker reads `/run/systemd/resolve/resolv.conf` instead). On user-defined networks containers get the embedded DNS at `127.0.0.11`,
which forwards unknown names to the upstreams (the host's, or those you configure). Set them explicitly:
```json
{"dns": ["10.0.0.2", "10.0.0.3"], "dns-search": ["corp.internal"], "dns-opts": ["ndots:1"]}
```
Per container: `docker run --dns 10.0.0.2 --dns-search corp.internal`; Compose `dns:` /
`dns_search:`.
Docker Desktop has its own proxy settings in the Docker Desktop settings; see `docker-desktop-configuration-and-resources`.

## Verify
```bash
docker info | grep -i proxy                                          # daemon layer
docker run --rm alpine env | grep -i proxy                           # client-injected layer
docker run --rm alpine cat /etc/resolv.conf                          # 127.0.0.11 or your dns list
docker run --rm alpine nslookup intranet.corp.internal
docker build --no-cache --progress=plain - <<'EOF' 2>&1 | grep -i proxy
FROM alpine
RUN env
EOF
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the daemon proxy page (`proxies` keys `http-proxy`/`https-proxy`/`no-proxy`, systemd drop-in, precedence, NO_PROXY syntax, Desktop ignoring `daemon.json` proxies), the CLI proxy page (`~/.docker/config.json` `proxies.default` keys, env vars and build args, new containers and builds only), the Dockerfile reference (proxy ARGs excluded from `docker history`), the certificates page (`certs.d` and `.crt` handling), the MITM page (`COPY` + `update-ca-certificates`), the networking overview (DNS) and the moby resolvconf source (loopback handling and defaults). Removed unconfirmed claims: the Docker 23 version gate, per-context key behaviour, Go/Java NO_PROXY differences, apt/pip/npm proxy notes, distro trust-store paths, the secret-mount example, `insecure-registries` advice, BuildKit DNS behaviour and WSL resolv.conf behaviour.

Method: documentation only; no commands were run.
