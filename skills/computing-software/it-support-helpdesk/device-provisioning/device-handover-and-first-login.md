---
id: computing-software.it-support-helpdesk.device-provisioning.device-handover-and-first-login
name: device-handover-and-first-login
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, device-handover, onboarding, first-login, windows-hello, temporary-access-pass, acceptable-use]
level: practitioner
status: draft
description: "Hand a new device to a user so day one works: pre-staging checks, guided first sign-in and MFA, Hello and OneDrive setup, signed acceptance and asset record update."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/user-driven"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass"
  - "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# device-handover-and-first-login

## Before handover
- Device pre-provisioned (or Autopilot tested), fully updated, BitLocker on, compliant in
  Intune, asset record created with serial and tag.
- Accessories ready: charger, dock, headset; boxes labelled with the user's name.
- TAP issued and delivered securely (manager or in person), not by email to the new
  mailbox.

## First sign-in (sit with them, or a scheduled call)
1. Connect to Wi-Fi or Ethernet; sign in with UPN and TAP.
2. Register MFA (Authenticator or passkey) and set up Windows Hello PIN/face.
3. Wait for ESP/user apps; open Outlook, Teams, OneDrive (confirm Known Folder Move), and
   the browser with work profile sign-in.
4. Add printers if not automatic; test a print. Test camera, mic and speaker in Teams.
5. Show how to lock (`Win`+`L`), get support (portal, phone, chat), and report phishing.

## Paperwork
- User accepts the acceptable use policy and device agreement (signed or e-acknowledged).
- Update the asset record: assigned user, date, accessories issued, condition.
- Close the onboarding ticket with what was verified.

## Remote handover
Ship to a verified address, send TAP separately once delivery is confirmed, and book a
call for the first sign-in. Ask for the courier confirmation in the ticket.

## Gotchas
- TAP expires; check its lifetime covers the handover time.
- Users on day one often cannot receive SMS or access their personal phone; have a FIDO2
  key or Authenticator plan agreed with the manager.

## Verify
The user signs in without help on a second attempt (lock and unlock), MFA and Hello work,
core apps open, and the asset record shows them as owner.
