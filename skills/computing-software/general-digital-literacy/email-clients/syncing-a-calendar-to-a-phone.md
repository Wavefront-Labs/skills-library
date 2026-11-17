---
id: computing-software.general-digital-literacy.email-clients.syncing-a-calendar-to-a-phone
name: syncing-a-calendar-to-a-phone
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, calendar, calendar-sync, caldav, exchange-activesync]
level: intro
status: draft
description: "Get Outlook, Google or iCloud calendars onto iPhone and Android, choose which calendars show, and fix events that don't appear or appear twice."
sources:
  - https://support.google.com/calendar
  - https://support.apple.com/guide/iphone/welcome/ios
  - https://support.microsoft.com/en-us/outlook
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sync a calendar to a phone

## Add the account
- **iPhone**: Settings > Calendar > Accounts > Add Account (iCloud, Microsoft Exchange, Google, Outlook.com) and turn **Calendars** on.
- **Android**: Google calendars sync automatically in Google Calendar. Outlook/Exchange: install **Outlook for Android** or add the account under Settings > Passwords & accounts and enable *Sync Calendar*.
- Microsoft 365 work accounts: the **Outlook app** is often required by company policy (Intune) and gives the best results.
- Other providers (Fastmail, Nextcloud): CalDAV account on iPhone; DAVx5 on Android.

## Choose what shows
- iPhone Calendar app > **Calendars** at the bottom: tick/untick per calendar, including shared and subscribed ones.
- Google: shared calendars may need enabling at calendar.google.com/calendar/syncselect on iOS.
- Google Calendar app > menu: tick the calendars to display.

## Fixing problems
- **Events missing**: check the right calendar is ticked; on iPhone set Settings > Calendar > *Sync* to *All Events* (default only syncs a month back).
- **Duplicates**: the same account added twice (e.g. via iOS Settings and also inside a calendar app); remove one. Or a subscribed ICS and a shared copy of the same calendar.
- **Wrong times**: Settings > Calendar > *Time Zone Override* off unless you want it; check phone time zone is automatic.
- **Not updating**: pull to refresh; Settings > Mail > Accounts > *Fetch New Data* set to Push/Automatic; subscribed ICS calendars refresh slowly (hours).

## Verify
- [ ] Create an event on the computer and see it on the phone within a few minutes, and vice versa.
