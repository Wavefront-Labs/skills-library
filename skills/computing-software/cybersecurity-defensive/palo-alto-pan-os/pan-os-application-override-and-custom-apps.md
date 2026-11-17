---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-application-override-and-custom-apps
name: pan-os-application-override-and-custom-apps
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [application-override, pan-os, custom-application, app-override-policy, proprietary-protocol]
level: practitioner
status: draft
description: "Create PAN-OS application override rules and custom applications for proprietary protocols, and understand what inspection override disables."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/app-id/use-application-objects-in-policy/create-a-custom-application"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: force a specific application label on traffic the signature engine cannot classify, accepting the loss of deep inspection.

```
configure
set application corp-erp category business-systems subcategory database technology client-server risk 2
set application corp-erp default port [ tcp/9443 ]
set rulebase application-override rules erp-override from trust to dmz source any destination 10.1.2.20 protocol tcp port 9443 application corp-erp
commit
```
Prefer a custom application with a signature (pattern match on the first bytes) over override, because override bypasses App-ID and Content-ID: no threat, URL or file inspection on that traffic, only the security rule matching.

Where it is appropriate: internal UDP/TCP protocols with no signature, flows that fail inspection because of non-standard framing, high-volume trusted backup traffic where inspection is deliberately skipped.

Gotchas
- The override rule is evaluated before App-ID, so scope it narrowly by source, destination and port.
- Security rules must still allow the custom application name.
- The application-override match occurs on session creation; changing a rule does not affect existing sessions (clear the session).

## Verify
```
show session all filter application corp-erp
```
The traffic log should show the custom application, and threat logs should be empty for it (confirming inspection is bypassed as intended).
