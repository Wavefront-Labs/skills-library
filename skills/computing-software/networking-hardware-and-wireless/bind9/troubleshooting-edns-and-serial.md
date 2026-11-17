---
id: computing-software.networking-hardware-and-wireless.bind9.troubleshooting-edns-and-serial
name: troubleshooting-edns-and-serial
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, troubleshooting, edns-compliance, sslkeylogfile]
level: practitioner
status: docs-checked
description: "BIND 9 troubleshooting recipes: EDNS-broken servers with server clauses and dig tests, decrypting DoT and DoH with SSLKEYLOGFILE, and fixing a serial that went too high."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter9.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# troubleshooting edns and serial
Set up logging first; log files hold the first clues.

EDNS problems: broken authoritative servers may drop EDNS queries. Test:

```
dig soa <zone> @<server> +dnssec
dig soa <zone> @<server> +dnssec +nocookie
dig soa <zone> @<server> +noedns
```

If the first fails but the second succeeds, the server most likely needs `send-cookie no` in a `server` clause. If the first two fail but the third succeeds, it needs `edns no`.

Encrypted DNS: set the `SSLKEYLOGFILE` environment variable for named so Wireshark can decrypt DoT and DoH. Needs OpenSSL 1.1.1 or newer; check with `named -V`.

Serial set too high: add 2147483647 to the serial, reload, wait until all secondaries have it, then set the intended number and reload again. A secondary will not update while the primary's serial is lower than its own.

## Checked

2026-11-04. Read the Troubleshooting chapter: logging advice, EDNS compliance tests and server clause fixes, SSLKEYLOGFILE with the OpenSSL 1.1.1 requirement, and the 2147483647 serial fix confirmed. Made the dig test outcomes match the page wording.

Method: documentation only; no commands were run.
