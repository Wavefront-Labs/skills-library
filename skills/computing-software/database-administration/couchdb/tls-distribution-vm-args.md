---
id: computing-software.database-administration.couchdb.tls-distribution-vm-args
name: tls-distribution-vm-args
category: computing-software
field: database-administration
product: couchdb
tags: [tls, erlang-distribution, vm-args, no-tls, remsh, clouseau]
level: advanced
status: docs-checked
description: "Enable TLS Erlang distribution in vm.args with -proto_dist couch, the -couch_dist no_tls values, the clouseau exception, and connecting remsh."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/tls_erlang_distribution.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `vm.args` (use absolute paths to your own files):

```
-proto_dist couch
-couch_dist no_tls \"clouseau@127.0.0.1\"
-ssl_dist_optfile </absolute_path/to/couch_dist.conf>
```

The page states that the default value of `no_tls` is `false`, and that if no `no_tls` flag is set, all nodes use TCP. For search to work, set `no_tls` for the `clouseau` node (by default `"clouseau@127.0.0.1"`).

Values:

- `-couch_dist no_tls false`: TLS only (the default value).
- `-couch_dist no_tls true`: TCP only.
- Specific nodes on TCP, others TLS: repeat the flag per node, for example `-couch_dist no_tls \"node2@127.0.0.1\"`.
- Pattern: `-couch_dist no_tls \"*@127.0.0.1\"` puts every node ending in `@127.0.0.1` on TCP. `*` matches zero or more occurrences and `?` zero or one.

**Remote shell.** `./remsh` for a TCP node; for a TLS node `./remsh -t </absolute_path/to/couch_dist.conf>`.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/tls_erlang_distribution page (Config Settings, Connect to Remsh): the three vm.args lines, no_tls notes and clouseau default node, the four value forms, wildcard and question-mark notes, remsh commands. Nothing removed.

Method: documentation only; no commands were run.
