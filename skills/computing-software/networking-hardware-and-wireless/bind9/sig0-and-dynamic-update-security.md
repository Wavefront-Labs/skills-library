---
id: computing-software.networking-hardware-and-wireless.bind9.sig0-and-dynamic-update-security
name: sig0-and-dynamic-update-security
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, sig0, dynamic-update-security, nsupdate]
level: advanced
status: docs-checked
description: "Security notes for BIND 9 dynamic update: prefer TSIG over address-based allow-update, and the limited SIG(0) support."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sig0 and dynamic update security
ACLs can match the TSIG or SIG(0) key that signed a request as well as its source address, so `allow-update` and `update-policy` rules can require a key.

BIND partially supports SIG(0). A SIG(0) message is only verified if the key is known and trusted by the server, which does not fetch or validate keys itself. Signing of multiple-message TCP streams is not supported. `nsupdate` is the only tool shipped with BIND 9 that generates SIG(0) signed messages.

To require both an address and a key, nest the address test, as in `allow-update { !{ !localnets; any; }; key name.; };`, which succeeds only if the request comes from localnets and is signed with that key.

## Checked

2026-11-04. Confirmed against the ARM Access Control and SIG(0) sections. Removed the unconfirmed claim that IP-based `allow-update` can be spoofed and the advice on broad networks; added the documented SIG(0) limits.

Method: documentation only; no commands were run.
