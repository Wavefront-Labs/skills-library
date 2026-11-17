---
id: computing-software.cybersecurity-defensive.zeek.log-filters-and-paths
name: log-filters-and-paths
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, log-filter, add-filter, path-func, default-logdir]
level: practitioner
status: docs-checked
description: "Use Log::Filter to rename logs, set Log::default_logdir, write extra files with include or exclude fields, drop the default filter, path_func."
sources: ["https://docs.zeek.org/en/current/frameworks/logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# log filters and paths

A stream with no filters writes nothing. Creating a stream attaches a filter named `default`. Filter names are unique per stream; `Log::add_filter` with an existing name replaces it. Remove with `Log::remove_filter`.

**Rename**: fetch and change `path` (never include the extension):

```
local f = Log::get_filter(Conn::LOG, "default");
f$path = "myconn";
Log::add_filter(Conn::LOG, f);
```

**Directory**: `redef Log::default_logdir = /path/to/output_log_directory`, honoured by the ASCII and SQLite writers.

**Extra file with fewer fields**:

```
local filter: Log::Filter = [$name="orig-only", $path="origs",
                             $include=set("ts", "id.orig_h")];
Log::add_filter(Conn::LOG, filter);
```

`$exclude` lists unwanted fields instead. Two filters with the same path get numeric suffixes such as `conn-2`, with a warning.

**Dynamic path**: `$path_func=myfunc`, where the function takes `(id: Log::ID, path: string, rec: ...)` and returns a string, for example `fmt("%s-%s", path, r)` for local versus remote. Typing `rec` as `record { id: conn_id; }` makes it reusable on any stream with that field. Beware creating many files quickly.

Field names can be translated with `Log::default_field_name_map` or a filter's `field_name_map`, for example `id.orig_h` to `id_orig_h`.

## Checked

2026-11-08. Read the Logging Framework page in full; every claim confirmed.

Method: documentation only; no commands were run.
