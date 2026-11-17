---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-app-id-and-dependencies
name: pan-os-app-id-and-dependencies
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [app-id, pan-os, application-identification, application-dependencies, unknown-tcp, application-incomplete, policy-optimizer]
level: practitioner
status: draft
description: "Use PAN-OS App-ID correctly - dependencies, shifting application identity mid-session, unknown-tcp and incomplete - and tighten port rules to applications."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/app-id"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: policy by application, not port, without breaking apps that need helper applications.

How it works: signatures, protocol decoders, heuristics and decryption classify a session; the application can change after the first packets (ssl then a named SaaS app), and rules are re-evaluated when it does.

Workflow to move a port-based rule to App-ID
1. Clone the legacy rule above itself with applications `any` and log-end on.
2. Watch traffic logs (or Policy Optimizer > No App Specified) for the applications seen.
3. Replace `any` with the observed list and `service application-default`.
4. Remove the legacy rule once hit count falls to zero.

```
show session all filter application ssl
show session all filter application unknown-tcp
show session id <ID>
```
Application details (dependencies, standard ports, risk) are in Objects > Applications or `show running app-details` style output (confirm). Dependencies are listed in the application page "Depends on"; add them to the same rule.

Gotchas
- `unknown-tcp` / `unknown-udp` means no signature matched: often custom apps, or encrypted payload without decryption; do not simply allow it.
- `incomplete` means the handshake never finished or too little data arrived; usually a routing or asymmetry problem, not an application.
- Allowing only `ssl` is much wider than allowing named SaaS apps on ssl; decryption improves identification.

## Verify
```
test security-policy-match from trust to untrust source 10.1.1.5 destination 198.51.100.7 destination-port 443 protocol 6 application ssl
```
Check the traffic log Application column for the final identified app.
