---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortiguard-licensing-and-update-services
name: fortiguard-licensing-and-update-services
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortiguard-update, fortios, forticare, fortiguard-services, license-status, update-server, av-ips-signatures]
level: practitioner
status: draft
description: "Check FortiGuard license entitlements and update services, fix update failures and select update servers on FortiOS."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: security profiles that are actually licensed and current.

```
get system fortiguard-service status
diagnose autoupdate versions
execute update-now
diagnose debug rating
config system fortiguard
    set update-server-location usa
    set protocol https
    set port 443
end
```
Entitlements (FortiCare registration): AV, IPS, web filtering, application control, FortiGuard industrial and DNS filtering, FortiConverter, etc. A device that is registered and licensed shows each service with an expiry date. Registration of hardware uses the FortiCare account; FortiGate VM uses licence files or FortiFlex tokens.

Gotchas
- Update fails when the unit cannot resolve or reach `*.fortinet.net`; fix DNS and the default route first, and check the source interface (`set interface-select-method specify`).
- Clock drift leads to certificate and licence errors.
- FortiManager can act as local FortiGuard server for sites with restricted internet (`config system central-management` with update options).
- Web filter rating issues: `diagnose debug rating` shows which rating server is used and whether it is reachable.

## Verify
```
diagnose autoupdate status
get system fortiguard-service status
```
Services show valid and recent signature dates; test with a manual `execute update-now` and check the event log for a success entry.
