---
id: computing-software.networking-hardware-and-wireless.powerdns.pdnsutil-tsigkey-autoprimary-network
name: pdnsutil-tsigkey-autoprimary-network
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdnsutil, tsigkey, autoprimary, network, views, generate, activate]
level: practitioner
status: docs-checked
description: "pdnsutil tsigkey generate/import/activate/deactivate/delete/list, autoprimary add/list/remove, network set/list and views commands."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdnsutil tsigkey, autoprimary, network, views

TSIG keys (hmac-md5, hmac-sha1, hmac-sha224, hmac-sha256, hmac-sha384, hmac-sha512):
- `tsigkey generate NAME ALGORITHM`, `tsigkey import NAME ALGORITHM KEY`, `tsigkey list`.
- `tsigkey activate ZONE NAME primary|secondary|producer|consumer`: sets `TSIG-ALLOW-AXFR` for primary/producer and `AXFR-MASTER-TSIG` for secondary/consumer.
- `tsigkey deactivate ZONE NAME ...`: undoes that.
- `tsigkey delete NAME [ALGORITHM]`: does not deactivate the key where it is in use.

Autoprimaries:
- `autoprimary add <IP> <NAMESERVER> [ACCOUNT]`
- `autoprimary list`
- `autoprimary remove IP NAMESERVER` (not supported by the BIND backend)

Networks and views:
- `network set NET [VIEW]`: omit VIEW to delete the assignment. `network list`.
- `views add-zone VIEW ZONE..VARIANT`, `views del-zone VIEW ZONE..VARIANT`, `views list VIEW`, `views list-all`.

Before 5.0 `autoprimary add` was named `add-autoprimary`.

## Checked

2026-11-08. Read docs/manpages/pdnsutil.1.rst in full and docs/modes-of-operation.rst in full. Confirmed the TSIG algorithms, tsigkey commands and metadata effects, autoprimary commands, network set and list, and views commands. Removed the old names import-tsig-key and activate-tsig-key, which no page read states; kept add-autoprimary, which modes-of-operation.rst states. Description shortened.

Method: documentation only; no commands were run.
