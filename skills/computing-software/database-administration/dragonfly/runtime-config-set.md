---
id: computing-software.database-administration.dragonfly.runtime-config-set
name: runtime-config-set
category: computing-software
field: database-administration
product: dragonfly
tags: [config-set, runtime-config, config-get, dragonfly]
level: intro
status: docs-checked
description: "Change Dragonfly settings without a restart using CONFIG SET one parameter at a time, and list supported parameters with CONFIG GET *."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/config-set.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`CONFIG SET parameter value` reconfigures the server at runtime without restarting. It is in the `@admin`, `@slow`, `@dangerous` ACL categories.

- Only one parameter can be set per call.
- `CONFIG GET *` lists the parameters that are supported and their current values.
- Not every flag can be changed at runtime.

```shell
dragonfly> CONFIG SET maxmemory 10gb
OK
dragonfly> CONFIG GET *
```

The flags page lists `CONFIG SET` as one of the ways to set a flag and says not all flags can be configured at runtime. It states that `jwt_validate` can be changed at runtime, and that `pubsub_slow_subscriber_timeout_ms` is startup-only, like `publish_buffer_limit`.

## Checked

2026-11-04. Confirmed against the Dragonfly CONFIG SET page and flags page: syntax, ACL categories, runtime reconfiguration, `CONFIG GET *`, one parameter at a time, the `maxmemory 10gb` example, `jwt_validate` runtime change, the startup-only note. Removed the TLS reload and cluster_announce_ip, announce_port claims, which neither page states.

Method: documentation only; no commands were run.
