---
id: computing-software.messaging-and-integration.prosody.prosodyctl-cert-commands
name: prosodyctl-cert-commands
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, prosodyctl, certificates, csr, self-signed, renewal]
level: practitioner
status: docs-checked
description: "prosodyctl certificate workflow for Prosody: cert request, cert generate, --root cert import for renewal hooks, then reload."
sources:
  - https://prosody.im/doc/certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prosodyctl cert commands

```
prosodyctl check certs
prosodyctl cert request example.com
prosodyctl cert generate example.com
prosodyctl --root cert import /path/to/certificates
prosodyctl reload
```

- `cert request`: creates a certificate signing request to send to a certificate authority.
- `cert generate`: creates a self-signed certificate. The Common Name must match the VirtualHost domain.
- `--root cert import`: copies certificates and keys into Prosody's certificates directory and signals Prosody to reload. Suited to cron jobs or ACME renewal hooks (`--root` lets prosodyctl write to paths the prosody user cannot write).
- `reload`: applies new certificates and keys without a restart.
- `check certs`: basic sanity checks of the certificate configuration.

Verify: after import, `prosodyctl check certs` shows valid expiry dates for every host.

## Checked

2026-11-04. Read the Prosody certificates page: cert request (CSR), cert generate (self-signed, Common Name must be the VirtualHost domain), --root cert import copying to the certificates directory and signalling reload, use from cron or ACME clients, and prosodyctl reload all match. Reworded the --root explanation to the page's wording.

Method: documentation only; no commands were run.
