---
id: computing-software.database-administration.dragonfly.tls-certificate-rotation
name: tls-certificate-rotation
category: computing-software
field: database-administration
product: dragonfly
tags: [certificate-rotation, tls, config-set-tls, zero-downtime, dragonfly]
level: advanced
status: docs-checked
description: "Rotate Dragonfly TLS certificates without downtime by updating the tls file flags and running CONFIG SET tls true."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/using-tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To rotate the certificate of a running TLS-enabled Dragonfly server:

1. Update the `tls_key_file`, `tls_cert_file` and `tls_ca_cert_file` server flags to match the new TLS configuration (for example replace the files at the same paths, or change the flag values you start with).
2. Reload the TLS configuration with no downtime:

```bash
redis-cli --tls -h <domain> -a ${DFLY_PASS_TOKEN} CONFIG SET tls true
```

`CONFIG SET` is an admin command (`@admin`, `@dangerous`), so run it with a user that may do so.

Verification:

- `INFO server` over a TLS listener can include the subject, issuer and validity period of the listener's certificate, so you can confirm the new certificate is live.
- Reconnect a client and check it still works.

On Kubernetes the Operator takes the TLS Secret from the `tlsSecretRef` field of the Dragonfly resource; the Secret must be in the same namespace.

## Checked

2026-11-04. Confirmed in the Dragonfly TLS guide (rotation section), the CONFIG SET page (ACL categories) and the INFO page (certificate details over TLS) and the Operator configuration page (`tlsSecretRef`). Removed the unconfirmed Secret key names and the cert-manager 90-day duration claim.

Method: documentation only; no commands were run.
