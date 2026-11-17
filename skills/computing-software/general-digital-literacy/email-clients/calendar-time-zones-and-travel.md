---
id: computing-software.general-digital-literacy.email-clients.calendar-time-zones-and-travel
name: calendar-time-zones-and-travel
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, calendar, calendar-time-zones, travel-time-zone, secondary-time-zone, meeting-time-zone]
level: intro
status: docs-checked
description: "Schedule across time zones in Google Calendar: set the primary and extra zones, set separate start and end zones, a world clock, and how daylight saving is handled."
sources:
  - https://support.google.com/calendar/answer/37064
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Calendar time zones and travel (Google Calendar)

## How it works
An event you create appears in your local time zone and in the local time zone of anyone you invite. Calendar stores events converted to UTC and always shows them in your local time. When you travel, your calendar shows local time. Events created before an area changed its time-zone rules may be in the wrong zone.

## Settings (computer)
- Primary zone for all calendars: Settings > General > **Time zone** > **Primary time zone**; tick **Ask to update my primary time zone to current location** to be asked when you travel.
- One calendar only: My calendars > More > **Settings and sharing** > Time zone (owners only).
- Extra zones on the grid: Settings > Time zone > **Show additional time zones**, choose a secondary and optionally a tertiary zone.
- World clock: Settings > World clock > **Show world clock** > Add time zone.

## Event time zones
- New event: Create > Event > More options > **Time zone** next to the time; **Use separate start and end time zones** for flights.
- Existing event: open > Edit > Time zone > OK.

## Habits
- State the zone in the invite text ("15:00 UK / 10:00 ET").
- Check recurring cross-continent meetings after clocks change; Google notes past or future years may not reflect daylight saving changes.

## Verify
- [ ] Hover the event: it shows the intended time in the other attendee's zone.

## Checked
2026-10-27. Google Calendar Help "Use Google Calendar in different time zones". Confirmed every setting name and path above, UTC storage and daylight-saving note. Removed unconfirmed Outlook and Apple Calendar steps and the Find a time and worldtimebuddy remarks.
Method: documentation only; no commands were run.
