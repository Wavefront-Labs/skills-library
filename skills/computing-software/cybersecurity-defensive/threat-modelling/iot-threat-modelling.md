---
id: computing-software.cybersecurity-defensive.threat-modelling.iot-threat-modelling
name: iot-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [iot-threat-modelling, iot-security, embedded-devices, firmware, etsi-en-303-645]
level: practitioner
status: docs-checked
description: "Threat model a consumer IoT product against ETSI EN 303 645 V3.1.3: credentials, updates, stored secrets, network and physical interfaces, boot integrity."
sources: ["https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IoT threat modelling against ETSI EN 303 645

ETSI EN 303 645 V3.1.3 (2024-09) sets baseline provisions for consumer IoT devices. Use its
provisions as the control checklist when you model the device, its companion services and
its update path. Provision 5.0-1 says a justification shall be recorded for each
recommendation that is considered not applicable or not fulfilled; record the same in the
threat model.

## Provision groups and the threats they answer
- **5.1 No universal default passwords.** Passwords must be unique per device or defined by
  the user (5.1-1); pre-installed unique passwords need a generation mechanism that reduces the
  risk of automated attacks across a device class (5.1-2); passwords should not be used for
  machine-to-machine authentication (5.1-2A); authentication must use best practice
  cryptography (5.1-3); users get a simple way to change the authentication value (5.1-4);
  brute-force attacks over network interfaces must be made impracticable unless a resource
  constraint prevents it (5.1-5).
- **5.2 Vulnerability reports.** A public vulnerability disclosure policy (5.2-1), timely action
  on disclosed vulnerabilities (5.2-2), and continual monitoring during the support period
  (5.2-3).
- **5.3 Updates.** Non-immutable software should be securely updateable (5.3-1); a secure update
  mechanism unless a resource constraint prevents it (5.3-2); best practice cryptography for
  updates (5.3-7); timely security updates (5.3-8); the device should verify authenticity and
  integrity of updates (5.3-9), and must do so via a trust relationship when updates arrive
  over a network (5.3-10); the defined support period must be published (5.3-13); devices that
  cannot be updated should be isolable and their hardware replaceable (5.3-15A, 5.3-15B).
- **5.4 Stored secrets.** Sensitive security parameters stored securely (5.4-1); hard-coded
  unique device identities resist tampering (5.4-2); no hard-coded critical security
  parameters in source code (5.4-3); critical parameters for update checks and service
  communication are unique per device (5.4-4).
- **5.5 Communicate securely.** Best practice cryptography (5.5-1); reviewed or evaluated
  implementations (5.5-2); replaceable algorithms (5.5-3); access to functionality over a
  network interface only after authentication (5.5-4, and 5.5-5 for security-relevant
  configuration changes); critical security parameters encrypted in transit and
  confidentiality protected over remotely accessible interfaces (5.5-6, 5.5-7); managed
  through their lifecycle (5.5-8).
- **5.6 Minimise attack surface.** Disable unused network and logical interfaces (5.6-1);
  minimise unauthenticated disclosure of security-relevant information (5.6-2); do not
  unnecessarily expose physical interfaces (5.6-3); debug interfaces disabled or protected by
  authentication or access control (5.6-4A) and physically protected where they are physical
  ports (5.6-4B); enable only needed services (5.6-5); minimise code (5.6-6); least privilege
  (5.6-7); hardware-level memory access control (5.6-8); secure development process (5.6-9).
- **5.7 Software integrity.** Verify software with secure boot (5.7-1) and alert the user or
  administrator if an unauthorised change is detected, without connecting to wider networks
  than needed to alert (5.7-2).
- **5.8 to 5.13.** Protect personal data; make systems resilient to outages; examine system
  telemetry data; make it easy for users to delete user data; make installation and
  maintenance easy; validate input data.

## Modelling steps
1. Draw the device, local interfaces, companion app, cloud services and update server, with
   trust boundaries between them.
2. For each interface, walk the 5.5 and 5.6 provisions to find missing authentication,
   unneeded exposure and debug access.
3. For each secret, walk 5.1 and 5.4: where is it stored, is it unique per device, is it ever
   hard-coded.
4. Walk 5.3 and 5.7 along the update path from the manufacturer to the running device.
5. Record each provision as met, not applicable with justification, or a gap.

## Verify
- [ ] Every provision has a status and, where not met, a justification.
- [ ] The update path and secret storage each have a documented trust relationship.

## Checked
Confirmed 2026-11-09 against the ETSI EN 303 645 V3.1.3 PDF (converted with pdftotext): table of contents, and provisions 5.0 to 5.7 read by provision number; sections 5.8 to 5.13 confirmed by heading only.
Removed as unconfirmed: the device-surface threat catalogue (UART, JTAG, glitching, BLE Just Works, MQTT topic ACLs, IDOR, UPnP), the specific control suggestions (SBOM, secure element, rollback protection), the UK PSTI Act statement, and the NISTIR 8259A and OWASP IoT sources, which were not read.
Method: docs-checked 2026-11-09 against etsi.org EN 303 645 V3.1.3 PDF via pdftotext
