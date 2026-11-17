---
id: computing-software.cybersecurity-defensive.zeek.input-framework-tables
name: input-framework-tables
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, input-framework, add-table, end-of-data, idx-val-records]
level: practitioner
status: docs-checked
description: "Read tab-separated files into Zeek tables or sets with Input::add_table, key and value records, Input::end_of_data and removing the stream."
sources: ["https://docs.zeek.org/en/current/frameworks/input.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# input framework tables

The default input format matches what the logging framework writes: tab-separated ASCII with a `#fields` line. Column order does not matter, as columns are matched by name.

```
#fields	ip	timestamp	reason
192.168.17.1	1333252748	Malware host
```

Define key and value records, a destination, and add the table:

```
type Idx: record { ip: addr; };
type Val: record { timestamp: time; reason: string; };
global denylist: table[addr] of Val = table();

event zeek_init() {
    Input::add_table([$source="denylist.file", $name="denylist",
                      $idx=Idx, $val=Val, $destination=denylist]);
    Input::remove("denylist");
}
```

For membership only, make the destination a `set[addr]` and omit `$val`.

Omitted columns (the `-` character) are only allowed for `&optional` fields in the value record; key columns cannot be omitted. Offending lines are skipped with a warning.

Reading is asynchronous: one thread per stream, so the table may be incomplete at first. Short runs can end before data arrives. Calls on a stream are queued, so `Input::remove` right after `add_table` waits until the read completes. Use the event to know when loading is done:

```
event Input::end_of_data(name: string, source: string) { print denylist; }
```

The input framework is unaware of the cluster and works on any node; the config and intel frameworks apply it on the manager.

## Checked

2026-11-08. Read the Input Framework page in full; every claim confirmed.

Method: documentation only; no commands were run.
