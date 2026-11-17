---
id: computing-software.systems-network-administration.headscale.debug-endpoint
name: debug-endpoint
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, metrics, debug-endpoint, debugkey, prometheus]
level: advanced
status: docs-checked
description: "Use Headscale's metrics and debug endpoint on port 9090: access methods, debug key and debug IP, host checks, and keeping it private."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/debug.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics and debug endpoint

Controlled by `metrics_listen_addr` (default localhost:9090). Set it to `null` to disable the interface entirely.

## Access

```
curl http://localhost:9090/debug/
ssh <HEADSCALE_SERVER> -L 9090:localhost:9090
```

Endpoints: `/metrics` (Prometheus; accepts any Host header), `/debug/` (overview).

## Debug key or IP

```
openssl rand -hex 32 | tee debugkey.txt
export TS_DEBUG_KEY_PATH=debugkey.txt
export TS_ALLOW_DEBUG_IP=192.168.0.10
headscale serve
```

Then request `http://<IP_OF_HEADSCALE>:9090/debug/?debugkey=<DEBUG_KEY>`. The key must be sent with every request. The debug IP is ignored when `X-Forwarded-For` is present.

## Host check

Accepted hosts: an IP literal, `localhost`, the host in `server_url`, and the hostname in `metrics_listen_addr` (case-insensitive, trailing dot ignored). Other hostnames get HTTP 403 on all debug paths, including statsviz. `dns.base_domain` adds no accepted hosts.

## Contents

Go runtime and memory stats, connected nodes and pending registrations, active policy and filters, SSH policy, current DERPMap, Prometheus metrics.

## Gotcha

Keep this endpoint private to your internal network; do not expose it to the Internet.

## Checked

2026-11-04. Confirmed against the Headscale debugging page and config-example.yaml: metrics_listen_addr (127.0.0.1:9090 in the example, null or empty disables), curl and SSH forwarding access, debug key and debug IP environment variables, X-Forwarded-For note, the host check and HTTP 403, and the endpoint contents.
Method: documentation only; no commands were run.
