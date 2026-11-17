---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.apm-access-policy-and-vpe
name: apm-access-policy-and-vpe
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, apm, access-policy, visual-policy-editor]
level: practitioner
status: draft
description: "Build an APM per-session access policy in VPE with logon page, AD auth and resource assignment, and attach it to a virtual."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-access-policy-manager-visual-policy-editor.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# APM access policies and the Visual Policy Editor

```
tmsh list apm profile access
tmsh list apm policy access-policy
tmsh list apm aaa active-directory
tmsh modify ltm virtual vs_apm profiles add { prof_apm { context clientside } rba http }
tmsh show apm access-info
tmsh show apm access-policy
```
- An APM deployment needs: a client SSL profile, an HTTP profile, an APM access profile, and (for the per-request policy) a SWG-style profile if used. The access profile contains the per-session policy built in the VPE (GUI: Access > Profiles/Policies > Access Profiles > Edit).
- Typical flow: Start -> Logon Page -> AD Auth (AAA server) -> Resource Assign (webtop/portal/network access) -> Allow. Branch rules use session variables such as `session.logon.last.username` and `session.ad.last.attr.memberOf`.
- AAA servers (AD, LDAP, RADIUS, SAML, OAuth) are defined under Access > Authentication; AD auth needs reachable domain controllers via the BIG-IP data path with correct DNS and NTP (Kerberos tolerates 5 minutes of skew).
- Apply Access Policy after each edit; sessions in progress continue on the old policy.
- Gotcha: the APM session cookie `MRHSession` is only issued on the first request; load balancing cookies and `Domain=` mismatch cause login loops.

Verify: log in through the VS, then `tmsh show apm access-info` lists the session and `Access > Overview > Active Sessions` shows variables; failed auth logs to `/var/log/apm`.
