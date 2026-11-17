---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-secret-stores
name: telegraf-secret-stores
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [secretstores, secrets, credentials, mlock, secret-reference]
level: practitioner
status: docs-checked
description: "Explains Telegraf secret stores, the @{store:name} reference syntax, chaining stores, supported options and memory locking limits. Use to keep credentials out of config files."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secret stores

Secret stores keep credentials out of plain-text configuration. Configure one or more secret store plugins, then reference secrets in plugin options. Telegraf resolves them at runtime and protects them in memory.

## Reference syntax

```text
@{<secret_store_id>:<secret_name>}
```

`secret_store_id` is the unique `id` you give the store plugin; both parts may contain only letters, numbers and underscores.

## Configure

```toml
[[secretstores.os]]
  id = "local_secrets"

[[secretstores.jose]]
  id = "cloud_secrets"
  path = "/etc/telegraf/secrets"
  password = "@{local_secrets:cloud_store_passwd}"

[[outputs.influxdb_v3]]
  urls = ["http://localhost:8181"]
  token = "@{cloud_secrets:influxdb_token}"
```

One store can unlock another, as shown. Available stores include the OS keyring, Docker secrets, systemd credentials and encrypted files.

## Limits

Not all options support secrets. An option must be implemented as secret-capable; using a reference elsewhere fails. Each plugin's docs mark supported options.

## Memory locking

Telegraf locks the memory pages holding secrets, so the locked-memory limit must cover the number of secrets. It checks at startup and warns if too low; raise it with `ulimit -l`. In a FreeBSD jail add `allow.mlock = 1;` to the jail definition.

## Checked

Method: docs-checked 2026-11-09 against the Use secrets in Telegraf configurations page (raw markdown in github.com/influxdata/docs-v2, read in full). All claims confirmed.
