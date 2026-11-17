---
id: computing-software.collaboration-platform-administration.vikunja.caldav-clients-and-ios
name: caldav-clients-and-ios
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, caldav-urls, caldav-ios-reminders, vtodo-properties, caldav-tested-clients]
level: practitioner
status: docs-checked
description: "Connect CalDAV clients to Vikunja: discovery URL, iOS Reminders setup, supported VTODO properties and which clients are known to work or fail."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/help/caldav.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CalDAV support is alpha: it works with some clients and has bugs with others. Connection details are in Settings, CalDAV tab.

URLs live under `/dav`. For a new client use `/principals/<username>/` (project discovery). Also `/projects/`, `/projects/<id>/` and `/projects/<id>/<task UID>`.

iOS/iPadOS (needs Vikunja 2.2.0+): create a CalDAV token, then Settings, Apps, Calendar, Calendar Accounts, Add Account, Other, Add CalDAV Account. Server is the full URL with `https://` and trailing slash, for example `https://vikunja.example.com/api/v1/dav/principals/yourname/`. User is the username, password is the token. Turn on Reminders. Each project becomes a list. If verification fails, check the Server field has the full URL including `https://` and the trailing slash; repeated failures are rate limited per IP.

Supported properties: UID, SUMMARY, DESCRIPTION, PRIORITY, CATEGORIES, COMPLETED, DUE, DURATION, DTSTAMP, DTSTART, VALARM, RELATED-TO (parent/child), STATUS (COMPLETED only). CREATED and LAST-MODIFIED and RRULE go Vikunja to client only. Not supported: ATTACH, COMMENT, LOCATION, GEO, URL, PERCENT-COMPLETE, SEQUENCE (the page also lists CLASS, CONTACT, RECURRENCE-ID, RESOURCES and a disabled ORGANIZER).

Working clients: Evolution, OpenTasks with DAVx5, Tasks (Android), Korganizer, Apple Reminders. Not working: Thunderbird 68.

## Checked

2026-11-04: URLs, iOS steps, supported and unsupported properties and the client list checked against the CalDAV help page.

Method: documentation only; no commands were run.
