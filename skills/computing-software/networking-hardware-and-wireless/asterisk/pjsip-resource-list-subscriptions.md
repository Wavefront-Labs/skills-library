---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-resource-list-subscriptions
name: pjsip-resource-list-subscriptions
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, rls, resource-list, blf, presence, mwi, subscriptions]
level: advanced
status: docs-checked
description: "Group many presence, dialog or MWI subscriptions into one PJSIP resource_list with list_item entries and notification_batch_interval, including non-existent items and list loops."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Resource-List-Subscriptions-RLS/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip resource list subscriptions
RLS (RFC 4662) lets a phone make one subscription to a list instead of N-squared individual ones, reducing boot-time SUBSCRIBE bursts and dialog memory.

Define in `pjsip.conf`:
```
[sales]
type = resource_list
event = presence
list_item = alice
list_item = bob
```
- `event`: `presence` (BLF), `dialog` (alternate BLF), or `message-summary` (MWI).
- `list_item`: for presence and dialog, a dialplan extension name (needs a matching hint); for message-summary, a mailbox name (`mailbox@context` with app_voicemail).
- `notification_batch_interval`: milliseconds over which state changes are collected before one NOTIFY, for example `2000`. It reduces NOTIFY traffic but short transient states (a quick ring) can be missed.

Corner cases: if at least one list item subscription succeeds, the list subscription succeeds and only successful items are reflected. Lists that contain each other form a loop; the page describes how that is handled.

## Checked

2026-11-09. Confirmed against the Asterisk Resource List Subscriptions page: RFC 4662, resource_list type, event packages, list_item formats, notification_batch_interval in milliseconds and its transient-state drawback, non-existent item and loop policies. Nothing changed.
Method: documentation only; no commands were run.
