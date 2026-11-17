---
id: computing-software.cloud-infrastructure-engineering.openbao.leases-and-revocation
name: leases-and-revocation
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, lease, revoke-prefix, renew, increment]
level: practitioner
status: docs-checked
description: "Renew and revoke OpenBao leases: lease_id, the advisory increment, token-wide revocation and prefix revocation during an incident."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/lease.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leases and revocation

Every dynamic secret and `service` token gets a lease: metadata with a TTL, renewability and more. The secret is guaranteed valid for the TTL; afterwards OpenBao may revoke it. The KV engine does not issue leases (it may still return a lease duration value).

## Renew

Reading a dynamic secret returns a `lease_id`.

```
bao lease renew -increment=3600 my-lease-id
```

- The increment counts from now, not from the end of the existing TTL, so you can also shorten a lease.
- It is advisory only: the backend may ignore or cap it. Read the renewal response for the real new lease.

## Revoke

```
bao lease revoke my-lease-id
bao lease revoke -prefix auth/userpass/
```

- Revocation invalidates the secret immediately and blocks renewals (for the Kubernetes secrets engine it deletes the related service accounts).
- Revoking a token revokes every lease created with it.
- Lease IDs start with the request path, so `-prefix` revokes a whole mount's secrets, which suits intrusion response. It requires appropriate access control.

Can also be done in the UI Access tab or by the API.

## Checked

2026-11-04. Confirmed against the Lease, renew, and revoke page: lease content, KV not issuing leases, lease_id, the renew increment from the current time and its advisory nature, immediate revocation, token revocation revoking its leases, and prefix revocation. Nothing removed.

Method: documentation only; no commands were run.
