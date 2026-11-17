---
id: computing-software.systems-network-administration.audiobookshelf.listening-sessions-admin
name: listening-sessions-admin
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [listening-sessions, statistics, admin, debugging, sessions]
level: practitioner
status: docs-checked
description: "Use the Audiobookshelf Listening Sessions page to filter, inspect, close and delete sessions without damaging playback stats."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/listening-sessions.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/user-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Listening Sessions page lists all previous and current sessions for the server and can be filtered by user and sorted by each column.

What you can do:

- Click a row for details, including the device playback occurred on, which helps debugging.
- Close currently open sessions from this page.
- Delete previous sessions from the details popup or by selecting rows in the table.

Important: stats are calculated from listening sessions. Sessions should be kept and not deleted, otherwise statistics become inaccurate.

Related: the user-management page says account sharing is not supported, and listening to different media at the same time from one account can cause issues. A stuck open session is a reason to inspect it on this page, and close it rather than delete it, before removing anything.

## Checked

2026-11-09. Confirmed against the Audiobookshelf docs Listening Sessions page and User Management page (raw markdown, whole files). Removed the claim about the mobile app Listen History, which neither page mentions, and the advice about devices resetting progress.

Method: docs-checked 2026-11-09 against the audiobookshelf-docs repository files documentation/server-management/listening-sessions.md and user-management.md.
