---
id: computing-software.systems-network-administration.apache-guacamole.managing-sessions-history
name: managing-sessions-history
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, active-sessions, kill-sessions, connection-history, administration, cidr-filter, audit]
level: practitioner
status: docs-checked
description: "Use Guacamole's admin pages to list and kill active sessions and search connection history, with CIDR filtering and recordings."
sources:
  - https://guacamole.apache.org/doc/gug/administration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active sessions and history

The admin interface is provided by the database authentication extensions (the only officially supported modules with it).

Active sessions (Settings, Active Sessions):
- Shows username, duration, source IP and connection name.
- Tick sessions and press **Kill Sessions** to disconnect them immediately.
- The filter takes search terms (quote terms containing spaces) and CIDR blocks for IP ranges, IPv4 or IPv6, such as 10.0.0.0/8.

Connection history (Settings, History):
- Lists recent connections with user, start time, duration and whether a recording is available.
- A recording is viewable here only if the connection was configured to record and to store it for in-browser playback (apache-guacamole.recording-playback).
- Only the most recent records show at first; page through them. Filters apply only after you click **Search**.

Tip: to block a user, set "Login disabled" (apache-guacamole.user-and-group-management).

Verify: start a session as a test user and see it listed; kill it and the user's tab disconnects.

## Checked

2026-11-08. Read the whole of the administrative interface chapter (administration.html) and confirmed the session table columns, Kill Sessions, filter quoting, CIDR filtering for IPv4 and IPv6, history columns, the recording condition, the Search button behaviour and Login disabled. Removed the claim that source IPs need a proxy forwarding the client address, and the Logs column name (the page only says whether a recording is available).
Method: documentation only; no commands were run.
