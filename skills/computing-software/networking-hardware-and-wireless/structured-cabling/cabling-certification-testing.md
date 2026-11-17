---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-certification-testing
name: cabling-certification-testing
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [cabling-certification, permanent-link-test, next-return-loss, cabling-testing]
level: advanced
status: draft
description: "Run a certification tester to the right limit (permanent link or channel), read NEXT, return loss, insertion loss and fix common faults."
sources:
  - https://tiaonline.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certifying copper

- A wiremap tool only finds opens/shorts/miswires. Certification measures insertion loss, NEXT, PSNEXT, ACR-F, return loss, propagation delay/skew and length against a TIA limit.
- Choose the correct test limit: Permanent link or Channel, and the right category (e.g. Cat6A). Using the wrong limit passes bad links or fails good ones.
- Set the correct NVP for the cable; a wrong NVP gives wrong length.
- Return loss failures often point to a bad termination or a patch cord; NEXT failures to untwisted pairs or a poorly seated jack.
- Save the reports; they document acceptance and warranty claims.
- Reference-calibrate adapters regularly per vendor guidance.

## Verify
- [ ] Every link has a stored pass report with the stated limit, tester model and firmware/reference date.
