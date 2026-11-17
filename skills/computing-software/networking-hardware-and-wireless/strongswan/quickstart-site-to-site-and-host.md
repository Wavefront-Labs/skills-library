---
id: computing-software.networking-hardware-and-wireless.strongswan.quickstart-site-to-site-and-host
name: quickstart-site-to-site-and-host
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, quickstart, site-to-site, host-to-host, swanctl-conf]
level: intro
status: docs-checked
description: "Minimal swanctl.conf for strongSwan site-to-site and host-to-host tunnels with certificate authentication, file locations, and loading with swanctl --load-creds and --load-conns."
sources:
  - https://docs.strongswan.org/docs/latest/config/quickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quickstart site to site and host
Each endpoint needs the CA certificate in `/etc/swanctl/x509ca/`, its own certificate in `/etc/swanctl/x509/` and its key in `/etc/swanctl/private/`. The CA certificate must be on all endpoints to authenticate peers.

Site-to-site gateway moon (10.1.0.0/16) to sun (10.2.0.0/16):

```
connections {
  net-net {
    remote_addrs = 192.168.0.2
    local  { auth = pubkey
             certs = moonCert.pem }
    remote { auth = pubkey
             id = "C=CH, O=strongSwan, CN=sun.strongswan.org" }
    children {
      net-net {
        local_ts  = 10.1.0.0/16
        remote_ts = 10.2.0.0/16
        start_action = trap
      }
    }
  }
}
```

sun mirrors it with swapped addresses and traffic selectors. Identities default to the certificate subject DNs.

Host-to-host uses the same layout; omit the traffic selectors. Tunnel mode is the default even though transport mode would suffice.

Load with `swanctl --load-creds` (certificates and keys) and `swanctl --load-conns` (connections from swanctl.conf). `start_action = trap` sets up the SA on the first plaintext packet that needs the tunnel.

## Checked
2026-11-04. Confirmed against the strongSwan Configuration Quickstart page: file locations, site-to-site and host-to-host examples, default tunnel mode, swanctl --load-creds and --load-conns, start_action = trap. Nothing removed.

Method: documentation only; no commands were run.
