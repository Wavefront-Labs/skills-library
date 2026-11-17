---
id: defence-public-safety.physical-and-access-security.access-control-systems.credential-lifecycle-and-access-policy-administration
name: credential-lifecycle-and-access-policy-administration
category: defence-public-safety
field: physical-and-access-security
product: access-control-systems
tags: [physical-and-access-security, access-control-systems, pacs, physical-access-control, acs, credentials, proximity-card, 125-khz, mifare-desfire, iclass-seos, mobile-credentials, osdp, wiegand, card-reader, controller, door-position-switch, request-to-exit, rex, maglock, electric-strike, fail-safe, fail-secure, access-levels, schedules, joiner-mover-leaver, anti-passback, tailgating, audit-trail, visitor-management]
level: practitioner
status: draft
description: "Running an electronic access control system: credential technologies, readers and controllers, access levels and schedules, joiner/mover/leaver process, fail-safe vs fail-secure, and audits."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Credential lifecycle and access policy administration

**Goal:** make sure the system lets the right people through the right doors at the
right times — and stops letting them the day they leave. Most access control failures
are administrative, not technical. Reference for security administrators and
integrators; product terms differ between vendors.

## 1. Components
- **Credential:** card, fob, mobile credential, PIN, or biometric. Legacy **125 kHz
  proximity** cards and unencrypted formats are widely considered easy to copy;
  prefer secure smart credentials (e.g. MIFARE DESFire EV2/EV3, HID Seos — or current
  equivalents) with diversified keys.
- **Reader** at the door; **controller** that holds the decision logic and database
  cache; **server/software** for administration.
- Reader-to-controller wiring: legacy **Wiegand** is unencrypted and unsupervised;
  **OSDP** (with Secure Channel enabled) supports encryption and supervision — the
  better choice for new installs.
- **Door hardware:** electric strike or maglock, **door position switch** (detects
  forced/held open), **request-to-exit (REX)**.

## 2. Fail-safe vs fail-secure
- **Fail-safe** unlocks on power loss (maglocks are inherently fail-safe); required on
  many egress paths and often tied to fire alarm release.
- **Fail-secure** stays locked on power loss (common with electric strikes, free
  egress from the inside retained mechanically).
Life-safety and fire codes govern egress doors — check the local code (e.g. NFPA 101/
IBC in the US) and the fire authority before changing locking.

## 3. Access policy
- Build **access levels** from roles (e.g. "Lab staff — Building B labs, 07:00–19:00
  weekdays"), not from individual door lists per person. Fewer, well-named levels are
  easier to review.
- Use **schedules** and holiday calendars; time-limit contractor and visitor access.
- **Least privilege:** grant the narrowest level that does the job; time-bound elevated
  access.
- Features to consider: **anti-passback** (stops a card being passed back for a second
  entry), two-person rule for critical rooms, card + PIN for high-security doors.

## 4. Joiner / mover / leaver
- **Joiner:** credential issued only on an authorised request (manager plus security),
  ID verified, photo captured, credential number recorded.
- **Mover:** remove the old level when adding the new one — "privilege creep" is the
  classic failure.
- **Leaver:** disable the credential at departure — ideally automated from the HR
  system — and recover the physical card. Lost cards are disabled immediately.
- Shared or generic credentials (e.g. "cleaner 1") defeat the audit trail; avoid them.

## 5. Monitoring and audit
- Alarm handling for **door forced** and **door held open**; tune held-open times so
  operators don't learn to ignore alarms.
- Periodic **access reviews:** each area owner confirms who has access; remove the rest.
- Reports: credentials unused for 90 days (candidates for removal), after-hours use.
- **Tailgating** is a people problem: signage, training, turnstiles or mantraps where
  justified.

## Gotchas
- Offline controllers keep stale databases; verify sync after mass changes.
- Battery-backed locks and readers on fire release need testing with the fire system.
- Integrator default passwords and unpatched servers — the ACS is an IT system too.

## Verify
- [ ] Credential technology and reader protocol are current and encrypted.
- [ ] Every egress door's fail mode matches code and fire authority approval.
- [ ] Access levels are role-based with owners and schedules.
- [ ] Leaver process disables credentials the same day; tested by sample.
- [ ] Access review completed within the agreed cycle.
