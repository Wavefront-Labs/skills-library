---
id: computing-software.networking-hardware-and-wireless.bind9.tsig-keys
name: tsig-keys
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, tsig, tsig-keygen, hmac-sha256]
level: practitioner
status: docs-checked
description: "Create and use TSIG keys in BIND 9: tsig-keygen, key blocks, server keys, allow-update with key, and BADKEY, BADSIG, BADTIME errors."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter7.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tsig keys
Generate a key with `tsig-keygen name > file` (default hmac-sha256, 256 bits). `ddns-confgen` also generates keys and update-policy hints.

Add the key to `named.conf` on both servers:

```
key "host1-host2." {
    algorithm hmac-sha256;
    secret "base64-secret";
};
server 10.1.2.3 { keys { host1-host2.; }; };
```

Require a key for updates:

```
allow-update { !{ !localnets; any; }; key host1-host2.; };
```

Errors: BADKEY (unknown key), BADSIG (bad signature), BADTIME (time outside the allowed range); the response code is NOTAUTH. The key text contains the secret, so keep it out of world-readable files.

## Checked

2026-11-04. Read the TSIG section of the Administrator Reference Manual (Generating a Shared Key, Loading a New Key, Instructing the Server to Use a Key, TSIG-Based Access Control, Errors) and the tsig-keygen man page. Reworded the BADTIME and secret-handling sentence to match the page.

Method: documentation only; no commands were run.
