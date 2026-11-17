---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-security-policy-rules
name: pan-os-security-policy-rules
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [security-policy-rules, pan-os, rulebase, application-default, log-end, rule-order, shadowed-rules, rule-hit-count]
level: practitioner
status: draft
description: "Write PAN-OS security rules using zones, App-ID and application-default, log at end, and audit shadowing and hit counts."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/policy/security-policy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: allow exactly the applications you want, log them, and prove each rule is used.

```
configure
set rulebase security rules allow-web from trust to untrust source any destination any application [ web-browsing ssl ] service application-default action allow log-end yes
set rulebase security rules allow-web profile-setting group PG-STANDARD
set rulebase security rules deny-log from any to any source any destination any application any service any action deny log-end yes
move rulebase security rules deny-log bottom
commit
```
Evaluation is top-down, first match wins. Rule types (universal, intrazone, interzone) constrain which zone pairs a rule covers.

Practices
- `service application-default` pins the app to its standard ports; `any` lets the app run on any port, widening the allow.
- Log at session end (`log-end`); `log-start` adds load and is for troubleshooting only.
- Attach a profile group so inspection is not skipped on allow rules.
- Use tags, descriptions and rule hit counts (GUI Policies > Rule Usage; confirm CLI availability) to retire unused rules.

Gotchas
- Some apps depend on others (ssl, web-browsing); a rule with only the final app may not match until the dependency is also allowed.
- A shadowed rule never triggers; check with Policy Optimizer or an ordering review.

## Verify
```
test security-policy-match from trust to untrust source 10.1.1.5 destination 198.51.100.7 destination-port 443 protocol 6
show running security-policy
```
The result names the first rule matched and its action.
