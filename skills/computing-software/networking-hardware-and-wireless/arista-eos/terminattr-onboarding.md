---
id: computing-software.networking-hardware-and-wireless.arista-eos.terminattr-onboarding
name: terminattr-onboarding
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, terminattr, cloudvision-agent, cv-onboarding, ingestgrpcurl]
level: practitioner
status: draft
description: "Onboard EOS to CloudVision with the TerminAttr daemon, ingest address, token and management VRF."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudVision onboarding with TerminAttr
Goal: stream device state to CloudVision.

```
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=192.0.2.90:9910 -cvauth=token,/tmp/token -cvvrf=MGMT -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -taillogs
   no shutdown
```

```
show daemon TerminAttr
show agent TerminAttr logs
```

- Enrolment token is created in CloudVision and copied to `/tmp/token` (do not store it in configs or source control).
- `-cvvrf` selects the VRF with a route to CloudVision; use CVaaS address and `-cvauth` as given by your tenant (confirm).
- The exact flags change by TerminAttr version; use the CloudVision documentation matching your release.

Gotcha: the switch needs correct time, DNS and route in the right VRF; otherwise the daemon logs TLS or connection failures. Tokens expire.

Operational tip: onboard in the management VRF with a token that has a short validity, and verify that streaming survives a reload. Keep TerminAttr and EOS versions within the documented compatibility matrix.

## Verify
- `show daemon TerminAttr` shows `Running` and the device appears in the CloudVision Inventory as Streaming.
