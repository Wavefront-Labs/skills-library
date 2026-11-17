---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.source-addr-and-universal-persistence
name: source-addr-and-universal-persistence
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, source-addr-persistence, universal-persistence, persist-uie]
level: practitioner
status: draft
description: "Use source-address, SSL session ID and iRule-based universal persistence on BIG-IP, with masks, timeouts and mirroring."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://clouddocs.f5.com/api/irules/persist.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Source address and universal persistence

```
tmsh create ltm persistence source-addr sa_app defaults-from source_addr timeout 1800 mask 255.255.255.255 match-across-pools disabled mirror enabled
tmsh create ltm persistence universal uni_sess defaults-from universal rule irule_sess timeout 3600
tmsh modify ltm virtual vs_web persist replace-all-with { uni_sess { default yes } } fallback-persistence sa_app
tmsh show ltm persistence persist-records
```
```
when HTTP_REQUEST {
  if { [HTTP::cookie exists JSESSIONID] } { persist uie [HTTP::cookie JSESSIONID] 3600 }
}
when HTTP_RESPONSE {
  if { [HTTP::cookie exists JSESSIONID] } { persist add uie [HTTP::cookie JSESSIONID] 3600 }
}
```
- Source address: hashes the client IP (after `mask`). Many clients behind one NAT concentrate onto one member; use a smaller mask only to group by subnet.
- `match-across-services` / `match-across-virtuals` / `match-across-pools` let one record apply to several VSs or pools sharing the same address; be cautious, they can send a client to a pool where the member does not exist.
- `mirror enabled` copies records to the peer, which costs CPU and needs network failover (confirm).
- Universal needs an iRule. SSL persistence uses the SSL session ID, which fails when clients resume with tickets.
- Gotcha: persistence records for a down member are retained until timeout; with `override-connection-limit disabled`, persistent clients still honour connection limits.

Verify: `tmsh show ltm persistence persist-records mode universal` should show the session key mapped to a member.
