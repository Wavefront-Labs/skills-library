---
id: computing-software.messaging-and-integration.redpanda.rpk-admin-api-addresses
name: rpk-admin-api-addresses
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, admin-api, rpk-admin-hosts, environment-variable, redpanda-yaml, precedence]
level: practitioner
status: docs-checked
description: "Tell rpk where each broker Admin API is: the -X admin.hosts flag, RPK_ADMIN_HOSTS, or rpk.admin_api in redpanda.yaml, which commands need it, and the precedence order."
sources:
  - https://docs.redpanda.com/streaming/current/get-started/admin-addresses/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Admin-related rpk commands need the Admin API address of each broker (IPs or hostnames, default port 9644). Three methods exist, in decreasing precedence:

1. Command line flag `-X admin.hosts`
2. Environment variable `RPK_ADMIN_HOSTS`
3. `rpk.admin_api` in `redpanda.yaml`

**Which commands.** `rpk security user` and every `rpk cluster` subcommand except `rpk cluster info` and `rpk cluster metadata` use `-X admin.hosts`. Those two use `-X brokers` (the Kafka API) instead. `rpk redpanda admin` takes `--hosts` and is deprecated in 26.2.

**Environment variable**, lasting for the shell session:

```bash
export RPK_ADMIN_HOSTS="192.168.78.34:9644,192.168.78.35:9644,192.168.78.36:9644"
```

**Config file.** Each broker generates a `redpanda.yaml` with an `rpk` section. The default `admin_api` address is `0.0.0.0` on port 9644. Replace it with the real addresses:

```yaml
rpk:
  admin_api:
    - 192.168.72.34:9644
    - 192.168.72.35:9644
```

If you leave the defaults, you must pass the addresses by flag or environment variable.

## Checked

2026-11-04. The three methods, precedence, command table, example values and defaults were confirmed on the Admin API addresses page.
Method: documentation only; no commands were run.
