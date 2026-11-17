---
id: defence-public-safety.physical-and-access-security.security-locksmithing.lock-grading-master-key-systems-and-key-control
name: lock-grading-master-key-systems-and-key-control
category: defence-public-safety
field: physical-and-access-security
product: security-locksmithing
tags: [physical-and-access-security, security-locksmithing, locksmith, lock-selection, ansi-bhma, bhma-grade-1, ul-437, en-1303, en-12209, ts-007, sold-secure, master-key-system, mks, key-bitting-array, cross-keying, restricted-keyway, patented-keyway, key-control, key-register, rekeying, ic-core, interchangeable-core, lockout-authorisation, proof-of-occupancy, safe-servicing, high-security-cylinder]
level: practitioner
status: draft
description: "Locksmith's security practice: choosing lock grades (ANSI/BHMA, EN 1303, EN 12209), designing master key systems, restricted keyways, key control records, and verifying authority before lockouts."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lock grading, master key systems and key control

**Goal:** specify mechanical locks that match the risk, design a master key system
that doesn't quietly undermine itself, and keep control of every key. Reference for
locksmiths, facility managers and security specifiers. Standards and licensing rules
vary by country and state; check current editions.

## 1. Choosing locks by grade
- **US: ANSI/BHMA** grades (Grade 1 = heaviest commercial duty, 2 = light commercial/
  heavy residential, 3 = residential). Grades rate durability and strength; **UL 437**
  and ANSI/BHMA A156.30 cover high-security cylinders against manipulation and attack.
- **Europe: EN 1303** grades cylinders (key security and attack resistance digits);
  **EN 12209** covers mechanical locks; UK buyers look for **TS 007** (star ratings)
  or **Sold Secure** marks on euro-cylinders, chosen because cylinder snapping became
  a common burglary method.
- Match **door, frame, hinges, strike and lock** — a Grade 1 lock in a weak frame is
  a weak door. Fire doors need listed, compatible hardware; egress rules (panic and
  fire exit hardware) override security preferences.

## 2. Master key system design
A master key system (MKS) lets one key open many locks while change keys open one.
- Map the **hierarchy** from the organisation's real access needs: grand master →
  masters per building or department → change keys per door.
- Each master level **reduces** the security of the cylinders (more shear lines or
  key combinations work), and increases the effect of a lost master key. Keep the
  system as shallow as the organisation allows.
- Build from a **key bitting array** and record it; avoid accidental **cross-keying**
  (a change key unintentionally opening another door). Use manufacturer system-design
  services for larger systems.
- Leave capacity for growth; re-designing a mature system is expensive.
- **Interchangeable cores (IC)** let you re-core a door in seconds after a key loss —
  valuable for large sites.

## 3. Key control
- **Restricted or patented keyways** so blanks are only available through the
  authorised dealer with the owner's authorisation (patent protection expires —
  check how long is left).
- **Key register:** key number, holder, issue date, signature, return. Stamp keys
  with a code, not the door name; "Do Not Duplicate" stamps alone are not enforcement.
- Audit periodically; recover keys on leaving; rekey after an unrecovered master.
- Consider electronic access control (see
  `defence-public-safety.physical-and-access-security.access-control-systems.credential-lifecycle-and-access-policy-administration`)
  where frequent change or audit trails are needed.

## 4. Lockouts and authority
Professional practice (and many licensing regimes) requires checking **authority
before opening**: photo ID matching the address, proof of occupancy (lease, utility
bill), vehicle registration, or police presence when in doubt. Record the job
details. Refuse when authority can't be shown — a locksmith opening a door for the wrong
person can be liable. (Specific legal requirements vary by jurisdiction.)

## 5. Safes (outline)
Safe ratings: UL 687 / TL-15, TL-30 (US) or EN 1143-1 grades (Europe), with insurers
setting cash limits per grade. Servicing — combination changes, lock replacement —
follows manufacturer procedures and the customer's authorisation.

## Gotchas
- A beautiful high-security cylinder with an exposed, unprotected screw-on escutcheon.
- Masters handed out "temporarily" and never returned.
- Electronic and mechanical override keys forgotten in the key register.

## Verify
- [ ] Lock grade and door assembly match the assessed risk and fire/egress rules.
- [ ] MKS hierarchy documented with a bitting array; no unintended cross-keying.
- [ ] Every key logged to a person; audit date set.
- [ ] Authority checked and recorded before any lockout service.
