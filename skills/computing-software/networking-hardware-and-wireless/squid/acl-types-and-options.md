---
id: computing-software.networking-hardware-and-wireless.squid.acl-types-and-options
name: acl-types-and-options
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, acl, src, dstdomain, access-control]
level: intro
status: docs-checked
description: "Define Squid access lists with the acl directive: syntax, option flags and the common built-in ACL types."
sources:
  - https://www.squid-cache.org/Doc/config/acl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACL types and options
Form: `acl aclname acltype argument ...`, or values read from a file, one per line: `acl aclname acltype "file"`.

Options: `-i` case-insensitive regex, `+i` case-sensitive, `-n` no lookups or address conversion, `-m[=delimiters]` match comma-separated tokens, `--` ends option parsing.

Common types:
- `src` client IP or range; `dst` URL host IP (slow)
- `port` destination TCP port; `proto` request protocol; `method` HTTP method
- `dstdomain`, `dstdom_regex` destination server; `url_regex` whole URL
- `time` day abbreviations plus an h1:m1-h2:m2 range
- `maxconn` client has more than N TCP connections
- `proxy_auth` username list or `REQUIRED` (slow)
- `ssl::server_name` with `--client-requested`, `--server-provided`, `--consensus`

Examples from the docs:
```
acl localnet src 10.0.0.0/8
acl password proxy_auth REQUIRED
```

## Checked

2026-11-04. Read the acl directive page and confirmed the syntax, the -i, +i, -n, -m and -- options, the listed ACL types with their fast or slow tags, the ssl::server_name flags and the two examples. Nothing was removed.

Method: documentation only; no commands were run.
