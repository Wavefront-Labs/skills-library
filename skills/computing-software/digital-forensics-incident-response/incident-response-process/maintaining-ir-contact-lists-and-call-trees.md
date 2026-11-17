---
id: computing-software.digital-forensics-incident-response.incident-response-process.maintaining-ir-contact-lists-and-call-trees
name: maintaining-ir-contact-lists-and-call-trees
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [call-tree, contact-list, ir-preparation, escalation, out-of-band, dfir]
level: practitioner
status: draft
description: "Maintain incident response contact lists and call trees: internal and external contacts, out-of-band copies, quarterly verification and call-tree drills."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/resources-tools/resources/incident-response-plan-irp-basics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintaining IR contact lists and call trees

SP 800-61r2 3.1.1 lists contact information for team members, on-call, law enforcement, other IR teams and vendors as core preparation. Stale numbers are found in real incidents, so verification is the actual work.

## Contents
- **Internal**: IR team and deputies, incident commander rota, CISO, CIO, Legal, Privacy/DPO, Comms/PR, HR, facilities/physical security, executive sponsor, key system owners (from the crown-jewel register).
- **External**: IR retainer hotline and contract number, cyber insurer claim line and panel counsel, MSSP/MDR, cloud provider support (with account IDs and support plan level), ISP/DDoS provider, law enforcement contacts (local cyber unit, FBI field office / national CERT), regulators, ISAC, key SaaS vendors.
- For each: role, primary and backup person, mobile, personal email or Signal for out-of-band, time zone, what they can authorise.

## Call tree
A tree, not a broadcast: the IR lead calls the commander and Legal; the commander calls exec and comms; each caller confirms contact and reports back within a set time. Write the "no answer" rule (try backup after 10 minutes, then the next level up).

## Keeping it alive
1. Store it in at least three places: the IR platform, an offline printed copy in the jump kit, and an out-of-band location (e.g. a secured personal-device app) that works if corporate email and AD are down.
2. Verify quarterly: automated test page or SMS with acknowledgement, plus HR leaver/joiner feed to flag changes.
3. Run a call-tree drill twice a year, timing how long until all tier-1 contacts acknowledge.
4. Update immediately on role changes; version and date every copy.

## Gotchas
- Corporate softphones and Teams numbers fail when the identity provider is compromised; mobile numbers are mandatory.
- External contacts expire too: retainer contract numbers and insurer policy numbers change at renewal.
- The list holds personal data; restrict and protect it accordingly.

## Verify
Last drill timestamp is within six months, all tier-1 contacts acknowledged within the target time, and the printed copy matches the current version number.
