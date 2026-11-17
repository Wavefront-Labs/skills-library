---
id: computing-software.networking-hardware-and-wireless.bind9.logging-categories-and-query-errors
name: logging-categories-and-query-errors
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, logging-categories, query-errors, xfer-out]
level: practitioner
status: docs-checked
description: "Route BIND 9 log categories to channels, silence with null, and read the query-errors category for SERVFAIL diagnosis."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logging categories and query errors
Assign each category to channels. To discard a category use the `null` channel:

```
category xfer-out { null; };
```

The `query-errors` category records why and how queries resulted in error responses. At debug level 1 (or info when query logging is active) each SERVFAIL response is logged with the client, name, class, type and the source line that detected the error. At level 2 detailed context about failed recursive resolutions is added. At level 3 the same messages as level 1 are logged for errors other than SERVFAIL.

Use categories such as `queries`, `security`, `dnssec`, `xfer-in`, `xfer-out` and `notify` to route related events to their own files. Query logging is controlled by `querylog` or `rndc querylog`; at startup, specifying the `queries` category also enables it unless `querylog` is set.

## Checked

2026-11-04. Confirmed against the ARM logging block, `query-errors` category and `queries` category text. Rewrote the debug-level description from the manual and corrected the missing semicolon in the category example.

Method: documentation only; no commands were run.
