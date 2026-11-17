---
id: computing-software.firmware-embedded-development.iot-protocols.device-identity-x509
name: device-identity-x509
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [device-identity-x509, iot-provisioning, x509, device-certificate, csr, private-ca, iot-protocols]
level: practitioner
status: draft
description: "Device identity with X.509: Give each device a unique, rootable identity."
sources:
  - https://datatracker.ietf.org/doc/html/rfc5280
  - https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device identity with X.509

**Goal:** Give each device a unique, rootable identity.

## Steps
1. Generate the key pair on the device or secure element so the private key never leaves
2. Device creates a CSR; factory CA signs it into a certificate with CN or SAN equal to device ID
3. Use an intermediate CA for the fleet and keep the root offline
4. Short-lived certs (months to a few years) with rotation plan
5. Store key in secure element (ATECC608, TPM, STSAFE) or protected flash
6. Record identity to inventory at manufacture

## Gotcha
Putting one shared certificate in all firmware images means a single leak breaks the whole fleet.

## Verify
- [ ] Unique cert per serial
- [ ] Private key not exported
- [ ] Revocation or deny process tested
