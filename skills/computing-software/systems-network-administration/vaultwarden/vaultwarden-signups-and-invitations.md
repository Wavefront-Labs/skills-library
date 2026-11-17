---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-signups-and-invitations
name: vaultwarden-signups-and-invitations
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, signups-allowed, registration, invitations, domains-whitelist, signups-verify]
level: practitioner
status: docs-checked
description: "Control who can register on Vaultwarden using SIGNUPS_ALLOWED, SIGNUPS_DOMAINS_WHITELIST and SIGNUPS_VERIFY, and how invitations still work with signups disabled."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Disable-registration-of-new-users"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden signups and invitations

By default anyone who can reach the instance can register. Set `SIGNUPS_ALLOWED=false` to stop that:

```
docker run -d --name vaultwarden -e SIGNUPS_ALLOWED=false -v /vw-data/:/data/ -p 80:80 vaultwarden/server:latest
```

- `SIGNUPS_ALLOWED` is ignored when `SIGNUPS_DOMAINS_WHITELIST` is set.
- `SIGNUPS_DOMAINS_WHITELIST` restricts registration to email addresses in the listed domain or comma-separated domains.
- `SIGNUPS_VERIFY=true` requires email verification before a new user can log in, which stops registrations with fake addresses on an allowed domain (needs working SMTP).
- Invitations are separate: with signups disabled, organization owners and admins can still invite users, and the admin page can invite anyone regardless of these restrictions. Invitation links need `DOMAIN` set and expire after 5 days. Invitations can be turned off in the admin panel (see the wiki's Disable invitations page for the variable).

A typical private setup: create accounts first, then disable signups and use admin-page invitations for additions.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Disable-registration-of-new-users.
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
