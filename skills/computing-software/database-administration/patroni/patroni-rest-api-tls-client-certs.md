---
id: computing-software.database-administration.patroni.patroni-rest-api-tls-client-certs
name: patroni-rest-api-tls-client-certs
category: computing-software
field: database-administration
product: patroni
tags: [patroni, security, tls, client-certificates, patronictl]
level: advanced
status: docs-checked
description: "Enable TLS on the REST API, require client certificates with verify_client, and configure ctl to match."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: mutual TLS between Patroni, patronictl and the API.

Server-side keys in `restapi`:
- `certfile` (PEM). If missing or empty, the API runs without SSL.
- `keyfile`, `keyfile_password`.
- `cafile`: CA bundle used to verify client certificates.
- `ciphers`: permitted cipher suites.
- `verify_client`: `none` (default), `optional` or `required`. With `required`, client certificates are needed for all API calls and authentication succeeds if signature verification passes. With `optional`, a certificate is required only for PUT, POST, PATCH and DELETE.

Client side, the `ctl` section is used by patronictl:
- `ctl.authentication.username/password`: default to the restapi values if absent.
- `ctl.insecure`: allow connections without verifying SSL certificates.
- `ctl.cacert`: CA bundle or directory; defaults to `restapi.cafile`.
- `ctl.certfile`, `ctl.keyfile`, `ctl.keyfile_password`: client certificate.

Warning from the docs: if `restapi.verify_client` is `required`, you must also provide valid client certificates in `ctl.certfile`, `ctl.keyfile` and `ctl.keyfile_password`; otherwise Patroni does not work correctly.

## Checked

2026-11-08: Read the full YAML Configuration Settings page (patroni.readthedocs.io, latest). Confirmed the restapi TLS keys, verify_client semantics, the ctl keys and defaults, and the warning. Removed the `patronictl -k` claim, the PKI mutual-auth sentence and "Patroni's own calls" because that page does not state them.

Method: documentation only; no commands were run.
