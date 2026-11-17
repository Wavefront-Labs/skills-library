---
id: computing-software.it-support-helpdesk.apple-device-management.mdm-check-in-and-commands
name: mdm-check-in-and-commands
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, mdm-protocol, mdm-check-in-and-commands, check-in, mdm-commands]
level: practitioner
status: draft
description: "Trace the MDM protocol flow of check-in messages, push wake-ups and command queue results to explain why a command stays pending."
sources:
  - "https://developer.apple.com/documentation/devicemanagement"
  - "https://support.apple.com/guide/deployment/depc0bc6c1bf/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mdm-check-in-and-commands

Goal: reason about the protocol when commands appear stuck.
- Check-in messages: Authenticate, TokenUpdate (push token, UnlockToken, topic), CheckOut.
- APNs sends only an empty wake-up; the device then connects to the ServerURL (PUT /mdm) with Idle, receives the next command plist, and returns Acknowledged, Error or NotNow.
- Common commands: InstallProfile, RemoveProfile, DeviceInformation, InstallApplication, EraseDevice, DeviceLock, ScheduleOSUpdate.
- NotNow means the device is busy (locked, before first unlock) and will check in later.
Gotcha: an unreachable ServerURL or an expired TLS certificate looks like a push problem; test the URL and certificate chain before blaming APNs.
Verify:
- Command history shows Acknowledged for a test command.
- The MDM log shows a recent TokenUpdate for the device.
