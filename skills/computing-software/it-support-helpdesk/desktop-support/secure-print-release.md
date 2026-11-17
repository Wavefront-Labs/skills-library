---
id: computing-software.it-support-helpdesk.desktop-support.secure-print-release
name: secure-print-release
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, secure-print-release, pull-printing, follow-me-printing, badge-release, printing]
level: practitioner
status: draft
description: "Set up and support secure print release: held jobs released at the device by badge or PIN, follow-me queues, retention timers, card enrolment and common release failures."
sources:
  - https://www.papercut.com/help/manuals/ng-mf/common/topics/secure-print-release.html
  - https://learn.microsoft.com/en-us/universal-print/fundamentals/universal-print-anywhere
  - https://www.ncsc.gov.uk/collection/device-security-guidance/managing-deployed-devices/printers
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure print release

**Why:** printed payroll and HR documents left in output trays are a common data leak. Held jobs print only when the owner is at the device.

## How it works
1. User prints to a **hold/release queue** (often one "follow-me" queue for all devices).
2. The print server or cloud service holds the job, tagged with the user identity.
3. At any compatible device, the user authenticates: **badge/card** (HID Prox, iCLASS, MIFARE readers), **PIN**, or mobile app/QR, then releases selected jobs.
4. Unreleased jobs are deleted after a timer (e.g. 4-24 hours).

## Products
PaperCut MF/NG, Ricoh Streamline NX, Kofax/Tungsten Printix, uniFLOW, Universal Print "anywhere" with partner release apps; vendor embedded apps on the MFD panel.

## Setup essentials
- Queue configuration: hold all jobs on the release queue; driver: universal driver compatible with all fleet models (colour/duplex capabilities lowest common denominator).
- Identity: sync users from AD/Entra; card numbers self-enrolled at first swipe (user enters credentials once) or imported from the badge system.
- Device: install embedded app or attach card reader; set device to require login.
- Policies: default duplex/mono, retention timer, release-all vs choose jobs.

## Common tickets
| Symptom | Check |
|---|---|
| "My job is not at the printer" | Job held under a different username (service account, shared PC); check the held jobs list on the server |
| Badge not recognised | Card not enrolled or reader format mismatch; re-enrol |
| Job released but prints garbled | Driver mismatch with device model; use the universal driver or device-specific queue |
| Jobs disappear | Retention timer expired |
| Mac/mobile prints not held | Client not sending user identity; install client or use authenticated IPP |

## Verify
Print a test page to the release queue, confirm it waits, release at two different devices, and check the audit log records user, device and pages.
