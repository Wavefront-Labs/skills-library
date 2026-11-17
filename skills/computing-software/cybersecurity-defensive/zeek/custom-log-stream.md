---
id: computing-software.cybersecurity-defensive.zeek.custom-log-stream
name: custom-log-stream
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, log-stream, create-stream, log-write, extend-info-record]
level: practitioner
status: docs-checked
description: "Create a Zeek log stream with Log::create_stream, the &log attribute and Log::write; extend existing Info records, log events, disable streams."
sources: ["https://docs.zeek.org/en/current/frameworks/logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# custom log stream

Define an ID, a record whose fields carry `&log`, create the stream, then write:

```
module Foo;
export {
    redef enum Log::ID += { LOG };
    type Info: record {
        ts: time &log;
        id: conn_id &log;
        service: string &log &optional;
        missed_bytes: count &log &default=0;
    };
    global log_foo: event(rec: Info);
}
event zeek_init() &priority=5
    {
    Log::create_stream(Foo::LOG, [$columns=Info, $ev=log_foo, $path="foo"]);
    }
```

Fields without `&log` are not output. A nested record such as `conn_id` flattens into columns named with periods (`id.orig_h`). `Log::write(Foo::LOG, rec)` sends data; creating a stream adds a default filter automatically. Add a field to `connection` so other handlers reach the record.

**Extending a log**: `redef record Conn::Info += { is_private: bool &default=F &log; };`. New fields need `&default` or `&optional`, plus `&log`. Set them before the write, for example in `connection_state_remove` at a higher priority than the handler that writes.

**Logging event**: the `$ev` handler runs on each write; every default stream has one (`Conn::log_conn`), which can raise notices in real time.

**Disable**: `Log::disable_stream(Conn::LOG);` must run after the stream exists, so use a lower priority than creation.

## Checked

2026-11-08. Read the Logging Framework page in full; every claim confirmed.

Method: documentation only; no commands were run.
