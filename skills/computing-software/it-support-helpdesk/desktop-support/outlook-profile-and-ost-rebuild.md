---
id: computing-software.it-support-helpdesk.desktop-support.outlook-profile-and-ost-rebuild
name: outlook-profile-and-ost-rebuild
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, microsoft-365, m365-support, outlook-profile, ost, cached-exchange-mode, autodiscover, outlook-safe-mode, scanpst, new-outlook, outlook-search-index, autodiscover-troubleshooting, pst-recovery, office-add-ins]
level: practitioner
status: draft
description: "Fix classic Outlook that won't open, sync or search: safe mode and add-ins, new mail profile, OST rebuild, Autodiscover checks, search index rebuild, and the new Outlook toggle."
sources:
  - "https://support.microsoft.com/en-us/office/create-an-outlook-profile-f544c1ba-3352-4b3b-be0b-8d42a540459d"
  - "https://learn.microsoft.com/en-us/troubleshoot/outlook/performance/outlook-not-starting"
  - "https://learn.microsoft.com/en-us/microsoft-365/troubleshoot/administration/microsoft-support-recovery-assistant"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# outlook-profile-and-ost-rebuild

Goal: get classic Outlook working without losing anything — mailbox data is
on Exchange Online; the local OST is a disposable cache (except PSTs).

## Order of operations
1. **Webmail check** (outlook.office.com): if mail is missing there too, the
   problem is the mailbox/rules, not Outlook.
2. **Safe mode**: `outlook.exe /safe`. Opens fine → an add-in. File →
   Options → Add-ins → COM Add-ins → Go → untick, re-enable one by one.
   Teams Meeting add-in, PDF and CRM add-ins are frequent offenders.
3. **New profile**: Control Panel → Mail (Microsoft Outlook) → Show Profiles
   → Add → set "Always use this profile" to the new one. This rebuilds the
   OST from the server. Keep the old profile until confirmed.
4. **Microsoft Support and Recovery Assistant (SaRA / Get Help)** automates
   most of the above and collects logs.

## OST rebuild
OST location: `%LOCALAPPDATA%\Microsoft\Outlook\<address>.ost`. Close Outlook,
rename it to `.old`, reopen — Outlook redownloads. For a large mailbox
set the cached-mode slider (Account settings → Change → "Download email for
the past") to 6–12 months first to keep the resync fast. Never use
`scanpst.exe` on an OST to "fix" sync; it's for PST files.

## Autodiscover
Profile creation hangs or asks for passwords repeatedly →
`Ctrl+right-click Outlook tray icon → Test E-mail AutoConfiguration` (untick
Guessmart). Should resolve `outlook.office365.com`. Stale on-premises
SCP/DNS records after migration send it the wrong way — fix DNS
(`autodiscover` CNAME) rather than registry hacks where possible.

## Search
"Search results may be incomplete": Indexing Options → Advanced → Rebuild
(hours), or check Outlook is listed under indexed locations. Search in the
online archive needs server search, works only online.

## New Outlook
The "New Outlook" toggle switches to a different client (web-based, no
COM add-ins, no PST import in older builds). If a user's add-in vanished,
check whether they toggled.

## Gotchas
- PSTs attached to the old profile must be re-added to the new one — list
  them first (Account Settings → Data Files).
- Shared mailbox auto-mapped with Full Access is cached into the user's OST
  and can bloat it; consider not caching shared folders.
- Credential prompts loop: clear Windows Credential Manager entries for
  `MicrosoftOffice16_Data:*` and check modern auth / WAM (Accounts in
  Windows settings).

## Verify
Outlook opens in normal mode, Send/Receive shows "All folders are up to
date", search returns recent items, and the user's calendar/shared
mailboxes appear.
