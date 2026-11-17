---
id: computing-software.systems-network-administration.virtualisation.proxmox-api-tickets-and-csrf-with-curl
name: proxmox-api-tickets-and-csrf-with-curl
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-api-ticket, csrfpreventiontoken, proxmox-api, api-token, pvesh, curl, proxmox]
level: practitioner
status: docs-checked
description: "Call the Proxmox VE REST API with curl using ticket cookies plus CSRFPreventionToken or API token headers, with examples for listing, starting and creating guests."
sources:
  - https://pve.proxmox.com/pve-docs/api-viewer/
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_tokens
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
  - https://github.com/proxmox/pve-docs/blob/master/certificate-management.adoc
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/API2/AccessControl.pm
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/AccessControl.pm
  - https://github.com/proxmox/pve-http-server/blob/master/src/PVE/APIServer/AnyEvent.pm
  - https://github.com/proxmox/pve-manager/blob/master/PVE/API2/Tasks.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE API with curl

Base URL: `https://<node>:8006/api2/json/`. Paths mirror `pvesh` (`pvesh get /nodes`).
Browse every endpoint in the API viewer.

## Option A: API token (automation, preferred)
```sh
TOKEN='automation@pve!ci=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
curl -s -H "Authorization: PVEAPIToken=$TOKEN" "https://pve01:8006/api2/json/cluster/resources?type=vm"
curl -s -X POST -H "Authorization: PVEAPIToken=$TOKEN" https://pve01:8006/api2/json/nodes/pve01/qemu/101/status/start
```
No CSRF token is needed with API tokens. Tokens with **privilege separation** (the default) are limited to the intersection of the user's ACLs and the ACLs granted to the token itself.

## Option B: ticket (user/password, interactive tools)
```sh
curl -s -d 'username=root@pam' --data-urlencode 'password=...' https://pve01:8006/api2/json/access/ticket
# copy data.ticket and data.CSRFPreventionToken from the JSON response
TICKET='<data.ticket>'
CSRF='<data.CSRFPreventionToken>'
# GET needs only the cookie
curl -s -b "PVEAuthCookie=$TICKET" https://pve01:8006/api2/json/nodes
# POST/PUT/DELETE need the CSRF header too
curl -s -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" -X POST \
     --data 'vmid=150' --data 'name=test150' --data 'memory=2048' --data 'net0=virtio,bridge=vmbr0' \
     https://pve01:8006/api2/json/nodes/pve01/qemu
```
Tickets expire after **2 hours**; the `password` parameter of `/access/ticket` can also be a valid ticket, which is how you renew one. With TFA enabled the first response carries `NeedTFA` and a signed challenge ticket; answer it by POSTing `/access/ticket` again with `tfa-challenge` set to that challenge string and the second-factor response in `password` (not `otp`). See the API viewer entry for `/access/ticket` for the exact response format.

## Tasks
Mutating calls return a UPID (`UPID:pve01:...`). Poll:
```sh
curl -s -H "Authorization: PVEAPIToken=$TOKEN" "https://pve01:8006/api2/json/nodes/pve01/tasks/$UPID/status"
```
`status: stopped` and `exitstatus: OK` means done.

## Gotchas
- 401 with token: header must be exactly `PVEAPIToken=user@realm!tokenid=secret`.
- 403: ACL missing on the path (`/vms/101`, `/storage/x`), or token privsep restricting it.
- Self-signed cert: copy `/etc/pve/pve-root-ca.pem` from a cluster node and pass it with `--cacert` instead of using `-k`.

## Verify
Script returns expected data with a least-privilege token; mutating call yields UPID with
exitstatus OK.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and pve-access-control source (`/access/ticket` API, ticket lifetime).

Confirmed: the API token header form and privilege separation semantics; ticket lifetime of 2 hours (`$ticket_lifetime = 3600 * 2` in the source); `password` accepts a valid ticket; `tfa-challenge` parameter and `NeedTFA` flag, with the TFA response going in `password` and not `otp`; CSRF prevention token returned in the ticket response; `/etc/pve/pve-root-ca.pem` as the cluster root CA. From the HTTP server source (proxmox/pve-http-server, AnyEvent.pm): cookie name `PVEAuthCookie`, token header scheme `PVEAPIToken`, and the `CSRFPreventionToken` request header. From pve-manager's tasks API: `/nodes/{node}/tasks/{upid}/status` exists with `status` of `running` or `stopped` and an `exitstatus`. Removed as unconfirmed: the `totp:<code>` prefix format, `jq` pipelines, and the wiki source link.

Method: documentation only; no commands were run.
