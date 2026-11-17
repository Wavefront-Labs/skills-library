---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.waf-policy-creation-and-learning
name: waf-policy-creation-and-learning
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, advanced-waf, asm-policy, learning-mode]
level: practitioner
status: draft
description: "Create a BIG-IP ASM/Advanced WAF policy, set blocking versus transparent, and accept learning suggestions."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-asm-implementations.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Advanced WAF policy creation and learning modes

```
tmsh create asm policy /Common/pol_web policy-template POLICY_TEMPLATE_RAPID_DEPLOYMENT enforcement-mode transparent
tmsh create ltm policy pol_waf strategy first-match requires add { http } controls add { asm } rules add { default { actions add { 0 { asm enable policy pol_web } } } }
tmsh modify ltm virtual vs_web policies add { pol_waf }
tmsh list asm policy pol_web enforcement-mode
```
- Attach the policy to a virtual server through a local traffic policy (as above) or in the GUI under Security > Application Security.
- Start in `transparent`: violations are logged, not blocked. Switch to `blocking` once false positives are accepted. Built-in templates include Rapid Deployment, Comprehensive and Fundamental.
- Learning mode per violation: `learn`, `alarm`, `block` flags (the Learn/Alarm/Block column in Security > Policy Building > Learning and Blocking Settings). Only violations with Learn enabled generate suggestions.
- Policy Builder (automatic) can accept suggestions after sufficient distinct sources send them; keep it off for apps with internal-only users since few sources means few trusted IPs.
- Changes only take effect after `Apply Policy`, which does not drop connections.
- Gotcha: a policy applied to a VS with an `HTTP` profile missing never inspects traffic; the ASM engine needs the HTTP profile. For HTTPS, the VS must terminate TLS.

Verify: send `curl 'http://vip/?q=<script>alert(1)</script>'`, then check Security > Event Logs > Application > Requests for the violation; `tmsh show asm policy-stats` for counts (confirm).
