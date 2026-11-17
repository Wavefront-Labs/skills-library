---
id: computing-software.cybersecurity-defensive.zeek.log-writers-and-extensions
name: log-writers-and-extensions
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, log-writer, ascii-writer, extension-fields, print-to-log]
level: practitioner
status: docs-checked
description: "Choose log writers (ASCII default, LogAscii::use_json, Log::default_writer), add extension columns with Log::default_ext_func, redirect print output, and local vs remote logging."
sources: ["https://docs.zeek.org/en/current/frameworks/logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# log writers and extensions

Each filter has a writer; the default is ASCII. Change it for all filters by redefining `Log::default_writer`, or per filter through its `writer` field.

The ASCII writer emits metadata header lines (format, path, creation and close times) then the data. Options are in `base/frameworks/logging/writers/ascii.zeek`. Some are global, such as JSON output for all logs:

```
redef LogAscii::use_json = T;
```

Others apply per filter. Check that downstream parsers still recognise a changed format.

**Extension fields**: records returned by `Log::default_ext_func` are appended to every log, and a filter's `ext_func` overrides locally. The prefix defaults to an underscore (`Log::default_ext_prefix`, or filter `ext_prefix`).

```
function add_extension(path: string): Extension
    {
    return Extension($write_ts=network_time(), $stream=path, $system_name=peer_description);
    }
redef Log::default_ext_func = add_extension;
```

Extension fields are invisible to filters, policy hooks and log events.

**print redirection**: `Log::print_to_log` takes `Log::REDIRECT_NONE` (default), `Log::REDIRECT_STDOUT` or `Log::REDIRECT_ALL`. `Log::print_log_path` names the file and `Log::log_print` is the event.

**Local versus remote**: single nodes log locally; in clusters only loggers do, others forward. Rarely changed via `Log::enable_local_logging` and `Log::enable_remote_logging`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
