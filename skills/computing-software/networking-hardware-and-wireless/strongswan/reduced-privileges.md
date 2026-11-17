---
id: computing-software.networking-hardware-and-wireless.strongswan.reduced-privileges
name: reduced-privileges
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, capabilities, non-root, hardening, charon]
level: practitioner
status: docs-checked
description: "Run the strongSwan charon daemon with dropped Linux capabilities or as a non-root user, with the configure flags, strongswan.conf options and updown caveat."
sources:
  - https://docs.strongswan.org/docs/latest/install/reducedPrivileges.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# reduced privileges
**Capability dropping.** charon starts as root and drops most privileges immediately, then more after initialization. Build with `--with-capabilities=libcap` (needs libcap) or `--with-capabilities=native` (uses capset(2)). Depending on loaded plugins charon keeps some capabilities, such as `CAP_NET_ADMIN` or `CAP_NET_RAW`, to talk to the kernel IPsec subsystem or use raw sockets.

**Non-root user.** Create a user and group, for example:

```
groupadd vpn
useradd -g vpn vpn
```

Then configure with `--with-user=vpn --with-group=vpn`. `make install` installs config files with that owner, but check existing permissions. Alternatively set `charon.user` and `charon.group` in strongswan.conf; adjust file permissions or the daemon may not read the swanctl directory.

**Caveat.** A non-root user breaks the iptables updown script (`connections.<conn>.children.<child>.updown` in swanctl.conf), because iptables does not allow non-root users to insert rules even with capabilities. Customise the script to call iptables via sudo. A non-root group alone does not affect it.

## Checked
2026-11-04. Confirmed against the strongSwan Running with Reduced Privileges page: --with-capabilities=libcap or native, retained capabilities, groupadd and useradd example, --with-user and --with-group, charon.user and charon.group, iptables updown caveat. Nothing removed.

Method: documentation only; no commands were run.
