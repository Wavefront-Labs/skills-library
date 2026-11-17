---
id: computing-software.networking-hardware-and-wireless.squid.external-acl-helper
name: external-acl-helper
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, external-acl-type, helper, ttl, children-max, tag]
level: advanced
status: docs-checked
description: "Define an external ACL helper with external_acl_type: options, format macros and the OK/ERR/BH reply protocol."
sources:
  - https://www.squid-cache.org/Doc/config/external_acl_type/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# external_acl_type
Syntax: `external_acl_type name [options] FORMAT /path/to/helper [helper arguments]`.

Options (defaults): `ttl=n` (3600 s), `negative_ttl=n`, `grace=n`, `cache=n` (262144), `children-max=n` (5), `children-startup=n` (0), `children-idle=n` (1), `concurrency=n`, `queue-size=N` (2 x children-max), `protocol=2.5`, `ipv4`/`ipv6`.

Format macros: `%ACL`, `%DATA` (arguments from the `acl ... external` line), logformat codes, and `%USER_CERT` style codes with SSL.

Reply: `[channel-ID] result keyword=value ...`. Results `OK` (matched), `ERR` (no match), `BH` (helper error). Keywords: `user=`, `password=`, `message=`, `tag=`, `log=`, `clt_conn_tag=`.
```
user=John%20Smith
user="John Smith"
```

## Checked

2026-11-04. Read the external_acl_type directive page and confirmed the syntax, each option and default, the format macros, the OK, ERR and BH results and the keywords. Nothing was removed.

Method: documentation only; no commands were run.
