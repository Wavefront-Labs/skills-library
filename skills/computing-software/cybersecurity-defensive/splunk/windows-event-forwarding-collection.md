---
id: computing-software.cybersecurity-defensive.splunk.windows-event-forwarding-collection
name: windows-event-forwarding-collection
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, windows-event-forwarding, wef, wec, windows-event-collection, wineventlog, inputs-conf, subscription]
level: practitioner
status: draft
description: "Collect Windows event logs at scale with Windows Event Forwarding to collectors or forwarder WinEventLog inputs, with subscriptions, filtering and coverage checks."
sources: ["https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/use-windows-event-forwarding-to-assist-in-intrusion-detection", "https://docs.splunk.com/Documentation/Splunk/latest/Data/MonitorWindowseventlogdata", "https://github.com/palantir/windows-event-forwarding"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows event log collection (WEF or forwarder inputs)

**Goal:** every Windows host's security-relevant logs reach the SIEM, with a known way to
tell when one stops.

## Choose the pattern
- **Forwarder on every host:** UF with `WinEventLog` inputs. Fine-grained per-host control,
  but another agent to deploy and patch.
- **WEF:** built-in agentless push (WinRM) from hosts to Windows Event Collector (WEC)
  servers; a UF on each WEC reads `ForwardedEvents`. Fewer agents, central filtering.
Many estates use WEF for workstations and UF on servers and domain controllers.

## WEF setup
1. Collector: `wecutil qc` (enables Windows Event Collector service). Size about 2,000-4,000
   clients per collector with source-initiated subscriptions.
2. GPO for sources: Computer Configuration > Administrative Templates > Windows Components >
   Event Forwarding > *Configure target Subscription Manager*:
   `Server=http://wec01.example.internal:5985/wsman/SubscriptionManager/WEC,Refresh=60`
3. Give `NETWORK SERVICE` read on the Security log: add
   `(A;;0x1;;;NS)` to the channel access SDDL (GPO *Configure log access*), or add the
   account to Event Log Readers.
4. Subscription (XML, imported with `wecutil cs sub.xml`): source-initiated, target
   domain computers group, XPath query selecting the event IDs you need, `ContentFormat`
   `RenderedText` only if the UF needs messages (otherwise `Events` is smaller).
5. Delivery mode `MinLatency` for security events, `Normal` for bulk.

## Splunk forwarder input
```
[WinEventLog://Security]
disabled = 0
renderXml = true
evt_resolve_ad_obj = 0
blacklist1 = EventCode="4662" Message="Object Type:\s+(?!groupPolicyContainer)"

[WinEventLog://ForwardedEvents]
disabled = 0
renderXml = true
```
`renderXml = true` with the Splunk Add-on for Windows gives `XmlWinEventLog` sourcetype,
smaller and parsed consistently. Avoid `evt_resolve_ad_obj` at scale (LDAP lookups per event).

## Gotchas
- Forwarded events keep the original `Computer` field; in Splunk use `host` from the event
  (the TA does this) not the collector name.
- Large subscriptions on one collector hit the WinRM/HTTP.sys limits; split by event channel.
- Sysmon and PowerShell Operational need their own channel entries in the subscription.

## Verify
```
wecutil gr <subscription>      # per-source runtime status, last heartbeat
| tstats count where index=wineventlog by host | where count < 10
```
Compare the host list against AD computer objects active in the last 7 days.
