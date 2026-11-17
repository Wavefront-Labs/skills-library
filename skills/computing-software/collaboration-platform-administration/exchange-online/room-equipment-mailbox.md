---
id: computing-software.collaboration-platform-administration.exchange-online.room-equipment-mailbox
name: room-equipment-mailbox
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [room-equipment-mailbox]
level: practitioner
status: draft
description: Provision bookable resources with booking policy.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Room and equipment mailboxes
**Goal:** Provision bookable resources with booking policy.

- `New-Mailbox -Room -Name 'Room 1'` or `-Equipment`.
- `Set-CalendarProcessing -Identity 'Room 1' -AutomateProcessing AutoAccept -AllowConflicts $false -BookingWindowInDays 180 -MaximumDurationInMinutes 480`.
- Use room lists (`New-DistributionGroup -RoomList`) for Outlook room finder.
- Restrict who can book with `-BookInPolicy` and `-AllBookInPolicy $false`.

## Gotchas
- With AutoAccept disabled, requests wait for a delegate that may not exist.
- Allow external meeting requests deliberately via `-ProcessExternalMeetingMessages`.

## Self-check
Send a test invite to the room and confirm automatic acceptance.
