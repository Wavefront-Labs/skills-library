---
id: computing-software.cybersecurity-defensive.endpoint-security.usb-exception-process
name: usb-exception-process
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [usb-exception-process, device-control-exceptions, removable-media-approval, encrypted-usb, risk-acceptance, device-control]
level: practitioner
status: draft
description: "Run a USB and removable media exception process: request and approval, approved encrypted devices by serial, time-limited exceptions, scanning stations and periodic review."
sources: ["https://www.cisecurity.org/controls/v8", "https://learn.microsoft.com/en-us/defender-endpoint/device-control-removable-storage-access-control", "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB exception process

Blocking removable media is easy; keeping it blocked depends on a fast, controlled exception path.

## Request
Fields: user, device(s), business reason, data classification to be moved, duration, alternative considered
(secure file transfer, SharePoint external sharing, managed SFTP), manager approval.

## Approve
- Security approves; data owner approves for confidential data.
- Prefer **issuing a corporate encrypted USB device** (FIPS 140-2/3 validated hardware-encrypted keys, or BitLocker To Go enforced) registered by **serial number** over allowing a user's own device.
- Exception scoped to user + device serial + access (read-only vs read/write) + **expiry date** (e.g. 30-90 days).

## Implement
- Add the serial to the allowed group in device control (Defender device control `SerialNumberId`, Jamf, Ivanti etc.) via the policy pipeline, linked to the ticket.
- BitLocker "Deny write access to removable drives not protected by BitLocker" enforces encryption.

## Inbound media from outside (vendors, auditors)
Kiosk/scanning station (multi-engine AV, CDR) that copies sanitised files to a share; do not plug external
media into corporate endpoints.

## Monitor and review
- Log file copies to the approved device (Defender `DeviceEvents` / DLP).
- Monthly report of active exceptions; expired exceptions removed automatically.
- Lost corporate USB device = incident report; encryption limits impact.

## Verify
- [ ] Every allow-list entry maps to a ticket with expiry.
- [ ] Average approval time within SLA (otherwise users find workarounds).
