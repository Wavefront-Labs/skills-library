---
id: computing-software.systems-network-administration.virtualisation.proxmox-openid-connect-realm
name: proxmox-openid-connect-realm
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-openid, openid-connect, sso, proxmox, authentication]
level: practitioner
status: docs-checked
description: "Configure an OpenID Connect realm in Proxmox VE with Keycloak, Entra ID or Authentik: client settings, redirect URL, username and groups claims, autocreate."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_openid
  - https://pve.proxmox.com/pve-docs/pveum.1.html
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/Auth/OpenId.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenID Connect realm

**Goal:** single sign-on to the Proxmox VE GUI through your identity provider, with group-based permissions.

## Identity provider side
- Create an OIDC client for PVE at the provider; PVE takes a `client-id` and an optional `client-key`.
- Redirect URI: register the URL users open to reach the PVE web interface, for example `https://pve.example.com:8006`; check your provider's rules for exact matching.
- Include a groups claim (in the ID token or userinfo response) if you want group mapping; its value must be a list of strings.

## Proxmox side
```bash
pveum realm add sso --type openid \
  --issuer-url https://idp.example.com/realms/infra \
  --client-id proxmox --client-key '<secret>' \
  --username-claim username \
  --scopes 'email profile' \
  --autocreate 1 \
  --groups-claim groups --groups-autocreate 1 --groups-overwrite 1 \
  --default 1
```
GUI: Datacenter -> Permissions -> Realms -> Add -> OpenID Connect Server.

Users appear as `<claim value>@sso`. All users need an entry in the PVE user configuration: add them manually or use `autocreate`. Group names from the claim are suffixed with `-<realm>` (group `my-openid-group` in realm `oidc` becomes `my-openid-group-oidc`); groups missing in PVE are ignored unless `groups-autocreate` is set. Assign ACLs to the synced groups, for example `pveum acl modify / --groups admins-sso --roles Administrator` for a claim group `admins` in realm `sso`.

## Username claim
`subject` (the default) yields usernames like `DGH76OKH34BNG3245SB@<realm>`: unique but hard to read. `username` is preferred when the provider supplies it and guarantees uniqueness; `email` also gives readable names, but only use it if the provider guarantees uniqueness. Changing the claim later changes the generated usernames, so decide before users are created (the guide does not describe a migration).

## Gotchas
- `issuer-url` is the authorization server URL; PVE uses OpenID Connect Discovery to configure the rest, and https is strongly recommended over http.
- Providers that do not support the userinfo endpoint (for example ADFS) need `query-userinfo` disabled.
- Groups whose names contain characters not allowed in PVE group IDs are skipped with a log warning.
- Keep `root@pam` (protected with two-factor authentication) as break-glass for provider outages.
- `groups-overwrite` removes all of the user's existing PVE groups before adding the ones from the claim (default: groups are appended).

## Verify
Log out, choose the `sso` realm, log in through the IdP; `pveum user list` shows the new user and its synced groups.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and pve-access-control source (Auth/OpenId.pm).

Confirmed: options `issuer-url`, `client-id`, `client-key` (optional), `autocreate`, `username-claim` (`subject`, `username` or `email`), `groups-claim`, `groups-autocreate`, `groups-overwrite` semantics, group `-<realm>` suffix, `query-userinfo` and ADFS note, invalid group characters, `scopes` option (default `email profile` in the source), OpenID Discovery and https recommendation. Wrong in the draft: `--username-claim preferred_username` is not one of the documented values (`username` is). Removed as unconfirmed: the exact-match trailing-slash and clock-skew remarks, `openid` as an explicit scope, the redirect-URI exact-match claim and the claim that the username claim cannot be changed without re-creating users (replaced by a cautious statement), and the `--default 1` and GUI-path details.

Method: documentation only; no commands were run.
