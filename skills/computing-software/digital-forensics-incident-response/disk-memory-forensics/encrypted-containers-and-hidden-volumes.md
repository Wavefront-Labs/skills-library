---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.encrypted-containers-and-hidden-volumes
name: encrypted-containers-and-hidden-volumes
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [veracrypt, anti-forensics, encrypted-volume, steganography, dfir]
level: advanced
status: draft
description: "Find and handle encrypted containers (VeraCrypt, BitLocker To Go, 7z/AES): detection by entropy and artefacts, mounted-volume evidence, hidden volume questions."
sources: ["https://veracrypt.fr/en/Hidden%20Volume.html", "https://www.sans.org/posters/windows-forensic-analysis/", "https://github.com/veracrypt/VeraCrypt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encrypted containers and hidden volumes

**Goal:** identify that encrypted containers exist and were used, recover what can be shown
about their contents, and capture keys while systems are live.

## Detecting containers
- VeraCrypt/TrueCrypt containers have no header signature: look for large files with size a
  multiple of 512, near-maximal entropy (~8.0 bits/byte across the file), no recognisable format,
  often with innocuous extensions. Tools: `ent`, entropy views in Autopsy/X-Ways, `densityscout`.
- Program evidence: VeraCrypt installed or portable (`VeraCrypt.exe`, `veracrypt.sys` driver),
  prefetch, Amcache, UserAssist; `%APPDATA%\VeraCrypt\Configuration.xml`, `History.xml` (if history enabled: recently mounted container paths).
- Registry `MountedDevices` entries with `\??\Volume{...}` for VeraCrypt volumes; shellbags and LNK files pointing to drive letters with volume serials not matching any physical device.

## Live system first
- If a container is mounted, image the **mounted logical volume** (it is decrypted) and capture
  memory: VeraCrypt master keys reside in RAM; some tools (Passware, `volatility` plugins for TrueCrypt on older versions) extract them.
- Hibernation file/pagefile may hold keys if the system hibernated while mounted.

## Hidden volumes
- A VeraCrypt hidden volume lives inside the free space of an outer volume and is undetectable by design.
  Indicators are circumstantial: outer volume with old/few files and much "free space" with high entropy,
  usage artefacts (file paths on that drive letter) inconsistent with the outer volume's contents.
  Report as a possibility with stated limits; do not overclaim.

## Other encryption
- BitLocker To Go: `-FVE-FS-` signature in the VBR; recovery keys may be escrowed in AD/Entra (`msFVE-RecoveryInformation`).
- Encrypted archives (7z/ZIP AES): headers are recognisable; password cracking may be authorised.

## Gotchas
- High entropy alone also fits compressed media and random swap; corroborate with usage artefacts.
- Compelled disclosure of passwords is a legal question; route through counsel.

## Verify
Report lists container candidates with entropy and usage evidence, and live-captured keys/volumes where obtained.
