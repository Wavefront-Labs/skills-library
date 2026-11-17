---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-boot-fields-next-server
name: dhcp4-boot-fields-next-server
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, next-server, siaddr, boot-file-name, pxe, tftp]
level: practitioner
status: docs-checked
description: "Set siaddr, sname and file (next-server, server-hostname, boot-file-name) globally, per subnet or per host reservation in kea-dhcp4."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 next server and boot fields
Some clients use the `siaddr`, `sname` and `file` header fields instead of options 66 and 67.

- `next-server` sets siaddr (a TFTP server, for example). Global or per subnet; the subnet value wins. In a subnet, "0.0.0.0" means do not send it, and an empty string is the same as undefined (use the global value).
- `server-hostname` goes in sname (up to 64 bytes).
- `boot-file-name` goes in file (up to 128 bytes).
- Both are handled the same way as `next-server`.

Per host, put them in a reservation:

```json
{ "hw-address": "aa:bb:cc:dd:ee:ff", "next-server": "10.1.1.2",
  "server-hostname": "server-hostname.example.org",
  "boot-file-name": "/usr/local/share/kea/bootfile.efi" }
```

They combine with other reservation parameters such as an address; a subset or none may be given.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (DHCPv4 chapter Next Server (siaddr) and host reservation sections). Removed: nothing.
Method: documentation only; no commands were run.
