---
id: computing-software.systems-network-administration.virtualisation.proxmox-authentication-realms
name: proxmox-authentication-realms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pveum, pve-realm, pve-ldap, active-directory, openid-connect, realm-sync, pam-realm, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Configure Proxmox VE authentication realms: PAM vs PVE, LDAP and Active Directory with group sync, OpenID Connect SSO, default realm, and keeping root@pam as break-glass."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_authentication_realms
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/Auth/LDAP.pm
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/Auth/AD.pm
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/Auth/Plugin.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE authentication realms

**Goal:** admins log in with directory accounts (ideally SSO with MFA), groups come from the
directory, and local root is reserved for emergencies.

## Realm types
| Realm | Users live in | Notes |
|---|---|---|
| `pam` | Linux users on the host | Added by default and cannot be removed; `root@pam` lives here |
| `pve` | PVE's own user DB (`/etc/pve/priv/shadow.cfg`, SHA-256 hashed) | Created by default; users can change their own password in the GUI |
| `ldap` | Any LDAP server | `base_dn`, `user_attr`, `server1`, optional `server2` fallback, `bind_dn` |
| `ad` | Microsoft Active Directory | `domain`, `server1`, optional `server2`, `port`, bind user usually required |
| `openid` | OpenID Connect provider | Browser login through the provider |

## AD realm with sync
```sh
pveum realm add corp --type ad --domain corp.example --server1 dc1.corp.example \
  --server2 dc2.corp.example --mode ldaps --bind_dn 'CN=svc-pve,OU=Svc,DC=corp,DC=example' \
  --password '<from-vault>' --base_dn 'DC=corp,DC=example' \
  --filter '(memberOf=CN=PVE-Users,OU=Groups,DC=corp,DC=example)' \
  --group_filter '(cn=PVE-*)' --sync-defaults-options 'scope=both,enable-new=1,remove-vanished=acl;entry;properties'
pveum realm sync corp
```
Option names use underscores (`bind_dn`, `base_dn`, `group_filter`); `mode` is `ldap`, `ldaps` or `ldap+starttls`. A sync writes users and groups to `/etc/pve/user.cfg`; groups get `-<realm>` appended to their names. `remove-vanished` takes `acl`, `entry` and `properties`; `scope` is `users`, `groups` or `both`; `enable-new` defaults to true; `dry-run` previews a sync. The bind password is stored under `/etc/pve/priv/realm/<realm>.pw`. To verify certificates set `capath` and `verify`.
Grant permissions to the synced groups (for example `PVE-Admins-corp`).

## OpenID Connect
Add a realm of type OpenID Connect with `issuer-url` (PVE uses OpenID Connect Discovery), `client-id`, optional `client-key`, `username-claim` (`subject`, `username` or `email`), `autocreate`, and optionally `groups-claim`. See the OpenID realm skill for details.

## Hygiene
- Choose the default realm for the login page in the realm settings.
- `root@pam`: use a long random password kept in a vault and protect it with two-factor authentication; use it for break-glass.
- Remove or disable departed users; `remove-vanished` can remove synced users that disappear from the directory.

## Gotchas
- Use an encrypted LDAP connection (`mode ldaps` or `ldap+starttls`) with certificate verification (`capath`, `verify`).
- Redirect URI registration for OpenID is covered in the OpenID realm skill.
- A realm outage blocks logins for its users; keep an emergency account in a realm that does not depend on an external server.

## Verify
A directory user logs in, sees only what their group allows; `pveum user list` shows synced
users with the right groups; root@pam login still works with TFA.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and pve-access-control source (Auth/LDAP.pm, AD.pm, OpenId.pm, Plugin.pm).

Confirmed: realm types and their descriptions, `/etc/pve/priv/shadow.cfg`, `base_dn`, `user_attr`, `bind_dn`, `server1`/`server2`, `filter`, `group_filter`, `mode` enum (`ldap`, `ldaps`, `ldap+starttls`), `sync-defaults-options` with `scope`, `enable-new`, `remove-vanished` (acl, entry, properties), `dry-run`, `pveum realm sync`, bind password file path, `capath` and `verify`, group suffix `-<realm>`, OpenID options and `username-claim` values. Wrong in the draft: the hyphenated option names `--bind-dn`, `--base-dn` and `--group-filter` (the properties use underscores). Removed as unconfirmed: the list of named identity providers, 'LDAPS recommended' wording tied to AD, the sync-job schedule claim ('PVE 8+') and the `preferred_username` claim value.

Method: documentation only; no commands were run.
