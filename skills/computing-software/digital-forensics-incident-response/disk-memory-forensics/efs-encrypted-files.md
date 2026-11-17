---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.efs-encrypted-files
name: efs-encrypted-files
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [efs, ntfs, encrypted-volume, dpapi, dfir]
level: advanced
status: docs-checked
description: "Handle EFS-encrypted files in investigations: the $EFS logged utility stream, DDF and DRF key fields, who can decrypt, recovery agents and what cannot be encrypted."
sources: ["https://learn.microsoft.com/en-us/windows/win32/fileio/file-encryption", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/certificates-and-public-key-infrastructure-pki/back-up-recovery-agent-efs-private-key", "https://flatcap.github.io/linux-ntfs/ntfs/attributes/logged_utility_stream.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EFS-encrypted files

**Goal:** the Encrypting File System gives cryptographic protection to individual files on NTFS volumes using a public-key
system. In an image such files are ciphertext; you need to know who can decrypt them and how.

## How EFS protects a file
- A file encryption key (FEK) is generated dynamically to encrypt the file. The FEK is encrypted with the user's EFS public key
  and stored with the file as an EFS attribute, the Data Decryption Field (DDF). Decrypting needs the matching EFS private key to
  recover the FEK.
- Every time a file is encrypted the FEK is also encrypted with the recovery agent's public key and attached in the Data Recovery
  Field (DRF). The recovery agent's private key can therefore decrypt the FEK and the file if the user's key is lost.
- On NTFS this lives in the `$LOGGED_UTILITY_STREAM` attribute (type 0x100): all encrypted files have it, with the name `$EFS`.
  Its internal layout is not documented on the cited NTFS page ("contents depend on the name of the $DATA stream"), so parse it
  with a tool you have validated.

## Limits and behaviours (Win32 file encryption page)
- Compressed files, system files, system directories, root directories and transactions cannot be encrypted. Sparse files can.
- Whether a volume supports encryption is exposed through the `FS_FILE_ENCRYPTION` flag of `GetVolumeInformation`.
- When the source is encrypted, `CopyFile` and `CopyFileEx` rely on the EFS service (in lsass.exe), impersonating the caller, to
  create the target and apply the keys.
- The raw encryption functions exist so encrypted files can be backed up and restored without decrypting them.

## Decrypt options (authorised only)
1. Collect as the user in a live session: the file is decrypted transparently for the owning user.
2. Recovery agent: the agent's certificate shows "File Recovery" in the Intended Purposes column. By default a domain's recovery
   agent is the built-in Administrator on the first domain controller, with the public certificate delivered by Default Domain
   Policy (Computer Configuration, Windows Settings, Security Settings, Public Key Policies). If that profile or the first DC is
   gone the key is lost and files cannot be recovered through that agent. A workgroup Windows XP machine has no default agent.
3. The user's private key (not covered by the cited pages; see the DPAPI skill for how it is protected).

## Gotchas
- Moving files across file systems or accounts may fail or decrypt depending on context: document the exact method used.
- Handle recovery-agent keys as highly sensitive: possession lets someone read the encrypted data.

## Verify
The report lists which users and recovery agents can decrypt each relevant file and the method used to reach plaintext.

## Checked
Date: 2026-11-08.
Confirmed in the Win32 file encryption page: public-key protection of NTFS files, non-encryptable items, sparse files,
`FS_FILE_ENCRYPTION`, copy behaviour via the EFS service, raw backup functions. Confirmed in the recovery-agent article: FEK, DDF,
DRF, default recovery agent rules, "File Recovery" purpose, policy location. Confirmed in the NTFS page: `$LOGGED_UTILITY_STREAM`
0x100 used by EFS under the name `$EFS`.
Removed (not on the cited pages): `cipher /c`, MFTECmd/istat usage, `FILE_ATTRIBUTE_ENCRYPTED` detail, certificate thumbprints in
the stream, the DPAPI key path and named tools, the ransomware-abuse section, and the BackupRead/FAT claims.
Method: docs-only read of cited pages, 2026-11-08
