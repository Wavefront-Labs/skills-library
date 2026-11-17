---
id: computing-software.digital-privacy-hygiene.phishing-awareness.opened-a-malicious-attachment
name: opened-a-malicious-attachment
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, opened-malicious-attachment, phishing-incident-response, malware-removal]
level: practitioner
status: draft
description: "What to do after opening a suspicious attachment or enabling macros: isolate, assess what ran, scan offline, change passwords from a clean device, report."
sources:
  - "https://support.microsoft.com/windows/help-protect-my-pc-with-microsoft-defender-offline-9306d528-64bf-4668-5b80-ff533f183d6c"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
  - "https://ssd.eff.org/module/how-do-i-protect-myself-against-malware"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Opened a malicious attachment

**Goal:** limit damage in the first hour after opening something you shouldn't have.

## Assess
| What happened | Risk |
|---|---|
| Opened a PDF/Office file in protected view, nothing else | Low; delete it, run a scan |
| Clicked "Enable Content/Editing" (macros) | High: code likely ran |
| Opened a .exe/.lnk/.js/.iso or "installer" | High |
| Entered a password on a page that opened | Credential compromise (separate response) |

## High-risk steps
1. **Disconnect** from the network (Wi-Fi off, unplug Ethernet).
2. **At work:** call IT/security now; don't power off unless told (they may want memory evidence).
3. **At home:** run **Microsoft Defender Offline scan** (Windows Security > Virus & threat protection > Scan options)
   or your AV's full scan; on Mac, update and run a reputable scanner.
4. From a **different, clean device**: change passwords for email, banking, password manager; sign out all
   sessions; check email forwarding rules.
5. Watch for new logins, unknown programs, browser extensions.
6. If anything was found, or you can't be sure, back up documents (not programs) and **reinstall** the OS.

## Identify the file
Upload the **hash** (not the file if it may contain sensitive data) to VirusTotal: `Get-FileHash file`.

## Report
Forward the original email as an attachment to IT or report phishing to your provider/APWG.

## Gotchas
- Infostealers act in seconds; changing passwords from the infected PC can leak the new ones.
- Browser session cookies may be stolen: sign out everywhere, not just change passwords.
