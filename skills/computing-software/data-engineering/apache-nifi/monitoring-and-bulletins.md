---
id: computing-software.data-engineering.apache-nifi.monitoring-and-bulletins
name: monitoring-and-bulletins
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, monitoring, bulletins, summary, status-history, system-diagnostics]
level: intro
status: docs-checked
description: "NiFi monitoring basics: bulletins (WARN default, five minute expiry), five minute statistics, 24 hour status history, Summary page tabs and System Diagnostics."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring

- Bulletins: a component that logs an event raises a bulletin. The Bulletin level on the Settings tab sets the lowest level shown in the UI and defaults to WARN (warnings and errors). Hover over the bulletin icon to read the message, level, time and, in a cluster, the emitting node. Bulletins expire automatically after five minutes. A child component's bulletin also shows on its parent Process Group.
- Processor and Process Group statistics on the canvas cover the past five minutes (for a cluster, all nodes combined).
- Status History (right-click a component, or from the Summary page) stores history configurable in NiFi properties, defaulting to 24 hours; see the Component Status Repository in the administration guide.
- Summary page (Global Menu > Summary): a table of components with five tabs for the component types, a Pop Out button to open it in its own tab or window, and System Diagnostics.
- The Connections tab links to the Cluster Connection Summary showing data per node.
- System Diagnostics: CPU utilisation, disk fullness, and Java metrics such as memory and garbage collection information.
- Cluster membership persists across restarts; remove a node that will not return via the Cluster dialog.

Verify: a deliberate processor error raises a bulletin that disappears after about five minutes.

## Checked

Confirmed against the NiFi user guide (Anatomy of a Processor, Anatomy of a Process Group, Summary Page, Status History, Load Balancing). Removed the claim that the Summary page is not auto-refreshed (not stated).

Method: docs-only read of cited pages, 2026-11-08
