---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.dpapi-master-key-and-secret-theft
name: dpapi-master-key-and-secret-theft
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [dpapi-masterkey, credential-theft, dpapi, browser-cookies, dfir]
level: advanced
status: draft
description: "Investigate DPAPI abuse: master key files, domain backup key theft, offline decryption of browser and credential manager secrets, and the evidence it leaves."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/dpapi/", "https://attack.mitre.org/techniques/T1555/004/", "https://github.com/gentilkiwi/mimikatz/wiki/howto-~-credential-manager-saved-credentials"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DPAPI master key and secret theft

**Goal:** DPAPI protects browser cookies/passwords (Chromium `Local State` key), Credential Manager,
Wi-Fi keys, RDP saved credentials and many app secrets. Attackers steal master keys or the domain
DPAPI backup key to decrypt them offline. Investigators use the same mechanics to scope what was exposed.

## Pieces
| Item | Location |
|---|---|
| User master keys | `%APPDATA%\Microsoft\Protect\<UserSID>\<GUID>` (and `Preferred`) |
| System master keys | `%SystemRoot%\System32\Microsoft\Protect\S-1-5-18\` |
| Credential blobs | `%APPDATA%\Microsoft\Credentials\`, `%LOCALAPPDATA%\Microsoft\Credentials\`, `Vault\` |
| Chromium | `Local State` `os_crypt.encrypted_key` (DPAPI-wrapped AES key; app-bound encryption on recent Chrome adds a SYSTEM layer) |
| Domain backup key | On DCs (LSA secret `G$BCKUPKEY_...`); lets anyone holding it decrypt any domain user's master key |

## Attacker evidence
- **Domain backup key theft**: `lsadump::backupkeys` via MS-BKRP/LSA RPC to a DC - DC Security
  event **4662** with object `BCKUPKEY` secret access, or 5145 / RPC to `\pipe\lsarpc` from a non-DC admin
  host; Mimikatz/SharpDPAPI command lines on the source.
- **Master key access**: process reading many `Protect\` and `Credentials\` files (EDR file events; Sysmon 11 does not show reads, use SACL auditing 4663 if configured).
- Tools on disk/prefetch: `SharpDPAPI.exe`, `mimikatz.exe`, `donpapi`, `dploot` (Python, remote via SMB - shows as 5145 reads of `\Users\*\AppData\...\Protect` over ADMIN$/C$).

## Scoping what was decrypted (authorised IR only)
- With the user's password or the domain backup key held by the defender, `dpapi.py`
  (Impacket) or SharpDPAPI can decrypt master keys and then credential blobs to list which
  secrets existed - those are the secrets to rotate.

## Response
- Backup key theft is effectively permanent compromise of all DPAPI secrets in the domain; Microsoft
  does not support rotating the domain backup key in place - plan for secret rotation at scale and,
  in severe cases, domain migration.

## Gotchas
- Reading DPAPI blobs requires care: decryption outputs are themselves sensitive evidence; protect them.
- Chrome app-bound encryption (v127+) changes the attack chain (requires SYSTEM or injected browser).

## Verify
Exposed secret inventory is built and each secret is rotated or confirmed unused.
