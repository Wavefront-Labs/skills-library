---
id: computing-software.search-and-information-retrieval.apache-solr.bin-solr-cli
name: bin-solr-cli
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [bin-solr, solr-cli, control-script, solr-start, zk-subcommands]
level: intro
status: docs-checked
description: "Use the bin/solr control script: start, stop, create, delete, config, zk subcommands, healthcheck, export, auth, and common start options."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/solr-control-script-reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bin-solr-cli

`bin/solr` manages a node. Subcommands seen in the reference: `start`, `stop`, `restart`, `status`, `create`, `delete`, `config`, `zk`, `healthcheck`, `export`, `api` and `auth`.

Start options: `-p` port, `-m` heap, `-z`/`--zk-host`, `--host`, `--solr-home`, `--server-dir`, `--jvm-opts`, `-e <name>` for examples such as `techproducts`, `--force`. `-Dname=value` passes system properties, for example `bin/solr start -Dsolr.autoSoftCommit.maxTime=3000`. `--user-managed` starts standalone mode, which was the default until Solr 10.

Examples from the guide:
- `bin/solr config -c mycollection --action set-property --property updateHandler.autoCommit.maxDocs --value 100` (also `unset-property` and the user-property forms).
- `bin/solr export --solr-url http://localhost:8983 -c gettingstarted --limit -1`.
- `bin/solr zk ls -r /collections/mycollection`, `zk mkroot /solr -z <zkHost>`, `zk mv`, `zk downconfig`.

Options such as `-c <collection>`, `-z`, and `--solr-url` select the target. Each subcommand has its own `--help`, for example `bin/solr start --help`.

## Checked

2026-11-04. Confirmed against the Solr Control Script Reference: subcommands, start options, `-Dsolr.autoSoftCommit.maxTime=3000` example, `--user-managed` (default until Solr 10), `zk mkroot`, `zk downconfig`. Removed the generic `<command> --help` claim in favour of the documented `bin/solr start --help` form.

Method: documentation only; no commands were run.
