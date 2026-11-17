---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-kv-store-cli
name: consul-kv-store-cli
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, kv-store, consul-kv, kv-import-export]
level: practitioner
status: docs-checked
description: "Put, get, export and import Consul KV data with the consul kv command, view metadata, and use check-and-set for safe updates."
sources: ["https://developer.hashicorp.com/consul/commands/kv", "https://developer.hashicorp.com/consul/commands/kv/put", "https://developer.hashicorp.com/consul/commands/kv/get", "https://developer.hashicorp.com/consul/commands/kv/delete", "https://developer.hashicorp.com/consul/docs/automate/kv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Consul KV stores configuration parameters and metadata. It is not intended as a full-featured datastore; the maximum object size is 512 KB.

```sh
consul kv put config/web/timeout 30s
consul kv put config/web/password @password.txt   # value from a file; "-" reads stdin
consul kv get config/web/timeout
consul kv get -detailed config/web/timeout        # includes ModifyIndex and flags
consul kv get -recurse config/web/
consul kv get -keys config/                        # key names only
consul kv export config/ > config-backup.json
consul kv import @config-backup.json              # -prefix=<p> sets a key prefix (1.10+)
consul kv delete -recurse config/old/
```

For concurrent writers use check-and-set: `consul kv put -cas -modify-index=<ModifyIndex> key value`. `kv delete` also accepts `-cas` with `-modify-index`, but not together with `-recurse`.

Gotchas:
- `kv put KEY` with no data overwrites the key with an empty value.
- For many entries at once use `kv import`; the transaction API does up to 64 KV operations atomically.
- With ACLs on, the token needs `key:read` for `get` and `export` and `key:write` for `put` and `import` (rules on `key` or `key_prefix`).
- The KV data lives on the servers; back it up with `consul snapshot`.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/kv (index, put, get, delete, export, import) and automate/kv (512 KB limit, snapshot backup, ACL requirement). Removed: "confirm for your version" hedge on the size limit, the claim that exports base64-encode values, the claim about recursive deletes being recoverable only by snapshot, and the Verify step.
Method: documentation only; no commands were run.
