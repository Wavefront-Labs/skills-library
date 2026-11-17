---
id: computing-software.messaging-and-integration.redpanda.bootstrap-file-and-admin-api-first-user
name: bootstrap-file-and-admin-api-first-user
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [bootstrap-yaml, rp-bootstrap-user, admin-api, superusers, scram, custom-deployment]
level: advanced
status: docs-checked
description: "Pre-seed cluster configuration with .bootstrap.yaml, create the first SCRAM user with RP_BOOTSTRAP_USER, and choose how to secure the Admin API before first start."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/production/production-deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For custom deployments that do not use the supported Ansible, Helm or Operator tools, cluster configuration normally goes through the Admin API and `rpk cluster config`. To provide configuration before the very first start, write a `.bootstrap.yaml` next to `redpanda.yaml`. It is read only on the first startup of the cluster; later edits are ignored and must be made through the Admin API.

Example from the page, enabling Admin API authentication with one superuser:

```yaml
admin_api_require_auth: true
superusers:
- alice
```

With this, the Admin API is not accessible until you bootstrap a user.

**First user.** Set `RP_BOOTSTRAP_USER` when starting Redpanda for the first time, in the form `username:password[:mechanism]`. The only mechanisms are `SCRAM-SHA-512` and `SCRAM-SHA-256` (the default if omitted), for example `RP_BOOTSTRAP_USER=alice:letmein:SCRAM-SHA-512`. It only creates the account; you still configure authentication through cluster configuration.

**Securing the Admin API** (it creates SASL users and ACLs, so decide up front):
- No authentication but listening only on 127.0.0.1, when only administrators can reach the host.
- mTLS: generate client and server x509 certificates before first start, reference them in `redpanda.yaml`, and use the client certificate to call the API.
- Username and password: combine `admin_api_require_auth`, `superusers` and `RP_BOOTSTRAP_USER`, and still enable TLS on the Admin API endpoint to protect credentials in flight.

## Checked

The bootstrap file behavior and example, RP_BOOTSTRAP_USER format and the three Admin API security options were confirmed on the Deploy for Production: Manual page (Custom deployment section).

Method: docs-checked 2026-11-09 against the Deploy for Production: Manual page, read in full; no commands were run.
