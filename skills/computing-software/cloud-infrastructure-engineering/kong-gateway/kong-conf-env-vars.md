---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.kong-conf-env-vars
name: kong-conf-env-vars
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, kong-conf, kong-env-prefix, kong-restart, configuration, environment-variables]
level: intro
status: docs-checked
description: "Where Kong finds kong.conf, how KONG_ environment variables override it, and the commands that apply changes: restart, reload and a custom --conf path."
sources:
  - https://developer.konghq.com/gateway/manage-kong-conf/
  - https://developer.konghq.com/gateway/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kong.conf and environment variables

Template: `/etc/kong/kong.conf.default`. Copy it to create your working file:

```bash
cp /etc/kong/kong.conf.default /etc/kong/kong.conf
```

Without `--conf`, Kong looks for `kong.conf` at `/etc/kong/kong.conf` and then `/etc/kong.conf`. Use `-c` or `--conf` to give another path:

```bash
kong start --conf ./kong.conf
```

Environment variables win over the file. Name them with the parameter in uppercase and a `KONG_` prefix, for example:

```bash
export KONG_LOG_LEVEL=error
```

Nginx directives follow the same rule: `KONG_NGINX_HTTP_SSL_PROTOCOLS` maps to `nginx_http_ssl_protocols`.

Commented-out parameters fall back to their defaults.

Apply changes:
- `kong restart` for file changes.
- In Docker quickstart containers, set the environment variable and use `kong reload`.

To validate and inspect, see the kong check and prepare skill.

## Checked

2026-11-04. Confirmed against the Managing Kong Gateway configuration page and kong.conf.default: template path, copy step, the two default search paths, `-c`/`--conf`, `KONG_` override, `KONG_NGINX_HTTP_SSL_PROTOCOLS` mapping, commented defaults, `kong restart` and Docker `kong reload`. Nothing removed.
Method: documentation only; no commands were run.
