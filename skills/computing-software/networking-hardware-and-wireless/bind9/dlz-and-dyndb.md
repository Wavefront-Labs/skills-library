---
id: computing-software.networking-hardware-and-wireless.bind9.dlz-and-dyndb
name: dlz-and-dyndb
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dlz, dyndb, dynamically-loadable]
level: advanced
status: docs-checked
description: "BIND 9 dynamic data back ends: DLZ with dlopen and DynDB driver modules, and the caution about high-volume servers."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dlz and dyndb
Two interfaces load zone data from outside zone files.

DLZ (dynamically loadable zones):

```
dlz example {
    database "dlopen driver.so args";
    search yes;
};
```

The manual does not recommend DLZ on high-volume servers: text-to-wire conversion and no internal caching limit query performance. DLZ has no built-in support for DNS notify, so secondaries are not told of changes.

DynDB:

```
dyndb example "driver.so" {
    /* driver parameters */
};
```

Unlike DLZ, a DynDB module provides a full BIND zone database interface and can pre-load an in-memory database from the external source, giving native performance. DLZ cannot handle DNSSEC-signed data.

## Checked

2026-11-04. Confirmed against the ARM chapter 6 DLZ and DynDB sections: `dlz` with `database "dlopen ..."`, `search`, the high-volume warning, `dyndb` statement grammar. Replaced the unconfirmed claims about drivers updating the database and trusting drivers with the documented DynDB properties.

Method: documentation only; no commands were run.
