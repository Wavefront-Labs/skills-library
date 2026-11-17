---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-licensing-and-dynamic-updates
name: pan-os-licensing-and-dynamic-updates
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [dynamic-updates, pan-os, licenses, content-updates, antivirus-updates, threat-prevention, app-id-content, wildfire-updates]
level: practitioner
status: draft
description: "Fetch PAN-OS licences and schedule content updates (Applications and Threats, antivirus, WildFire) with CLI checks and the right ordering."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/software-and-content-updates/dynamic-content-updates"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: licensed subscriptions active and App-ID / threat content current without breaking policy.

```
request license fetch auth-code <AUTH-CODE>
request license info
request content upgrade check
request content upgrade download latest
request content upgrade install version latest
request anti-virus upgrade check
request anti-virus upgrade download latest
request anti-virus upgrade install version latest
```

Scheduling (Device > Dynamic Updates > Schedule): set Applications and Threats to download-and-install with a threshold of 24 hours on production so new App-IDs are not enforced the moment they publish. Use a shorter interval for threat signatures, and verify the schedule appears in `show config running | match update-schedule`.

Gotchas
- New App-ID content can re-classify traffic (a previously `ssl` flow becomes a named app) and silently change which rule matches. Review the release notes and the Policy Optimizer new-App-ID view after install (confirm menu name in your release).
- A content package needs a minimum PAN-OS version; downloads for a package newer than the OS supports fail with a version error.
- In HA, install content on both peers or use the same schedule with the sync-to-peer option (confirm per release).

## Verify
```
show system info | match "app-version|av-version|threat-version"
request license info
show jobs all
```
Licences should show an expiry date in the future and the job should report FIN / OK.
