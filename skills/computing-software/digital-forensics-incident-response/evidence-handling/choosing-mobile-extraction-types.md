---
id: computing-software.digital-forensics-incident-response.evidence-handling.choosing-mobile-extraction-types
name: choosing-mobile-extraction-types
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [full-file-system-extraction, mobile-forensics, ios-forensics, android-forensics, dfir]
level: advanced
status: draft
description: "Choose between logical, backup, full file system and physical mobile extractions: what each yields, prerequisites, BFU vs AFU state and documentation."
sources: ["https://csrc.nist.gov/pubs/sp/800/101/r1/final", "https://www.swgde.org/documents/published-complete-listing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing mobile extraction types

**Goal:** select the extraction that gets the data the case needs with the access you have, and
document why (NIST SP 800-101r1 levels: manual, logical, hex dump/JTAG, chip-off, micro read).

## Extraction types today
| Type | iOS | Android | Yields |
|---|---|---|---|
| Logical / backup | iTunes/Finder backup (encrypted backup gives keychain, Health) via libimobiledevice `idevicebackup2` | ADB backup (deprecated), vendor backup, logical agent | User data apps allow in backups; no system logs, limited third-party app data |
| Advanced logical | Backup + AFC media + crash logs + sysdiagnose | Agent app via ADB pulling content providers | More, still no protected app containers |
| **Full file system (FFS)** | Via exploits/agents (checkm8 on A5-A11, commercial agents on newer) | Root/exploit-based, or vendor tools | Full app sandboxes, databases, KnowledgeC/Biome, keychain |
| Physical | Not practical on modern iOS (file-based encryption) | Older devices; chip-off/JTAG/ISP; FBE limits value | Raw flash; encrypted on modern devices |

## Device state matters
- **AFU (after first unlock)**: class keys in memory; most data decryptable by FFS tools. Keep the
  device powered and charged (and isolated) to stay AFU.
- **BFU (before first unlock)**: little user data accessible. A reboot moves AFU to BFU: avoid it.
- iOS inactivity reboot (iOS 18+) returns devices to BFU after days locked: act quickly.

## Documentation
- Device make/model/OS version, state (AFU/BFU, locked), isolation method, tool and version,
  extraction type and why, hash of the extraction output.

## Gotchas
- Choosing logical when FFS was possible misses most app data (Signal, WhatsApp full databases).
- Exploit-based extraction may modify the device; record and justify.
- Legal authority must cover the extraction scope (and cloud data reachable from the device).

## Verify
The report states the extraction type, device state, and known limits of what that type cannot contain.
