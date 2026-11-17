---
id: computing-software.networking-hardware-and-wireless.check-point.threat-emulation-and-extraction
name: threat-emulation-and-extraction
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, threat-emulation, sandbox, threat-extraction]
level: practitioner
status: draft
description: "Enable Check Point Threat Emulation (cloud or local sandbox) and Threat Extraction (CDR) for files in web and mail traffic."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ThreatPrevention_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat Emulation and Threat Extraction

- **Threat Emulation** sends supported files (PDF, Office, archives, executables) to a sandbox: ThreatCloud emulation (default, cloud), or a local **SandBlast Appliance**. Choose in the gateway object > Threat Emulation > Emulation Location.
- **Threat Extraction** (Content Disarm & Reconstruction) removes active content (macros, embedded objects) and delivers a clean copy, or converts to PDF, while the original is emulated in the background. It requires both HTTP and (for mail) MTA or mail-forwarding configuration.
- Set it up in **Threat Prevention > Profiles > Threat Emulation / Threat Extraction**: choose `Prevent` (hold the file until a verdict) or `Detect`/`Background` (deliver and block later), supported file types, maximum file size (default 15 MB, confirm), and exception sources.
```
mgmt_cli -r true set threat-profile name "Prof_DMZ" threat-emulation true threat-extraction true
mgmt_cli -r true publish
cpstat threat-emulation -f general   # (confirm)
```
- For mail, enable **MTA** on the gateway (Mail Transfer Agent) or deploy as an inline relay with `smtp`. HTTPS Inspection is needed to see HTTPS downloads.
- Privacy/legal: files leaving for cloud emulation may include sensitive content; use local sandbox or restrict file types and sources where policy requires.
- Gotcha: "Prevent" holds the download until the verdict (up to a minute), causing browser timeouts for large files; start with Background mode on user subnets.

Verify: download the Check Point sample or a macro test document; log shows `Verdict`, and the user receives the cleaned `.pdf` copy for Extraction.
