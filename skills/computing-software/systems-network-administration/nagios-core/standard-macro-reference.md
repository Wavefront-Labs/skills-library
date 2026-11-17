---
id: computing-software.systems-network-administration.nagios-core.standard-macro-reference
name: standard-macro-reference
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, macro-list, hoststate, servicestate, notificationtype, servicenotificationnumber, totalhostsdown, timet, downtime-macros]
level: practitioner
status: docs-checked
description: "Quick reference to standard Nagios Core macro groups: host and service state, notification, contact, date/time, file locations, summary totals, downtime, and where each is valid."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/macrolist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standard macros by group

- **Host state:** `$HOSTSTATE$`, `$HOSTSTATEID$`, `$HOSTSTATETYPE$`, `$LASTHOSTSTATE$`, `$HOSTATTEMPT$`, `$MAXHOSTATTEMPTS$`, `$HOSTDURATION$`, `$HOSTDURATIONSEC$`. Current state macros are not determined during the host's own check.
- **Service state:** same with SERVICE prefix. A macro used in a command where it is invalid becomes an empty string.
- **Notification:** `$NOTIFICATIONTYPE$`, `$NOTIFICATIONAUTHOR$` (`NAME`, `ALIAS`), `$NOTIFICATIONCOMMENT$`, `$NOTIFICATIONRECIPIENTS$`, `$NOTIFICATIONISESCALATED$`: notification commands only. Numbers are `$HOSTNOTIFICATIONNUMBER$` (host commands) and `$SERVICENOTIFICATIONNUMBER$` (service commands); there is no plain `NOTIFICATIONNUMBER`.
- **Contact:** `$CONTACTNAME$`, `$CONTACTALIAS$`, `$CONTACTEMAIL$`, `$CONTACTPAGER$`, `$CONTACTADDRESSn$`: notification commands only.
- **Date/time:** `$LONGDATETIME$`, `$SHORTDATETIME$`, `$DATE$`, `$TIME$`, `$TIMET$`.
- **Files:** `$MAINCONFIGFILE$`, `$STATUSDATAFILE$`, `$RETENTIONDATAFILE$`, `$LOGFILE$`, `$RESOURCEFILE$`, `$COMMANDFILE$`, `$HOSTPERFDATAFILE$`, `$SERVICEPERFDATAFILE$` and others.
- **Summary:** `$TOTALHOSTSUP$`, `$TOTALHOSTSDOWN$`, `$TOTALSERVICESCRITICAL$`, `...UNHANDLED$`, `$TOTALHOSTPROBLEMS$`. In notifications they are filtered to the contact's objects. Not environment variables under `use_large_installation_tweaks`.
- **Downtime:** `$HOSTDOWNTIME$` / `$SERVICEDOWNTIME$` give the downtime depth (>0 in downtime). Notification types: DOWNTIMESTART, DOWNTIMEEND, DOWNTIMECANCELLED.
- **Deprecated:** `$HOSTACKAUTHOR$` etc.; use `$NOTIFICATIONAUTHOR$`.

## Checked

2026-11-04. Confirmed against the Macro list page: macro names in each group, the footnote that state macros are not valid for a host while it is being checked, HOSTNOTIFICATIONNUMBER and SERVICENOTIFICATIONNUMBER only, summary macros filtered to the contact in notifications, deprecated acknowledgement macros, downtime depth macros and the empty-string rule for invalid macros.

Method: documentation only; no commands were run.
