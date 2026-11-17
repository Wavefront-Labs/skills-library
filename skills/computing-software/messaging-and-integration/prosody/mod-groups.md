---
id: computing-software.messaging-and-integration.prosody.mod-groups
name: mod-groups
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, shared-roster, groups, contacts]
level: practitioner
status: docs-checked
description: "mod_groups in Prosody: shared roster groups from a text file via groups_file, ini-like format with optional nicknames, and limits of server-side groups."
sources:
  - https://prosody.im/doc/modules/mod_groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_groups

Creates virtual groups of users that automatically see each other in their contact lists. The shared groups are sent to the user along with their usual roster without overriding or permanently adding the contacts, and users need not authorise the contacts.

```lua
modules_enabled = { "groups"; }
groups_file = "/path/to/sharedgroups.txt"
```

`groups_file` defaults to nil: the path to a text file where the shared groups are defined. If the path is empty, mod_groups does nothing. Make sure Prosody has sufficient permissions to read the file.

File syntax is similar to ini files. Groups are written in brackets, like `[This Group]`, followed by the JIDs in the group. Optionally a nickname follows an equals sign:

```
[Support Team]
support@example.com
john.doe@example.com

[Development Team]
hardworkingdeveloper@example.net=Joe Coder
other.dev@example.com=Mel
```

If no name is given it is up to the user's client to find a suitable name (for example from the contact's vcard/profile).

Limits: currently the shared groups can only be modified by changing the configuration. Changes a user makes to shared group contacts in their client are lost the next time they log in. Server-side modifications may not be visible to logged-in users unless they log out and back in.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_groups (groups_file default and meaning, file syntax, nickname rule, limits). Used the page's example contents and removed a generic verify line.
Method: documentation only; no commands were run.
