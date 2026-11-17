---
id: computing-software.systems-network-administration.virtualisation.proxmox-api-tokens-and-pvesh
name: proxmox-api-tokens-and-pvesh
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proxmox-api, api-token, pvesh, privilege-separation, terraform-proxmox, rest-api, automation, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Automate Proxmox VE: create privilege-separated API tokens, call the REST API with curl, explore it with pvesh, and scope tokens to the least privilege needed."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_tokens
  - https://pve.proxmox.com/pve-docs/api-viewer/
  - https://pve.proxmox.com/pve-docs/pvesh.1.html
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pvesh.adoc
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/API2/ACL.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox API tokens and pvesh

**Goal:** scripts and tools use narrowly scoped, revocable tokens instead of a person's
password, and you can find any API call quickly.

## Create a token
```sh
pveum user add automation@pve --comment "CI automation"
pveum user token add automation@pve terraform --privsep 1 --expire 0
# the secret is displayed only once: store it in a vault
pveum acl modify /pool/ci --tokens 'automation@pve!terraform' --roles PVEVMAdmin
pveum acl modify /storage/local-lvm --tokens 'automation@pve!terraform' --roles PVEDatastoreUser
```
Token types: with **privilege separation** (the default for new tokens) the token needs explicit ACLs and its effective permissions are the intersection of user and token permissions; with full privileges the token has the same permissions as its user, so disable separation only when the integration really needs that. Set `expire` (Unix epoch seconds) so abandoned automation stops working. API tokens cannot access the endpoints for the VM or system console.

## Call the API
```sh
curl -s -H 'Authorization: PVEAPIToken=automation@pve!terraform=<secret>' \
  https://pve1.<domain>:8006/api2/json/nodes
curl -s -X POST -H 'Authorization: PVEAPIToken=automation@pve!terraform=<secret>' \
  https://pve1.<domain>:8006/api2/json/nodes/pve1/qemu/120/status/start
```
The header value has the form `PVEAPIToken=USER@REALM!TOKENID=UUID`.

## pvesh (on a node, as root, same API locally)
```sh
pvesh get /nodes
pvesh get /nodes/pve1/qemu/120/config
pvesh usage cluster/options -v
```
`pvesh` calls API functions directly without the REST server and is allowed for `root` only; it takes the usual output options (see `pvesh help`). The online **API viewer** (`/pve-docs/api-viewer/`) documents every path and parameter, and the permissions each method requires.

## Tool scopes
Give each tool only the roles it needs on the narrowest path. The guide's own example is a monitoring token:
```sh
pveum user token add joe@pve monitoring --privsep 1
pveum acl modify /vms --tokens 'joe@pve!monitoring' --roles PVEAuditor
```
`PVEAuditor` is read-only. See each API method's required permissions in the API viewer before choosing roles for other tools.

## Verify
`pveum user token permissions automation@pve terraform` shows only the intended paths; a
call outside scope returns 403; the secret exists only in the vault.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and pve-access-control source (ACL API: parameters `users`, `groups`, `tokens`, `roles`, `propagate`).

Confirmed: token types and the default privilege separation, `expire` as a Unix timestamp, the secret shown once, the `PVEAPIToken=USER@REALM!TOKENID=UUID` header form, console endpoints unavailable to tokens, `pveum user token add ... --privsep 1`, `pveum acl modify ... --tokens ... --roles ...`, `pveum user token permissions`, pvesh examples and root-only restriction, API viewer. Removed as unconfirmed: the claims that tokens bypass TFA and that any node serves the whole cluster API with a load balancer, `pvesh ls`/`create ... snapshot`/`--output-format` examples beyond the guide, the third-party tool scope table, and the `jq` pipeline.

Method: documentation only; no commands were run.
