---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.windows-notification-database
name: windows-notification-database
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [notification-database, user-activity-artefacts, sqlite-forensics, dfir, wpndatabase]
level: practitioner
status: draft
description: "Recover toast notifications from wpndatabase.db: Notification and Handler tables, XML payloads with message previews, arrival and expiry times."
sources: ["https://inc0x0.com/2018/10/windows-10-notification-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows notification database

**Goal:** toast notifications show message previews from Teams, Outlook, Slack, Signal desktop,
browsers and security tools. Windows stores them in a SQLite database that persists after the toast disappears.

## Location
`%LOCALAPPDATA%\Microsoft\Windows\Notifications\wpndatabase.db` (+ `-wal`); older builds used `appdb.dat`.

## Tables
| Table | Content |
|---|---|
| `Notification` | `HandlerId`, `Type` (toast, tile, badge), `Payload` (XML), `ArrivalTime`, `ExpiryTime` (FILETIME), `Tag`, `Group` |
| `NotificationHandler` | `PrimaryId` = app identifier (AUMID such as `MSTeams_8wekyb3d8bbwe!MSTeams`), created time |

## Query
```sql
SELECT h.PrimaryId AS app,
       datetime(n.ArrivalTime/10000000 - 11644473600, 'unixepoch') AS arrival_utc,
       datetime(n.ExpiryTime/10000000 - 11644473600, 'unixepoch') AS expiry_utc,
       CAST(n.Payload AS TEXT) AS payload
FROM Notification n JOIN NotificationHandler h ON h.RecordId = n.HandlerId
ORDER BY n.ArrivalTime;
```
The XML payload `<text>` elements contain sender names and message previews.

## Investigative uses
- Chat/email previews for messages since deleted from the app or held only on a phone.
- Security product alerts the user saw (and dismissed) - establishes awareness.
- Browser web-push notifications from malicious sites (notification spam campaigns).

## Gotchas
- Notifications expire and are purged; recent ones may be only in the WAL file - collect it.
- Focus Assist / do-not-disturb still records some notifications; absence is not proof none arrived.
- Free-page recovery on the SQLite file can return deleted rows.

## Verify
Payload content and arrival times are cross-checked with the source app's own data where available.
