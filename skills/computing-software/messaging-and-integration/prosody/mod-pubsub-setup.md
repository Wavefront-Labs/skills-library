---
id: computing-software.messaging-and-integration.prosody.mod-pubsub-setup
name: mod-pubsub-setup
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, pubsub, component, nodes, autocreate]
level: practitioner
status: docs-checked
description: "Set up mod_pubsub as a Prosody component: admins, default_admin_affiliation owner, autocreate_on_subscribe/publish, pubsub_max_items 256 and summary templates."
sources:
  - https://prosody.im/doc/modules/mod_pubsub
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_pubsub setup

```lua
Component "pubsub.example.com" "pubsub"
```

| Option | Default |
|---|---|
| `admins` | `{}` (global admins are admins automatically) |
| `default_admin_affiliation` | `"owner"` |
| `autocreate_on_subscribe` | false |
| `autocreate_on_publish` | false |
| `pubsub_max_items` | 256 (limit on how many items nodes can be configured to store) |
| `pubsub_summary_templates` | no default stated; example below |

`autocreate_on_subscribe` and `autocreate_on_publish` control whether non-existent nodes are created automatically when someone subscribes or publishes.

Nodes with the `pubsub#include_body` setting true can have a plain text version of the payload generated from a template in util.xtemplate format. The template is selected by the `pubsub#type` config option; if unset, the namespace of the payload is used. Available node properties: `@pubsub:node`, `@pubsub:title`, `@pubsub:description`.

```lua
pubsub_summary_templates = {
    ["http://www.w3.org/2005/Atom"] = "{summary|or{{author/name|and{{author/name} posted }}{title}}}";
}
```

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_pubsub (component line, all listed options and defaults, template selection and properties). Replaced the invented "none" default for pubsub_summary_templates and removed a generic verify line.
Method: documentation only; no commands were run.
