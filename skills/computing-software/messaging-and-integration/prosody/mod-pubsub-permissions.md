---
id: computing-software.messaging-and-integration.prosody.mod-pubsub-permissions
name: mod-pubsub-permissions
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, pubsub, permissions, roles, add-permissions]
level: advanced
status: docs-checked
description: "Who may create Prosody pubsub nodes: pubsub:create-node and pubsub:service-admin permissions, add_permissions per role, and server_user_role."
sources:
  - https://prosody.im/doc/modules/mod_pubsub
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_pubsub permissions

With the default authorization provider (`mod_authz_internal`):

- `pubsub:service-admin`: gets `default_admin_affiliation` (default `owner`).
- `pubsub:create-node`: may create nodes and becomes node owner.

Users of the parent VirtualHost (they default to the `prosody:registered` role on a component):

```lua
Component "pubsub.example.com" "pubsub"
  add_permissions = {
      ["prosody:registered"] = { "pubsub:create-node" }
  }
```

Everyone on the same Prosody instance (add `server_user_role`):

```lua
Component "pubsub.example.com" "pubsub"
  server_user_role = "prosody:registered"
  add_permissions = {
      ["prosody:registered"] = { "pubsub:create-node" }
  }
```

Anyone on the federated network:

```lua
  add_permissions = {
      ["prosody:guest"] = { "pubsub:create-node" }
  }
```

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_pubsub (two permissions, default_admin_affiliation default, the three permission configurations). Added the page's wording that parent VirtualHost users default to the prosody:registered role on a component; removed a generic verify line with an invented error.
Method: documentation only; no commands were run.
