---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-users-tokens-and-acls
name: pbs-users-tokens-and-acls
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-acl, proxmox-backup-server, api-tokens, rbac, pbs, least-privilege]
level: practitioner
status: docs-checked
description: "Set up Proxmox Backup Server users, realms, API tokens and ACLs: built-in roles, token permission intersection, two-factor limits and backup group ownership."
sources:
  - https://pbs.proxmox.com/docs/user-management.html
  - https://pbs.proxmox.com/docs/backup-client.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS users, tokens and ACLs

**Goal:** each client and admin has only the access it needs, so a compromised client token cannot do more than its role allows.

## Users and realms
Realms: `pam` (existing Linux users on the host), `pbs` (PBS-internal, hashed passwords), `openid`, `ldap`, `ad`. After installation there is one user, `root@pam`, the superuser with full rights; the manual recommends adding other users with fewer privileges. New users and tokens have no permissions until you grant them.
```sh
proxmox-backup-manager user create john@pbs --email john@example.com
proxmox-backup-manager user generate-token john@pbs client1     # prints the secret once
proxmox-backup-manager user list-tokens john@pbs
```
Token ID format is `user@realm!tokenname` (here `john@pbs!client1`). The secret is shown only once and must be saved. `user update --enable 0` disables a user; `user remove` deletes one. Tokens give easy revocation and let you limit each client within the user's permissions.

## Roles (built-in only; custom roles are not possible)
| Role | Described as |
|---|---|
| NoAccess | nothing is allowed |
| Admin | anything on the assigned object path |
| Audit | view status and configuration, no changes |
| DatastoreAdmin | anything on existing datastores |
| DatastoreAudit | view datastore metrics, settings and list content, but not read the actual data |
| DatastoreReader | inspect a datastore's or namespace's content and do restores |
| DatastoreBackup | back up and restore owned backups |
| DatastorePowerUser | back up, restore and prune owned backups |
| RemoteAdmin / RemoteAudit / RemoteSyncOperator | anything on remotes / view remote settings / read data from a remote |
| TapeAdmin / TapeAudit / TapeOperator / TapeReader | anything tape / view tape state / tape backup and restore without config changes / read tape config and media |
Pruning needs the `Datastore.Prune` privilege and also requires backup ownership.

## ACLs
```sh
proxmox-backup-manager acl update /datastore/store1 DatastoreBackup --auth-id 'john@pbs!client1'
proxmox-backup-manager acl list
proxmox-backup-manager user permissions 'john@pbs!client1' --path /datastore/store1
```
Paths are filesystem-like: `/datastore`, `/datastore/{store}`, `/datastore/{store}/{ns}`, `/remote`, `/remote/{remote}/{storename}`, `/system/network`, `/tape/`, `/access/users`. Permissions propagate down the tree by default, and deeper entries replace inherited ones. ACLs are stored in `/etc/proxmox-backup/acl.cfg`. Use the `/datastore/{storename}` form, not the mount path.

## API token permissions
A token's permissions come from ACL entries naming the token itself, then are intersected with its user's permissions. So tokens need their own ACL entries and can never do more than their user. A user can always configure privileges for their own tokens.

## Ownership
By default the owner of a backup group is the user who created it (root@pam for sync jobs), and another user cannot back up into that group. Change it with a user holding `Datastore.Modify` on the datastore:
```sh
proxmox-backup-client change-owner vm/103 john@pbs
```
The web UI has the same action under the datastore's Content tab. `Datastore.Backup` provides read and verify rights only on groups owned by the user or one of its tokens.

## Two-factor authentication
Supported second factors: TOTP, WebAuthn and single-use recovery keys (one set per user). 2FA is implemented only for the web interface; use API tokens for non-interactive use such as adding PBS to Proxmox VE as storage. After 8 failed TOTP attempts the user's TOTP factors are disabled (a recovery key unlocks them); WebAuthn and recovery keys allow 100 tries, then all second factors are blocked for an hour. An admin can unlock with `proxmox-backup-manager user tfa unlock <user>`.

## Checked
2026-11-07. Read in full: PBS User Management page (user configuration, API tokens, access control with privileges and roles, inheritance, acl.cfg, token permissions, effective permissions, 2FA, realms and LDAP/AD sync). Backup-client page: only the "Changing the Owner of a Backup Group" section. Corrections: DatastoreBackup does not prune (only DatastorePowerUser, for owned backups, and prune needs ownership); DatastorePowerUser is for owned backups, not any group; ACL paths for remotes and system were `/remote/{remote}` and `/system` and are now the documented forms; "unless privilege separation is off" removed (not on the page). Removed: the `--password 'xxx'` example, "RemoteSyncOperator: run sync", the hardening items "do not give PVE root@pam" and "prune/GC run server-side so clients need no delete rights", and the invented Verify step with `proxmox-backup-client forget`.
Method: documentation only; no commands were run.
