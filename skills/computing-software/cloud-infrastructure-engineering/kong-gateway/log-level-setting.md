---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.log-level-setting
name: log-level-setting
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, log-level, notice, error-log, kong-conf, logging]
level: intro
status: docs-checked
description: "Set Kong's log_level in kong.conf: the levels from debug to crit, the notice default, the error.log location, and the KONG_LOG_LEVEL override."
sources:
  - https://developer.konghq.com/gateway/logs/
  - https://developer.konghq.com/gateway/manage-kong-conf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# log_level

Levels, least to most severe: `debug`, `info`, `notice`, `warn`, `error`, `crit`. The default is `notice`. Use `debug` only while troubleshooting.

Logs go to `logs/error.log` under the prefix, which by default is `/usr/local/kong/logs/error.log`. On Docker you can also read them from the container.

Persistent change in `kong.conf`:

```
log_level = error
```

then `kong restart` (a restart is required).

Environment override, which wins over the file:

```
export KONG_LOG_LEVEL=error
```

In the Docker quickstart containers, set the environment variable and run `kong reload`.

To change the level without restarting, use the Admin API instead (see the dynamic log level skill). That change is not written to `kong.conf` and reverts on restart.

Access logging is separate: it is governed by `proxy_access_log`.

## Checked

2026-11-04. Confirmed against the Kong Gateway logs page, the Managing Kong Gateway configuration page and kong.conf.default: level names and meanings, `notice` default, error.log location, kong.conf example, restart requirement, `KONG_LOG_LEVEL` override and Docker `kong reload`, non-persistent dynamic change. Nothing removed.
Method: documentation only; no commands were run.
