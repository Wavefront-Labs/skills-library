---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.afm-network-firewall-and-dos
name: afm-network-firewall-and-dos
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, afm, firewall-policy, dos-protection]
level: practitioner
status: draft
description: "Configure AFM network firewall rules at global, route-domain and virtual contexts, stage them, and enable DoS vectors."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-network-firewall-policies-and-implementations.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AFM firewall policies, contexts and DoS protection

```
tmsh create security firewall rule-list rl_web rules add { allow_https { action accept ip-protocol tcp destination { ports add { 443 } } source { addresses add { 10.0.0.0/8 } } place-after first } }
tmsh create security firewall policy pol_vs rules add { rl_web { rule-list rl_web } deny_all { action drop ip-protocol any } }
tmsh modify ltm virtual vs_web fw-enforced-policy pol_vs fw-staged-policy none
tmsh modify security firewall global-rules enforced-policy pol_global
tmsh show security firewall rule-list rl_web
tmsh modify security dos device-config dos-device { dos-device-vector add { tcp-syn-flood { auto-blacklisting disabled } } }
```
- Contexts are evaluated in order: Global -> Route Domain -> Virtual Server/Self IP -> Management port. The first context to drop wins; an `accept` in one context continues to the next, unless `accept-decisively` is used.
- A firewall policy added to a VS flips the VS to "default deny" for the destination (AFM is ADC-fastpath default-deny at VS level when a policy is attached); the last implicit rule is a drop, so end intentionally.
- Staged policies log hits without enforcing, which lets you test a new rule list on a production VS first.
- DoS: device-level vectors (e.g. TCP SYN flood, UDP flood, ICMP flood) with thresholds in packets per second; per-profile DoS (`security dos profile`) for application layer. Start with detection `mode` on `learning` or logging before `enforce`.
- Gotcha: rule order matters and the `place-after`/`place-before` option is required for ordering within a list; the GUI hides the drop-all rule `Default Action`.

Verify: `tmsh show security firewall rule-list rl_web` counters increment, and `tmsh show security firewall policy pol_vs` hits; logging profile output at `/var/log/ltm` shows `Network Firewall` records.
