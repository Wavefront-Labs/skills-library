---
id: computing-software.it-support-helpdesk.apple-device-management.enrollment-failures
name: enrollment-failures
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-troubleshooting, enrollment-failures, enrollment-troubleshooting, ade-failures]
level: practitioner
status: docs-checked
description: "Diagnose failing automated or user-initiated Apple enrolment: serial assignment, Apple network hosts, HTTPS interception, push certificate and a clean-device comparison."
sources:
  - https://support.apple.com/en-us/101555
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# enrollment-failures

Goal: find why a device will not enrol.
- Check the serial number is assigned to your MDM server in the device-management portal and to the right prestage or enrolment profile in the MDM.
- Verify the device can reach the Apple hosts used for enrolment (Apple's "Use Apple products on enterprise networks" article lists them, all on port 443): `albert.apple.com` (device activation), `iprofiles.apple.com` (hosts enrolment profiles for Device Enrollment), `mdmenrollment.apple.com` (device management services upload enrolment profiles and look up devices), `deviceenrollment.apple.com` (DEP provisional enrollment), `gdmf.apple.com` (software updates available under managed software updates), `identity.apple.com` (APNs certificate request portal), `vpp.itunes.apple.com` (Apps and Books licence operations), and `*.push.apple.com` (push notifications, on ports 443, 80, 5223 and 2197).
- Also allow your MDM server's own URL, and check its TLS certificate chain.
- Confirm the push certificate is valid and has not expired.
Practice: use a clean test device on the same network and compare it with a failing one; if both fail, the network or token is the cause, and if only one fails, check its serial and assignment. Note the exact error text shown on the Setup Assistant screen in the ticket.
Gotcha: Apple services fail any connection that uses HTTPS interception (SSL inspection). If traffic goes through a web proxy, disable HTTPS interception for the hosts Apple lists. Devices can reach APNs through an HTTP proxy configured manually, by an MDM service, or through a proxy auto-config (PAC) file.
Verify:
- Device reaches Remote Management.
- Enrolment shows in the MDM.

## Checked
2026-11-08. Checked the hosts, ports and purposes against Apple Support article 101555, including the HTTPS interception and proxy statements. Removed: the Jamf troubleshooting source (it did not load), the `*.apple.com` wildcard instruction, the `/var/log/install.log` and `log show` mdmclient predicate lines (no readable documentation), and the claim that only the JSS URL needs checking. Procedural steps (serial assignment, clean-device comparison) are practice advice, not documented claims.

Method: documentation only; no commands were run.
