---
id: computing-software.messaging-and-integration.prosody.mod-server-contact-info
name: mod-server-contact-info
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, contact-info, xep-0157, abuse, discovery]
level: intro
status: docs-checked
description: "mod_server_contact_info in Prosody: advertise abuse, admin, feedback, sales, security and support addresses (XEP-0157) through the contact_info table."
sources:
  - https://prosody.im/doc/modules/mod_server_contact_info
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_server_contact_info

Advertises contact addresses for your service. The single option `contact_info` is a table where each field is a list of URIs. With no config, the module exposes the configured `admins`.

Address forms: `xmpp:user@example.com`, `mailto:user@example.com`, `xmpp:room@muc.example.com?join`.

```lua
modules_enabled = { "server_contact_info"; }
contact_info = {
  abuse = { "mailto:abuse@example.com", "xmpp:abuse@example.com" };
  admin = { "mailto:admin@example.com" };
  security = { "xmpp:security@example.com" };
  support = { "xmpp:support@muc.example.com?join" };
}
```

The page's example shows all possible fields: abuse, admin, feedback, sales, security, support. Each string should be a URI (the page also uses `http://` URLs for feedback and support).

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_server_contact_info (XEP-0157, contact_info table, URI forms, field names, admins fallback). Removed a generic verify line.
Method: documentation only; no commands were run.
