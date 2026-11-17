---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-wildfire-analysis-profiles
name: pan-os-wildfire-analysis-profiles
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [wildfire, pan-os, wildfire-analysis, sandbox, file-forwarding, wildfire-cloud, verdicts]
level: practitioner
status: draft
description: "Forward unknown files to WildFire with a PAN-OS analysis profile, choose cloud region, and verify verdicts and the update cycle."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/threat-prevention/wildfire-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: unknown executables, documents and links get detonated and verdicts feed back as signatures.

```
configure
set deviceconfig setting wildfire cloud-server wildfire.paloaltonetworks.com
set profiles wildfire-analysis WF-ALL rules fwd-all application any file-type any direction both analysis public-cloud
set profile-group PG-STANDARD wildfire-analysis WF-ALL
commit
```
Choose public-cloud or private-cloud (WF-500 appliance) per rule. Set the size limits for forwarding in Device > Setup > WildFire.

Verdicts: benign, grayware, malware, phishing. Signature update interval can be as short as every minute with the WildFire dynamic update (needs the Threat Prevention + WildFire licences, confirm).

Gotchas
- Without decryption, HTTPS file downloads are invisible to forwarding.
- Email links need the `email-link` file type and an SMTP-aware path (confirm).
- Cloud reachability: the management plane (or its service route) must reach the cloud server on 443 and the control channel.

## Verify
```
test wildfire registration
show wildfire status
show wildfire statistics
```
Registration must be successful; statistics show forwarded and verdict counts. In the Monitor > WildFire Submissions log verify new entries.
