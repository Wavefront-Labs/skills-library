---
id: computing-software.messaging-and-integration.prosody.certificate-locations
name: certificate-locations
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, tls, certificates, ssl, permissions]
level: practitioner
status: docs-checked
description: "Where Prosody looks for TLS certificates: the certs directory, HOSTNAME.crt/key and fullchain.pem/privkey.pem names, the certificates option, and key permissions."
sources:
  - https://prosody.im/doc/certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate locations

By default Prosody searches the `certs` directory beside the config (`/etc/prosody/certs`). Change it with the global `certificates` option (not valid under a VirtualHost or Component).

Per host it tries `HOSTNAME.crt` + `HOSTNAME.key`, then `HOSTNAME/fullchain.pem` + `HOSTNAME/privkey.pem`. Services such as `legacy_ssl` and `https` use the service name, e.g. `https.crt`; override with options like `https_certificate`.

Manual per-host location:

```lua
VirtualHost "example.com"
  ssl = {
    certificate = "/etc/prosody/certs/example.com.crt";
    key = "/etc/prosody/certs/example.com.key";
  }
```

Other `ssl` options: `capath`, `password` (plain text in config is a risk).

Chains: put the intermediate after your certificate in the file; Let's Encrypt `fullchain.pem` already does.

Permissions: key readable by the Prosody user only, e.g. mode `640` owner `root:prosody`, and parent directories readable by Prosody.

Verify: `prosodyctl check certs` passes and `prosodyctl reload` picks up new files.

## Checked

2026-11-04. Read the Prosody certificates page: the certs directory beside the config and the global-only certificates option, HOSTNAME.crt/key and HOSTNAME/fullchain.pem and privkey.pem search order, service certificates such as https.crt with https_certificate, the manual ssl block, capath and password options with the plain-text warning, intermediate certificates after your own, and mode 640 root:prosody with readable parent directories all match. Nothing removed.

Method: documentation only; no commands were run.
