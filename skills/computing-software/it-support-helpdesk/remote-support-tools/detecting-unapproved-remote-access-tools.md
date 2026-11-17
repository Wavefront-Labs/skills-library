---
id: computing-software.it-support-helpdesk.remote-support-tools.detecting-unapproved-remote-access-tools
name: detecting-unapproved-remote-access-tools
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, unauthorized-remote-tools, anydesk, rustdesk, shadow-it, defender-for-endpoint, kql, app-control]
level: practitioner
status: draft
description: "Find and block unapproved remote-access tools: EDR hunting queries, DNS indicators, Intune discovered apps, portable-binary blocking with WDAC/AppLocker, and follow-up."
sources:
  - "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-025a"
  - "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table"
  - "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/appcontrol"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# detecting-unapproved-remote-access-tools

## Hunt
Microsoft Defender XDR advanced hunting:
```kql
DeviceProcessEvents
| where Timestamp > ago(30d)
| where FileName in~ ("anydesk.exe","teamviewer.exe","rustdesk.exe","screenconnect.clientservice.exe",
    "ultraviewer_desktop.exe","splashtop.exe","atera_agent.exe","ngrok.exe","remoteutilities.exe")
| summarize first=min(Timestamp), last=max(Timestamp), count() by DeviceName, FileName, AccountName, FolderPath
```
- Portable copies run from Downloads or Temp without install; `FolderPath` shows that.
- Also hunt network: `DeviceNetworkEvents` / DNS logs for domains like `*.anydesk.com`,
  `*.teamviewer.com`, `*.screenconnect.com`, `*.rustdesk.com`, `*.ngrok.io`.
- Legitimate RMM from an **unknown tenant** is the dangerous case; check the instance or
  relay host against your own.

## Other sources
- Intune > Apps > Discovered apps; RMM software inventory.
- Defender for Cloud Apps: mark remote-access apps unsanctioned to block at the proxy.

## Block
- App Control for Business (WDAC) or AppLocker: allow only your approved tool by publisher;
  block others by publisher/hash. Portable EXEs make deny-lists weak; allow-listing wins.
- Proxy/DNS filter category for remote access tools, with your approved tool exempt.
- Defender "Potentially Unwanted Applications" blocking catches some.

## Respond to a hit
1. Is it a sanctioned exception (vendor support)? Check change/exception records.
2. If not: ask the user how it got there. A tool installed during a "support call" is an
   incident (see responding-to-a-remote-access-scam-victim).
3. Remove, record, and educate. Repeat offenders go to their manager under the acceptable
   use policy.

## Verify
Weekly query returns only approved tools, block policies log denies for test binaries,
and every hit has a ticket with outcome.
