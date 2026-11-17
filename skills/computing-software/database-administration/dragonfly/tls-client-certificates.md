---
id: computing-software.database-administration.dragonfly.tls-client-certificates
name: tls-client-certificates
category: computing-software
field: database-administration
product: dragonfly
tags: [client-certificate, mutual-tls, tls-ca-cert-file, dragonfly]
level: advanced
status: docs-checked
description: "Authenticate Dragonfly clients with TLS client certificates instead of passwords by supplying a client CA via tls_ca_cert_file."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/using-tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instead of passwords, clients can authenticate with certificates. You manage the certificates yourself, so Let's Encrypt is not needed.

Server:

```bash
sudo ./dragonfly --tls \
  --tls_key_file=/etc/mycerts/server_key.pem \
  --tls_cert_file=/etc/mycerts/server_cert.pem \
  --tls_ca_cert_file=/etc/mycerts/clients_root_ca.pem
```

`tls_ca_cert_file` is the certificate authority certificate used to validate client connections.

Client:

```bash
redis-cli --tls -h <domain> \
  --key /etc/mycerts/client_priv.pem \
  --cert /etc/mycerts/client_cert.pem
```

Notes:

- Only `.pem` files are supported by Dragonfly.
- For a CA directory use `tls_ca_cert_dir` after running `c_rehash` on it.
- Replication can use the same arrangement; see replication over TLS.
- On Kubernetes with the Operator, set `authentication.clientCaCertSecret` (server TLS must also be enabled) so only clients holding a certificate signed by that CA can connect.

## Checked

2026-11-04. Confirmed in the Dragonfly TLS guide (client authentication section), the flags page (`tls_ca_cert_file`, `tls_ca_cert_dir`, `c_rehash`), the Replication page (`.pem` only) and the Operator configuration page (`clientCaCertSecret`). Nothing removed.

Method: documentation only; no commands were run.
