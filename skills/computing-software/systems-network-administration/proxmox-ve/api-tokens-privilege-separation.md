---
id: computing-software.systems-network-administration.proxmox-ve.api-tokens-privilege-separation
name: api-tokens-privilege-separation
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [api-token, pveum, privsep, least-privilege]
level: practitioner
status: docs-checked
description: "Create Proxmox VE API tokens with privilege separation and expiry, and give a monitoring token read-only access with pveum."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pveum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API tokens give stateless access to most of the REST API. Console endpoints for VMs and the system are excluded, since they need user privileges. A compromised token can be revoked without disabling its user.

Two token types exist:

- Separated privileges: the token needs explicit ACLs, and can never have permissions on a path where its user has none.
- Full privileges: identical to the user's permissions. Disable separation only if the integration genuinely needs that.

Set an expiry (Unix epoch seconds) at creation, so abandoned automation stops working. The token value is shown only once and cannot be retrieved later.

Limited monitoring example for user `joe@pve`:

```
pveum acl modify /vms -user joe@pve -role PVEVMAdmin
pveum user token add joe@pve monitoring -privsep 1
pveum acl modify /vms -token 'joe@pve!monitoring' -role PVEAuditor
pveum user permissions joe@pve
pveum user token permissions joe@pve monitoring
```

A token can never do more than its user, and the second ACL limits it to viewing VMs.

Use the token by sending an HTTP `Authorization` header of the form `PVEAPIToken=USER@REALM!TOKENID=UUID`. Revoking a token does not disable its user.

## Checked

2026-11-09. Compared with the API Tokens section of https://pve.proxmox.com/pve-docs/chapter-pveum.html. Removed the claim that separation is the default and the intersection wording, which the page does not state.

Method: documentation only; no commands were run.

