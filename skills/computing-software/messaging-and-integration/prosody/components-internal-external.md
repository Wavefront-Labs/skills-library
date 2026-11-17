---
id: computing-software.messaging-and-integration.prosody.components-internal-external
name: components-internal-external
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, components, xep-0114, muc, configuration]
level: intro
status: docs-checked
description: "Prosody Component blocks: internal components named after a plugin versus external XEP-0114 components with component_secret, and where modules_enabled goes."
sources:
  - https://prosody.im/doc/components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internal vs external components

Components provide extra services (chatrooms, gateways, uploads) at their own domain.

Internal component: name the Prosody plugin after the domain.

```lua
Component "groups.example.com" "muc"
modules_enabled = {
    "muc_mam";
}
```

Modules for it go in that component's own `modules_enabled`, not the global one. Common internal components: mod_http_file_share, mod_muc, mod_proxy65, mod_pubsub.

External component (XEP-0114): omit the plugin, set a secret.

```lua
Component "telegram.example.org"
         component_secret = "mysecretcomponentpassword"
```

Domain and secret must match exactly in Prosody and in the component's own config.

Discovery: a direct subdomain of a VirtualHost (`groups.example.com` under `example.com`) is linked automatically; `groups.xmpp.example.com` is not, so list it in `disco_items`.

DNS records and certificates are only needed if remote servers must reach the component over s2s.

Verify: `prosodyctl check config` passes and the component appears in service discovery of its parent host.

## Checked

2026-11-04. Read the Prosody components page: internal versus XEP-0114 external components, per-component modules_enabled for modules such as muc_mam, the common internal components, domain and secret matching, automatic linking of direct subdomains with disco_items for others, and DNS and certificates only needed for s2s all match. Nothing removed.

Method: documentation only; no commands were run.
