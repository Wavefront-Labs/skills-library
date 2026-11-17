---
id: computing-software.cybersecurity-defensive.network-defence.download-controls
name: download-controls
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [download-controls, file-type-blocking, sandboxing, content-disarm-and-reconstruction, mark-of-the-web, web-filtering]
level: practitioner
status: docs-checked
description: "Control file downloads in the browser and OS: Edge download policies, and what Microsoft Defender SmartScreen does and does not cover."
sources: ["https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies#downloadrestrictions", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/virus-and-threat-protection/microsoft-defender-smartscreen/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File download controls

## Gateway (SWG/NGFW)
The gateway vendor page for file blocking returned 404, so gateway settings are not covered here: take file
type, sandbox, CDR and unscannable-file handling from your gateway's current documentation.

## Browser policies (Microsoft Edge)
The Edge policy reference lists `DownloadRestrictions` ("Allow download restrictions"),
`ExemptFileTypeDownloadWarnings` ("Disable download file type extension-based warnings for specified file
types on domains") and `SmartScreenEnabled` ("Configure Microsoft Defender SmartScreen"). Read each policy's
own page for its values before deploying, and keep the file-type exemption list small. Chrome's equivalent
policy page was not readable in this review.

## Microsoft Defender SmartScreen (Windows and Edge)
- Checks downloaded files against a list of reported malicious software sites and programs, and against a
  list of well-known frequently downloaded files; a file not on that list triggers a warning advising caution.
- Does reputation checks of URLs and apps, including the digital signature used to sign a file. It is
  integrated into Windows and checks files that apps, including third-party browsers and email clients,
  download and run.
- Manageable through group policy and Microsoft Intune; in Edge it blocks URLs associated with potentially
  unwanted applications.
- Limit: it does not protect against malicious files on internal locations or network shares such as UNC
  paths or SMB shares.

## Verify
- [ ] A test download from a controlled test site triggers the expected SmartScreen or policy behaviour.
- [ ] Downloads from a network share are covered by other controls, since SmartScreen does not cover them.

## Checked
Checked 2026-11-09 against the Microsoft Edge policy reference (policy names and descriptions only; the page is
an index) and the Microsoft Defender SmartScreen overview. Removed: the Palo Alto file blocking source (404),
the Chrome policies source (empty page), the policy value numbers 1, 3 and 4, WildFire and Zscaler names, the
gateway practices (true-type blocking, sandbox, CDR, encrypted archives, size limits), the HTTPS inspection and
sync client remarks, Mark-of-the-Web handling for archive tools, and the ASR rule advice.
Method: docs-checked 2026-11-09 against the Edge policy reference and SmartScreen overview.
