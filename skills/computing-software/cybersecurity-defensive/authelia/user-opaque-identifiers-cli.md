---
id: computing-software.cybersecurity-defensive.authelia.user-opaque-identifiers-cli
name: user-opaque-identifiers-cli
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, subject-identifier, sector-identifier, pairwise, opaque-identifiers, cli]
level: sme
status: docs-checked
description: "Understand Authelia's UUID subject identifiers, pairwise sector_identifier_uri behaviour and how to pre-generate identifiers in bulk."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/clients/
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_user_identifiers_generate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia issues UUID version 4 subject identifiers (`sub`) for OpenID Connect users. By default the public subject type applies: the same user gets the same `sub` at every client.

Setting `sector_identifier_uri` on a client switches it to the pairwise subject type:

- Clients with no sector identifier all share one `sub` per user.
- Clients sharing a sector identifier share a `sub` for a user, which differs from the public one and from other sectors.
- The value must be absent or an absolute `https` URL serving a JSON array of strings. Every URI in it must exactly match a registered `redirect_uris` entry of this client (other clients' URIs may also appear).

Changing it changes the `sub` of every token for the client, so relying parties will treat all users as new. Pairwise identifiers matter for privacy when third parties you do not control use your provider. For a homelab or a business with no external relying party, the documentation sees very little benefit.

Bulk generation:

```bash
authelia storage user identifiers generate --users john,mary --services openid \
  --sectors=",example.com,test.com" --config config.yml
```

`--users` lists the users, `--services` the services (valid value: `openid`, the default) and `--sectors` the sectors to generate identifiers for.

Check: after changing `sector_identifier_uri` for a client, confirm the relying party now sees a different `sub` for the same user.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Clients configuration page (sector_identifier_uri requirements, UUID v4 subjects, public versus pairwise behaviour, privacy guidance) and the `authelia storage user identifiers generate` CLI reference (--users, --services, --sectors, example). Removed: the add, export and import subcommands and the claim about the empty sector entry, neither shown on the pages read.

Method: documentation only; no commands were run.
