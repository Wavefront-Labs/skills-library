---
id: computing-software.database-administration.yugabytedb.yb-ts-cli-tablet-commands
name: yb-ts-cli-tablet-commands
category: computing-software
field: database-administration
product: yugabytedb
tags: [yb-ts-cli, tablet-server, flush-tablet, set-flag, delete-tablet, remote-bootstrap, refresh-flags, reload-certificates]
level: advanced
status: docs-checked
description: "Reference for yb-ts-cli, which talks to a single tserver: flush, compact, delete and remote-bootstrap tablets, and change flags in memory with set_flag."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-ts-cli.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# yb-ts-cli tablet commands

yb-ts-cli performs operations on one particular tablet server. yb-admin commands focus on cluster administration; yb-ts-cli commands apply to specific YB-TServer nodes. The binary is in the `bin` directory of the YugabyteDB home.
```
yb-ts-cli [ --server_address=<host>:<port> ] <command> <flags>
```
The default server address is `localhost:9100` (the tserver RPC port). `--timeout_ms` defaults to 60000. For a TLS cluster add `--certs_dir_name` with the directory holding the root certificate.

Server state:
- `status` (node instance, bound RPC and HTTP addresses, version), `is_server_ready` (reports tablets not yet bootstrapped), `current_hybrid_time`
- `list_tablets`, `are_tablets_running`
- `clear_server_metacache` clears the tablet-location metacaches on that server

Tablet data:
- `flush_tablet <tablet-id>`, `flush_all_tablets`
- `compact_tablet <tablet-id>`, `compact_all_tablets`; compaction includes pgvector vector indexes by default, and `--exclude_vector_indexes` skips them
- `count_intents` (uncommitted intents) and `dump_tablet <tablet-id>` for debugging
- `delete_tablet <tablet-id> "<reason-string>"` deletes the tablet with the reason recorded
- `remote_bootstrap <source-host> <tablet-id>` triggers a remote bootstrap of a tablet from another tablet server to the specified server (source is a host or host and port)

Flags and certificates:
- `set_flag [--force] <flag> <value>` changes the in-memory value of a flag atomically on a running server. The change does NOT persist across restarts. A typical flow is to set the flag in memory and separately edit the configuration file the server starts with.
- `--force` allows changing a flag not marked runtime-settable; the change may be ignored or crash the server on unsafe values. Not every flag is runtime-settable (for example the bind address), so check the configuration reference pages.
- `refresh_flags` reloads flags from the configuration file; issue it on each process, since one server does not update the others. It works on masters as well as tservers.
- `reload_certificates` reloads TLS certificates and private keys from disk on the master or tablet server.

## Checked

2026-11-09: command list, syntax, defaults and the set_flag, refresh_flags and reload_certificates behaviour confirmed against the yb-ts-cli reference page (yugabyte-db docs admin/yb-ts-cli.md, read in full). Removed the unsourced manual split and broken-replica sequences and the port claim for masters (the page's port statements are inconsistent). `delete_tablet` and `remote_bootstrap` argument forms corrected to match the page.

Method: docs-checked 2026-11-09 against yugabyte-db docs admin/yb-ts-cli.md
