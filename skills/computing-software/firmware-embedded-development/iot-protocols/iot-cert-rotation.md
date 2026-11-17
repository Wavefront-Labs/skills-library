---
id: computing-software.firmware-embedded-development.iot-protocols.iot-cert-rotation
name: iot-cert-rotation
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [iot-cert-rotation, iot-security, certificate-rotation, renewal, est, expiry, iot-protocols]
level: practitioner
status: draft
description: "Certificate rotation for devices: Renew device certificates before expiry without truck rolls."
sources:
  - https://datatracker.ietf.org/doc/html/rfc7030
  - https://www.etsi.org/deliver/etsi_en/303600_303699/303645/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate rotation for devices

**Goal:** Renew device certificates before expiry without truck rolls.

## Steps
1. Pick lifetimes of 1-5 years for devices and shorter for gateways
2. Renew with EST (RFC 7030) simpleenroll or a cloud API using the current cert for authentication
3. Start renewal at 70-80 percent of lifetime with jitter
4. Keep the old cert until the new one is confirmed working
5. Maintain CA rollover: trust both old and new CA for an overlap
6. Track expiry dates in the fleet inventory

## Gotcha
Devices offline past expiry cannot authenticate to renew; provide a bootstrap path such as re-provision with claim cert.

## Verify
- [ ] Renewal works in staging
- [ ] Both CAs trusted during overlap
- [ ] Alert on devices within 30 days of expiry
