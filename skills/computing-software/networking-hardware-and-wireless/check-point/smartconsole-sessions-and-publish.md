---
id: computing-software.networking-hardware-and-wireless.check-point.smartconsole-sessions-and-publish
name: smartconsole-sessions-and-publish
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, smartconsole, publish, sessions]
level: practitioner
status: draft
description: "Work with SmartConsole sessions: publish, discard, session locks, and see who changed what in the audit view."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/latest/APIs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SmartConsole sessions, publish and discard

- Every SmartConsole login creates a database session. Edits are held privately until you click **Publish**; other administrators do not see your changes (they see locks on objects you modified). **Discard** drops the edit session.
- Locked objects: a lock icon shows an object is in someone else's unpublished session. The owner can publish/discard, or a superuser can take over via Manage & Settings > Sessions > "View sessions" and **Discard** or **Disconnect** the session.
- Always add a name and description to the session (the "Session" button) before publishing. Everything shows in **Logs & Monitor > Audit Logs** (the audit log of the management, `Session`, `Object`, `Operation`), searched by `Administrator` or `Object`.
- From the command line:
```
mgmt_cli -r true show sessions details-level full --format json
mgmt_cli -r true show session uid "<uid>"
mgmt_cli -r true discard uid "<uid>"
mgmt_cli login user admin password '...' > id.txt ; mgmt_cli publish -s id.txt
```
- A session with unpublished changes counts against object locks, and a stale session of a crashed client can block others until its timeout (`session-timeout`, default 600 s in `login`; confirm for SmartConsole).
- "Install Policy" always uses published data. Publish before installing, and note that revert to a prior revision is possible from Manage & Settings > Revisions.
- Gotcha: closing SmartConsole with changes pending prompts to save, publish, or discard; keep sessions short to avoid "locked by" conflicts.

Verify: open **Sessions** in the SmartConsole bottom pane; after publish the revision number increments and the audit log shows the publish.
