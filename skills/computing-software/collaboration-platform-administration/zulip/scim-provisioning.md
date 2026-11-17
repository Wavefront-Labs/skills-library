---
id: computing-software.collaboration-platform-administration.zulip.scim-provisioning
name: scim-provisioning
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [scim, scim-config, bearer-token, user-provisioning]
level: practitioner
status: docs-checked
description: "Enable beta SCIM user provisioning in Zulip with a SCIM_CONFIG block, bearer_token, scim_client_name, guest options and custom profile field mapping."
sources: ["https://zulip.readthedocs.io/en/latest/production/scim.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SCIM provisioning

Zulip has beta SCIM support for creating and deprovisioning users. The third-party IdP is the SCIM client; your server is the service provider. Group synchronisation is not supported.

Server setup:

1. Choose an internal client name, such as `okta`.
2. Add to `/etc/zulip/settings.py`:

```
SCIM_CONFIG = {
    "subdomain": {
        "bearer_token": "<secret token>",
        "scim_client_name": "okta",
        "name_formatted_included": False,
    }
}
```

Generate the token with a secure generator, for example `apg -m20`. The outer key is shown as `"subdomain"` in the example. `name_formatted_included` states whether the IdP sends `name.formatted`; it must be False for Okta.

3. Restart with `scripts/restart-server`.
4. In the IdP, supply `Bearer <secret token>` as the API token. Requests then carry an `Authorization: Bearer ...` header.

Docker deployments set this through the `SETTING_SCIM_CONFIG` environment variable.

Options in the client dict:

- `"create_guests_without_streams": True` creates guest accounts without subscribing them to initial channels.
- `"custom_profile_field_map"` maps Zulip fields to SCIM attributes. A field is named by its lowercase label with underscores, e.g. `"phone_number": "phoneNumber"`. The fields must already exist in organisation settings.

## Checked

2026-11-08. Checked: read against the Zulip SCIM page (docs/production/scim.md, read in full). Removed: the claim that the outer key is the organization subdomain, which the page does not state.

Method: documentation only; no commands were run.
