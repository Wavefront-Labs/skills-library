---
id: computing-software.systems-network-administration.coredns.coredns-identity-nsid-and-chaos
name: coredns-identity-nsid-and-chaos
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, nsid, chaos, identification, anycast]
level: intro
status: docs-checked
description: "Identify which CoreDNS instance answered using the nsid EDNS0 option or CH class TXT queries with the chaos plugin."
sources:
  - https://coredns.io/plugins/nsid/
  - https://coredns.io/plugins/chaos/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tell servers apart, such as in anycast setups.

nsid (RFC 5001) adds an EDNS0 OPT record carrying a server identifier to replies. Syntax: `nsid [DATA]`; without DATA the host's name is used. It can be used once per server block.

```
example.org {
    whoami
    nsid Use The Force
}
```

A client with NSID support (`dig +nsid`) then sees the identifier.

chaos answers TXT queries in the CH class. Syntax: `chaos [VERSION] [AUTHORS...]`. VERSION defaults to `CoreDNS-<version>`; AUTHORS defaults to all GitHub handles in the OWNERS files.

The plugin must receive queries for these zones: `version.bind`, `version.server`, `authors.bind`, `hostname.bind` and `id.server`. List them in the block header, or use `.`:

```
version.bind version.server authors.bind hostname.bind id.server {
    chaos CoreDNS-001 info@coredns.io
}
```

Test with `dig @localhost CH TXT version.bind`, which returns `"CoreDNS-001"`.

Use cases: NSID is useful in anycast setups to see which server generated a reply and for debugging. The chaos answer looks like `version.bind. 0 CH TXT "CoreDNS-001"`.

## Checked

2026-11-08. Checked in full against the nsid and chaos plugin READMEs. The chaos content was previously uncited, so the chaos page was added as a source; removed a closing claim about IN class resolution.

Method: documentation only; no commands were run.
