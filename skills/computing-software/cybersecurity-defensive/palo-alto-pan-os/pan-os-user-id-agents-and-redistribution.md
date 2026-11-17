---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-user-id-agents-and-redistribution
name: pan-os-user-id-agents-and-redistribution
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [user-id-agent, pan-os, windows-agent, agentless-user-id, redistribution, syslog-listener, xml-api-user-mapping]
level: practitioner
status: draft
description: "Choose agent or agentless User-ID, parse login syslogs, push mappings via XML API, and redistribute them from a hub firewall."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/user-id/map-ip-addresses-to-users"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: get IP-to-user mappings from the right source with minimal domain controller load.

Sources
- Agentless: the firewall reads Security event logs (IDs 4768, 4769, 4624 and similar, confirm set) from domain controllers using a service account with Event Log Reader and DCOM/WMI rights.
- Windows User-ID agent: runs on a member server, same event reading, then pushes to firewalls.
- Syslog listener: parse RADIUS/NAC/Wi-Fi login syslogs with a regex filter profile.
- XML API: push one mapping from a script or captive IdP.

XML API example:
```
curl --cacert ca.pem -H "X-PAN-KEY: $KEY" "https://fw.example.com/api/?type=user-id" \
  --data-urlencode 'cmd=<uid-message><version>2.0</version><type>update</type><payload><login><entry name="example\alice" ip="10.1.1.5" timeout="60"/></login></payload></uid-message>'
```

Redistribution: a hub firewall or Panorama aggregates mappings and redistributes them to other firewalls (Device > User Identification > User-ID Agents > Redistribution), so branch devices do not poll DCs. Configure the agent name, collector name and pre-shared key on both sides (confirm per release).

Gotchas
- Service account lockouts or missing log read rights are the top cause of an empty mapping table.
- Probing (WMI client probing) is a legacy setting that is off by default in newer content; leave it off unless required.
- Do not enable User-ID on untrusted zones; spoofed mappings become policy bypass.

## Verify
```
show user user-id-agent state all
show user server-monitor state all
show user ip-user-mapping all
```
Server monitor state should read Connected for each DC.
