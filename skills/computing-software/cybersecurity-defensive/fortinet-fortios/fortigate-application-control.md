---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-application-control
name: fortigate-application-control
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [application-control, fortios, application-list, app-category, shaper-per-app, p2p, block-apps]
level: practitioner
status: draft
description: "Control applications on FortiGate with application lists, categories, overrides and per-application shaping."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: allow business applications and block or limit risky categories.

```
config application list
    edit "app-std"
        config entries
            edit 1
                set category 2 6
                set action block
            next
            edit 2
                set application 40568
                set action pass
            next
        end
        set other-application-log enable
        set unknown-application-log enable
    next
end
config firewall policy
    edit 10
        set application-list "app-std"
    next
end
```
Category numbers (for example P2P, Proxy) and application IDs are looked up with `set category ?` / `set application ?` or in the FortiGuard application database. Entries are matched in order; the default action for unmatched applications is pass.

Gotchas
- Application control needs SSL deep inspection to classify most HTTPS apps.
- Some apps are dynamic and move between categories after IPS/app database updates.
- An application entry with `action block` for a base application (e.g., HTTPS.BROWSER) can break many services; test with monitor first.
- Use `set shaper` and `per-ip-shaper` for traffic-shaping by app.

## Verify
```
diagnose ips signature info 40568
```
(Confirm applicable command.) The App-Control log lists applications seen with action; test using the vendor-documented test application from a lab client.
