---
id: computing-software.systems-network-administration.coredns.coredns-root-plugin
name: coredns-root-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, root, zone-files, tls, paths]
level: intro
status: docs-checked
description: "Set the base directory used to resolve relative file paths, knowing that only file, tls and dnssec honour it."
sources:
  - https://coredns.io/plugins/root/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define where CoreDNS looks for relative files.

Syntax: `root PATH`. The default root is CoreDNS's current working directory. A relative PATH is relative to that directory. The plugin can be used only once per server block.

Example, serving zone data from a directory:

```
. {
    root /path/to/zones
}
```

Important limitation: the docs say the root directory is not supported by all plugins. Only these respect it:
- file
- tls
- dnssec

Combining with tls: the certificate and key must also sit in the root directory.

```
tls://example.com:853 {
    root /path/to/config
    tls cert.pem key.pem
    whoami
}
```

This looks for `cert.pem` and `key.pem` under the root.

## Checked

2026-11-08. Checked in full against the root plugin README. Removed a parenthetical about hosts, loadbalance and sign pages, and a claim about the request chain, neither of which this page states.

Method: documentation only; no commands were run.
