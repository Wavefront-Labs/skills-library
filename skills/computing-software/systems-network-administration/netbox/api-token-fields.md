---
id: computing-software.systems-network-administration.netbox.api-token-fields
name: api-token-fields
category: computing-software
field: systems-network-administration
product: netbox
tags: [api-tokens, token-v2, allowed-ips]
level: practitioner
status: docs-checked
description: "Understand v1 and v2 tokens and the restriction fields available."
sources: ["https://netboxlabs.com/docs/netbox/models/users/token/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API tokens

Goal: issue least-privilege credentials for automation.

A token is a secret credential tied to a user that authenticates requests to the REST and GraphQL APIs. A user may hold several; each can be expired, restricted or revoked independently. Requests run as the owning user.

**Versions (v4.5 and later).** v2 tokens are the default for new tokens, stored only as a salted HMAC digest with the plaintext shown once at creation. They need `API_TOKEN_PEPPERS` set. Legacy v1 tokens store plaintext, are deprecated and will be removed in v5.0.

**Fields**

- Description: name the application using it.
- Expires: optional; tokens without it never expire.
- Last Used: updated at most once per minute.
- Enabled: unset to temporarily revoke without deleting.
- Write Enabled: unset for read-only; POST, PATCH, PUT and DELETE are rejected.
- Allowed IPs: optional IPv4 or IPv6 prefixes the token may be used from.
- Key (v2): short identifier sent in plaintext to locate the record.

**Checklist**

1. Use v2.
2. Set Expires and Allowed IPs.
3. Disable write for read-only jobs.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Token model page and REST API page: v2 default with peppers, v1 deprecated and removed in v5.0, token fields, allowed IPs, write-enabled behaviour. Removed: Nothing.

Method: documentation only; no commands were run.
