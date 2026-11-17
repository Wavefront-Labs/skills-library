---
id: computing-software.digital-forensics-incident-response.incident-response-process.incident-jump-kit
name: incident-jump-kit
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [jump-kit, ir-preparation, incident-readiness, forensic-tools, write-blocker, dfir]
level: practitioner
status: draft
description: "Assemble and maintain an incident response jump kit: hardware, write blockers, media, boot tools, collection software, paperwork and offline documentation."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.sans.org/posters/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident jump kit

**Goal:** a responder can leave within 30 minutes with everything needed to collect evidence
on site, without borrowing from the compromised environment (NIST SP 800-61r2 3.1.1 lists
handler hardware, software and documentation).

## Hardware
- Forensic laptop (encrypted, not domain-joined, fully patched, admin rights) plus charger.
- Hardware write blockers: SATA/SAS, USB, NVMe/PCIe (Tableau or WiebeTech) and adapters
  (M.2, mSATA, IDE, Apple SSD).
- Wiped and hash-verified target drives, larger than the evidence (2x the biggest disk you
  expect); a few high-speed USB 3 / Thunderbolt NVMe enclosures.
- USB sticks with collection tools (one per host, never reused without wiping), labelled.
- Network: small managed switch with SPAN, network TAP, patch and crossover cables, USB
  Ethernet adapters.
- Faraday bags for phones, camera, anti-static bags, evidence bags, tamper-evident tape,
  labels, permanent markers, screwdriver set (Torx, pentalobe), torch.

## Software (on separate media)
- Memory: WinPmem, DumpIt/Magnet RAM Capture, LiME modules, AVML.
- Triage: KAPE, Velociraptor offline collector, UAC, CyLR.
- Imaging: FTK Imager (portable), ewfacquire, dc3dd, a Linux forensic boot ISO (Paladin,
  CAINE, Tsurugi) on Ventoy.
- Analysis: SIFT VM, Eric Zimmerman tools, Volatility 3, Wireshark, hash tools.

## Paperwork
Chain-of-custody forms, evidence log, interview notes templates, the printed IR plan and
contact sheet, legal authorisation templates, notebook (bound, numbered pages).

## Maintenance
- Quarterly: update tools, re-verify hashes of tool media, wipe and re-verify target drives,
  test boot media on current hardware (Secure Boot, new NVMe controllers).
- Inventory list taped inside the case; sign-out log for when it leaves.

## Gotchas
- BitLocker/Secure Boot block many boot ISOs; carry recovery-key procedures and plan live
  acquisition instead.
- Tools signed by expired certificates may be blocked by EDR; pre-approve hashes with the EDR team.

## Verify
Do an unannounced drill: image a test laptop and capture its RAM using only kit contents.
