---
id: computing-software.networking-hardware-and-wireless.squid.connect-and-read-timeouts
name: connect-and-read-timeouts
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, connect-timeout, read-timeout, timeouts]
level: practitioner
status: docs-checked
description: "Tune origin and peer timeouts with connect_timeout and read_timeout."
sources:
  - https://www.squid-cache.org/Doc/config/connect_timeout/
  - https://www.squid-cache.org/Doc/config/read_timeout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# connect_timeout and read_timeout
- `connect_timeout`: how long to wait for the TCP connect to an origin or peer. Default 1 minute. On timeout Squid looks for another forwarding path.
- `read_timeout`: how long to wait for data on peer server connections. Each successful read extends the timeout. Default 15 minutes. On expiry the request aborts and is logged as ERR_READ_TIMEOUT.

## Checked

2026-11-04. Read the connect_timeout and read_timeout directive pages and confirmed both defaults and behaviours, including ERR_READ_TIMEOUT. Nothing was removed.

Method: documentation only; no commands were run.
