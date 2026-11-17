---
id: computing-software.networking-hardware-and-wireless.bind9.raw-zone-format-and-compilezone
name: raw-zone-format-and-compilezone
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, raw-format, named-compilezone, masterfile-format]
level: practitioner
status: docs-checked
description: "Store BIND 9 zones in raw binary format with masterfile-format and convert with named-compilezone."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raw zone format and compilezone
`masterfile-format ( raw | text )` selects the on-disk format of zone files. The default is `text`, except for secondary zones, where it is `raw`. It can be set in `options`, `view` or `zone`.

When a non-text file is loaded, named may skip some checks; `check-names` applies only to text. Generate raw files with the same check level as the configuration.

`named-compilezone` converts a zone from one format to another. Options include `-f` for the input format (`text` or `raw`) and `-F` for the output format (`text`, `raw` or `raw=N`, where N is the raw format version: 0 is readable by any named, 1, the default, needs 9.9.0 or higher).

```
named-compilezone -f text -F raw -o example.com.raw example.com example.com.db
```

Do not run `named-compilezone` or `named-checkzone` on zone text from an untrusted source: `$INCLUDE` directives make the parser read any file the invoking user can read, and fragments can leak through error messages.

## Checked

2026-11-04. Confirmed against the ARM `masterfile-format` entry and the named-compilezone man page (`-f`, `-F`, `raw=N`, untrusted-source warning). Replaced the vague hostile-input wording with the documented `$INCLUDE` risk.

Method: documentation only; no commands were run.
