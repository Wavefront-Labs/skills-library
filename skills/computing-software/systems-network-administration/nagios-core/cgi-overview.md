---
id: computing-software.systems-network-administration.nagios-core.cgi-overview
name: cgi-overview
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, cgis, status-cgi, extinfo-cgi, tac-cgi, statusmap, cmd-cgi, history-cgi, trends, avail, showlog, web-interface]
level: intro
status: docs-checked
description: "What each Nagios Core CGI does (status, statusmap, extinfo, tac, outages, config, cmd, history, trends, avail, histogram, showlog, summary) and which need log rotation or gd."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cgis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The CGIs

| CGI | Purpose |
|---|---|
| status.cgi | current host/service status, group overview or detail |
| statusmap.cgi | PNG network map (gd 1.6.3+); layout from host coordinates or automatic |
| statuswrl.cgi | 3-D VRML model; needs a VRML browser |
| extinfo.cgi | process info, host and service state statistics, comments; launch point for commands |
| tac.cgi | tactical overview, handled vs unhandled problems |
| outages.cgi | problem hosts causing outages, by severity |
| config.cgi | view object definitions |
| cmd.cgi | send commands to the process (start from extinfo; leave its arguments alone) |
| history.cgi, notifications.cgi | alert and notification logs, filterable; archives need log rotation |
| trends.cgi, avail.cgi, histogram.cgi | state graphs and availability; need log rotation + archive path (gd for graphs) |
| showlog.cgi | the Nagios log |
| summary.cgi | alert totals and top producers |
| statuswml.cgi | WAP/mobile status and basic commands |

Without authentication enabled, nobody can issue commands. Authorization: `computing-software.systems-network-administration.nagios-core.cgi-authorization`.

## Checked

2026-11-04. Confirmed each CGI row against the CGIs page (file names, purposes, gd 1.6.3 or higher for the map and graphs, VRML browser, log rotation and log_archive_path for history/trends/availability, cmd.cgi arguments left alone, no commands without authentication). Removed an unconfirmed performance claim for extinfo.cgi.

Method: documentation only; no commands were run.
