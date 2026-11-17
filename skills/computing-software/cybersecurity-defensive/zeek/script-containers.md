---
id: computing-software.cybersecurity-defensive.zeek.script-containers
name: script-containers
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, table-type, set-type, vector-type, container-types]
level: practitioner
status: docs-checked
description: "Declare and use Zeek tables, sets and vectors: constructors, add and delete, composite indices, disallowed index types, hashing caveat."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tables, sets and vectors

**table**: `table[type+] of type`. The index cannot be `file`, `opaque` or `any`.

```
global t: table[count] of string = {
    [11] = "eleven",
    [5] = "five",
};
global t2 = table(
    [192.168.0.2, 22/tcp] = "ssh",
    [192.168.0.3, 80/tcp] = "http"
);
t[13] = "thirteen";
delete t[13];
```

Deleting a missing key does nothing. `delete t;` removes every element (page marks it added in 7.0). Membership uses `in` and `!in`.

**set**: like a table without values, same index type limits.

```
global s: set[port] = { 21/tcp, 23/tcp, 80/tcp, 443/tcp };
global s3 = set(21/tcp, 23/tcp);
add s[22/tcp];
```

**vector**: like a table indexed by non-negative integers from zero: `global v: vector of string;` and `local v = vector("one", "two", "three");`.

A constructor can be named by a type when the index type is ambiguous: `type MySet: set[MyRec]; global s4 = MySet([$b=1], [$b=2]);`

Caveat: complex index values (records, sets) are hashed at access time, so later changes to the index value do not affect the entry. After `t[s] = "http"` and `add s[8080/tcp]`, `t[set(80/tcp, 8000/tcp)]` still prints `http`, but `t[s]` is an error: no such index.

## Checked

2026-11-08. Read the Types page in full; every claim confirmed.

Method: documentation only; no commands were run.
