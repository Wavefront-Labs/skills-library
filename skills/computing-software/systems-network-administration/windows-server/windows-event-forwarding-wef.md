---
id: computing-software.systems-network-administration.windows-server.windows-event-forwarding-wef
name: windows-event-forwarding-wef
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-auditing, windows-event-forwarding, wef, wecsvc, source-initiated-subscription, wecutil, event-collector]
level: advanced
status: docs-checked
description: "Build Windows Event Forwarding with source-initiated subscriptions: collector setup, GPO for sources, subscription XML, Event Log Readers access and scaling."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/use-windows-event-forwarding-to-assist-in-intrusion-detection
  - https://learn.microsoft.com/en-us/windows/win32/wec/setting-up-a-source-initiated-subscription
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Event Forwarding (source-initiated)

## Collector
```powershell
wecutil qc /q                         # Windows Event Collector service, auto start
winrm quickconfig -q
```
Create a subscription (Event Viewer > Subscriptions > Create, "Source computer
initiated") or from XML:
```powershell
wecutil cs '<vol>:\WEF\Security-Core.xml'      # create from XML
wecutil gs Security-Core              # status
wecutil gr Security-Core              # runtime status per source
```
Subscription essentials: computer groups allowed (e.g. Domain Computers, Domain
Controllers), XPath query, delivery option (Normal: batch timeout 15 minutes; Minimize Latency: batch timeout 30 seconds; Minimize Bandwidth),
destination log (ForwardedEvents or a custom log).

## Sources (GPO)
- Computer Configuration > Administrative Templates > Windows Components > Event
  Forwarding > **Configure target Subscription Manager**:
  `Server=<http|https>://<collector FQDN>:<port>/wsman/SubscriptionManager/WEC,Refresh=<seconds>` (the HTTPS form also takes `IssuerCA=<thumbprint>`; see the source-initiated page)
- WinRM service automatic (Preferences > Services or System Services).
- Add `NT AUTHORITY\NETWORK SERVICE` to the **Event Log Readers** group so the forwarder can read the Security log
## Query content (start small)
Forward high-value events, not everything. Microsoft's intrusion-detection WEF page has sample queries (for example
log-cleared events 1102 and 1100 from the Security log); start from those and add event IDs as detections need them.

## Scale and health
- Size the ForwardedEvents (or custom) log for your volume and ship it on to a SIEM.
- Check each source with `wecutil gr <subscription>` (runtime status per source) and `wecutil gs <subscription>`.
- Learn's HTTPS example uses a separate port and certificate settings; for non-domain sources follow that page.

## Verify
- [ ] `wecutil gr <sub>` lists sources as Active.
- [ ] Test event (`eventcreate /id 999 /l application /t information /d test`) arrives if in the query.

## Checked
2026-10-28. Confirmed on Learn pages (source-initiated subscription setup, WEF intrusion-detection, wecutil reference):
`winrm quickconfig`/`wecutil qc /q`, Subscription Manager GPO string form with Refresh, NETWORK SERVICE and Event Log
Readers, delivery options 15 min / 30 s, `wecutil gs` and `gr`. Removed as unconfirmed: DC Security channel SDDL,
4 GB log size and sources-per-collector figure, forwarding-plugin channel event numbers, the Kerberos/5985 encryption
claim, the event-ID shopping list and named third-party query packs.
Method: documentation only; no commands were run.
