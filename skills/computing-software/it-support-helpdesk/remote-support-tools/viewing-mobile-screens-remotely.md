---
id: computing-software.it-support-helpdesk.remote-support-tools.viewing-mobile-screens-remotely
name: viewing-mobile-screens-remotely
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, mobile-screen-sharing, session-narration, remote-support, ios-screen-broadcast, android-remote-control]
level: practitioner
status: draft
description: "View or control phone and tablet screens during support: iOS broadcast limits, Android remote control add-ons, Remote Help, and narrating each step to the user."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/remote-help-android"
  - "https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-remote/remote-control/mobile-device-support/"
  - "https://support.apple.com/guide/iphone/record-the-screen-iph52bb0a9f6/ios"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# viewing-mobile-screens-remotely

## What's possible per platform
| Platform | View | Control | How |
|---|---|---|---|
| iOS/iPadOS | Yes | No | Screen broadcast via ReplayKit in TeamViewer QuickSupport, AnyDesk, Zoho; user starts broadcast from Control Center |
| Android (Samsung, Zebra, others with add-ons) | Yes | Yes | Vendor add-on or OEM agreements (TeamViewer add-on, Samsung Knox) |
| Android dedicated devices | Yes | Yes | Intune Remote Help for Android (Zebra, Samsung dedicated devices) |
| Any | Video call | No | Teams video with rear camera pointed at the screen of a second device |
- iOS never allows remote control by third-party tools; plan for guidance, not driving.

## iOS broadcast steps (QuickSupport-type apps)
1. User installs the app and reads you the session ID.
2. You connect; the app prompts the user to start a broadcast: Control Center > long press
   Screen Recording > choose the app > Start Broadcast.
3. Notifications and passwords appear in the stream; ask the user to enable Do Not
   Disturb and not type passwords while shared.

## Narration (essential when you can only view)
- Say what you see and what you want before each step: "I can see your Settings screen.
  Tap General, it's the grey gear about halfway down."
- Use screen landmarks (colour, position), not just labels the user can't find.
- Confirm after each step: "What do you see now?"
- When you can control (Android), still narrate: "I'm going to open Wi-Fi settings now",
  so the user isn't alarmed and learns the path.
- Pause and hand back for anything personal (photos, messages, banking apps).

## Security and privacy
- Ask before starting; tell the user how to stop sharing.
- Don't record mobile sessions unless policy and consent cover it.
- Be wary of users asking to "share screen" with callers claiming to be IT: same
  social-engineering rules apply.

## Verify
The user confirms the issue is fixed, knows how the session ended, and the ticket notes
the tool and whether control or view-only was used.
