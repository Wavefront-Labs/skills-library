---
id: computing-software.systems-network-administration.apache-guacamole.connection-sharing
name: connection-sharing
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, connection-sharing, sharing-profile, share-link, read-only-sharing, shadowing, join]
level: practitioner
status: docs-checked
description: "Share a live Guacamole session by link using sharing profiles: required permissions, what ends the share, database-only support."
sources:
  - https://guacamole.apache.org/doc/gug/using-guacamole.html
  - https://guacamole.apache.org/doc/gug/administration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection sharing

Sharing needs server support: of the extensions shipped with Guacamole, only the database authentication extension implements enough of the extension API. It can run alongside other authentication extensions, handling only connection storage and permissions.

Admin side:
1. Expand a connection in the connection list (Settings, Connections, or the user editor) and click the **New Sharing Profile** placeholder under it. There is no top-level New Sharing Profile button.
2. Set the profile name and parameters. Not all connection parameters are available for a sharing profile; the profile's parameters decide the access given to link users (for example read-only).
3. Grant users or groups read access to both the connection and the sharing profile; users with access to both can generate share links.

User side:
1. In an active session open the Guacamole menu (Ctrl+Alt+Shift).
2. Use the **Share** menu next to your username; picking an option generates a unique link. The sharing profile name is the option's label.
3. Anyone with the link, even without a Guacamole account, gets temporary access restricted by the chosen profile.

Lifetime: the link is valid only until the owner disconnects; then it stops working and people sharing are disconnected.

With JSON auth, a connection may carry an `id` so others can `join` it (apache-guacamole.json-auth).

Security: a link is a credential for that session; send it only to the intended person.

Verify: open the link in a private window; both views show the same desktop.

## Checked

2026-11-08. Read the whole of using-guacamole.html and administration.html. Confirmed database-extension-only support, placeholder-based creation of sharing profiles, restricted parameters, the need for read access to both connection and profile, the Share menu, account-less link users and the lifetime rule. Removed the guacamole_sharing_profile_parameter table name and the "read-only is the usual one" assertion (not on these pages; read-only is given only as an example). The json-auth cross-reference was not checked here.
Method: documentation only; no commands were run.
