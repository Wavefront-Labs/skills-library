---
id: computing-software.networking-hardware-and-wireless.opnsense.dashboard-widgets
name: dashboard-widgets
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [dashboard, widgets, lobby]
level: intro
status: docs-checked
description: "Customize the OPNsense dashboard: default widgets, edit mode buttons, saving layouts and per-user storage."
sources: ["https://docs.opnsense.org/manual/dashboard.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dashboard widgets

The dashboard is the landing page after login and is also reachable at Lobby > Dashboard. It is built from widgets. Defaults: System Information (version, update state), Memory, Disk, CPU, Announcements from the project, Gateways, Interface Statistics (packets, bytes, errors per interface), Firewall (events logged since the page loaded, expandable to a live log), Traffic Graph and Services (shows configured services with start, restart and stop controls).

Top-right buttons: Edit dashboard (pencil) unlocks the layout so you can move, resize, remove or configure widgets; Add widget (plus) opens the list of available widgets, click one to add it; Restore default layout discards all modifications; Save makes the changes persistent. Without Save, edits are lost when the page reloads.

While editing, each widget gets an Edit pencil (only if that widget is configurable) and a Remove cross. Outside edit mode many widgets show a link to the matching configuration page. Resize by dragging any corner.

The layout is stored per user, so each admin can have a different dashboard. If you run high availability and want identical dashboards on both nodes, include the Users and Groups option in the HA synchronisation settings.

## Checked

2026-11-03. Read the Dashboard manual page (dashboard.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
