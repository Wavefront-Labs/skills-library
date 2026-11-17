---
id: computing-software.systems-network-administration.coredns.coredns-hosts-plugin
name: coredns-hosts-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, hosts, hosts-file, wildcard, ptr]
level: practitioner
status: docs-checked
description: "Serve A, AAAA and PTR records from a hosts-style file or inline entries, with ttl, reload, wildcard and fallthrough behaviour."
sources:
  - https://coredns.io/plugins/hosts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: answer names from a hosts file.

Syntax:

```
hosts [FILE [ZONES...]] {
    [INLINE]
    ttl SECONDS
    no_reverse
    reload DURATION
    fallthrough [ZONES...]
}
```

- FILE defaults to the system hosts file; a relative path is prefixed with the root plugin path.
- Only A, AAAA and PTR are supported. The plugin can be used once per server block.
- The file is scanned every 5 seconds. If it is deleted, inlined content keeps being served; when restored it is used again.
- INLINE lines are extra hosts entries and override entries of the file.
- `ttl` default is 3600 seconds. `reload 0` disables reloading.
- PTR records are generated automatically and cannot be created manually; `no_reverse` disables them.
- Without `fallthrough`, a name with no match is not passed on.

Wildcards: `*` as the leftmost label matches one extra label. With `192.168.1.10 *.example.com`, `apps.example.com` resolves, but `example.com` (the apex) and `deep.apps.example.com` do not. Wildcard entries do not generate PTR records.

Blocking use: the plugin works with public hosts files that block advertising servers.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/hosts/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
