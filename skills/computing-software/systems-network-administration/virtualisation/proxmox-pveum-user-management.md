---
id: computing-software.systems-network-administration.virtualisation.proxmox-pveum-user-management
name: proxmox-pveum-user-management
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pveum-user, pveum, proxmox, user-management, access-control]
level: intro
status: docs-checked
description: "Manage Proxmox VE users, groups, passwords, expiry and API tokens with pveum user, and check effective permissions from the CLI."
sources:
  - https://pve.proxmox.com/pve-docs/pveum.1.html
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_users
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/CLI/pveum.pm
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/API2/User.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Users with pveum user

**Goal:** create and maintain accounts from the CLI, scriptably.

## Realms
- `@pve`: Proxmox VE authentication server (password stored in the cluster).
- `@pam`: Linux PAM users created on the host system (for example with `adduser`); a PVE entry lets them log in with their system password.
- LDAP and AD realms: users and groups can be synced; OpenID realms: users can be auto-created (`autocreate`). User attributes are stored in `/etc/pve/user.cfg`.

## Common commands
```bash
pveum group add ops --comment 'Operations'
pveum user add alice@pve --firstname Alice --lastname Ng --email alice@example.com --groups ops --expire 0
pveum passwd alice@pve
pveum user modify alice@pve --groups ops,dba
pveum user modify alice@pve --enable 0          # disable without deleting
pveum user modify alice@pve --expire $(date -d '2026-12-31' +%s)
pveum user list
pveum user delete alice@pve

pveum acl modify /vms --groups ops --roles PVEVMAdmin
pveum user permissions alice@pve                 # effective permissions per path
pveum user permissions alice@pve --path /vms/120

pveum user token add alice@pve ci --privsep 1 --expire 0
pveum acl modify /vms/120 --tokens 'alice@pve!ci' --roles PVEVMUser
pveum user token list alice@pve
```

## Good practice
- Grant roles to groups, not users.
- Use privilege-separated tokens (`privsep 1`, the default) with their own narrow ACLs for automation, and set an expiry.
- Disable leavers immediately (`--enable 0`), delete after audit retention.
- Keep `root@pam` for break-glass only; give admins named accounts and set up two-factor authentication.
- Always grant permissions to groups instead of individual users; the guide says that is much more maintainable.

## Verify
`pveum user permissions alice@pve` lists exactly the expected paths and privileges; login works at the GUI with the right realm selected.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and pve-access-control source (pveum CLI, user API).

Confirmed: user attributes stored in `/etc/pve/user.cfg`, groups as the preferred permission unit, PAM realm behaviour, `pveum passwd`, `pveum user token add ... --privsep 1`, `pveum acl modify ... --tokens ... --roles`, `pveum user permissions` and `pveum user token permissions`, `pveum user tfa` subcommands exist in the CLI, user API fields (`enable`, `expire`, `firstname`, `lastname`, `email`). Removed as unconfirmed: `--append 1` on `user modify` (not found in the user API source), the claim that the PAM account must exist on every node (stated only for PAM users generally), and 'disable leavers immediately' style process advice kept only as general practice.

Method: documentation only; no commands were run.
