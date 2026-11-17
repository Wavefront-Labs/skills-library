---
id: computing-software.networking-hardware-and-wireless.bind9.tls-and-doh-listeners
name: tls-and-doh-listeners
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, tls, doh, dot, http]
level: advanced
status: docs-checked
description: "Configure encrypted DNS listeners in BIND 9: tls block, http block, listen-on tls and http, and built-in ephemeral and none."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls and doh listeners
A `tls` block defines TLS parameters: `key-file`, `cert-file`, `ca-file`, `dhparam-file`, `remote-hostname`, `protocols`, `cipher-suites`, `ciphers`, `prefer-server-ciphers`, `session-tickets`. Built-in names: `ephemeral` and `none`.

An `http` block sets `endpoints` (default `/dns-query`), `listener-clients` and `streams-per-connection`.

```
http local {
    endpoints { "/dns-query"; };
};
options {
    listen-on tls ephemeral http local { any; };
};
```

`ephemeral` uses a key and certificate created for the running instance; for production use a named `tls` block with real `key-file` and `cert-file`.

## Checked

2026-11-04. Read the tls and http block definitions in the Administrator Reference Manual: option lists, ephemeral and none built-ins, the /dns-query default and the DoH example. Nothing was removed.

Method: documentation only; no commands were run.
