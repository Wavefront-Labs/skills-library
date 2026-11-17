---
id: computing-software.general-digital-literacy.web-browsers.checking-a-download-is-genuine
name: checking-a-download-is-genuine
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, downloads, verify-download, file-hash, sha256, notarization]
level: practitioner
status: verified
description: "Check a downloaded installer: official source, Mac notarisation, SHA-256 checksum with certutil or Get-FileHash, and VirusTotal as a second opinion."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
  - https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web
  - https://docs.virustotal.com/docs/how-it-works
  - https://support.google.com/chrome/answer/2765944
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Check a download is genuine

## 1. Source
Chrome's guidance: get a program from its official website, not from a pop-up about a program update or download; avoid downloading from sites that do not use HTTPS; pay attention to Safe Browsing download warnings.

## 2. Mac: notarisation
Apple's platform security guide: Gatekeeper checks that software is notarised, meaning Apple checked it for malicious software and found none. Software that is not notarised may expose the Mac to malware.

## 3. Checksum (when the publisher lists one)
- Windows Command Prompt: `certutil -hashfile <file> SHA256` (certutil's hash algorithms include MD2, MD4, MD5, SHA1, SHA256, SHA384 and SHA512).
- Windows PowerShell: `Get-FileHash <file>`; by default it uses SHA256.
- certutil prints lowercase hex and `Get-FileHash` prints uppercase hex for the same file, so compare case-insensitively.
- `certutil -hashfile <file> SHA3` fails (not a supported algorithm; non-zero exit).
- Compare every character with the value on the publisher's official site. A match shows the file is the one the publisher listed, provided the page showing the checksum is itself genuine.

## 4. Second opinion
VirusTotal aggregates results from many antivirus engines and can help identify false positives (harmless items flagged by some scanners). Its scanning reports are shared with the public VirusTotal community, so do not upload private documents.

## Verify
- [ ] The SHA-256 matches the published value and the source is the publisher's own site.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn (Get-FileHash, certutil), Apple Platform Security (Gatekeeper and runtime protection), VirusTotal documentation ("How it works"), Chrome Help ("Remove unwanted ads, pop-ups & malware"), read in October 2026. Confirmed: the certutil syntax and algorithm list, Get-FileHash default SHA256, notarisation meaning, VirusTotal aggregation and public sharing of reports, Chrome's sourcing tips. Removed as unconfirmed: the Windows Digital Signatures tab and "Verified publisher" steps, spctl and codesign commands, the shasum command, and the advice on weak MD5 and SHA-1.
Run 2026-11-01 (Windows 11, Windows PowerShell 5.1): `certutil -hashfile <file> SHA256` printed the digest and exited 0; MD2, MD4, MD5, SHA1, SHA384 and SHA512 also worked; `SHA3` failed with STATUS_NOT_FOUND. `Get-FileHash <file>` with no `-Algorithm` reported Algorithm SHA256 and the same digest as certutil (uppercase). `Get-AuthenticodeSignature` on a Microsoft-signed system file gave Status Valid. The Mac and Chrome statements, VirusTotal behaviour and the publisher-comparison advice are documentation-confirmed above (not runnable here).
Method: documentation for the Mac, Chrome and VirusTotal claims; the Windows commands were run.
