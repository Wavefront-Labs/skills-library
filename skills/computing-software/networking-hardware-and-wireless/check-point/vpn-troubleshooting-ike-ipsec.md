---
id: computing-software.networking-hardware-and-wireless.check-point.vpn-troubleshooting-ike-ipsec
name: vpn-troubleshooting-ike-ipsec
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, vpn-debug, ikeview, vpn-tu]
level: practitioner
status: draft
description: "Troubleshoot Check Point site-to-site VPN with vpn debug, ike.elg, IKEView, vpn tu and common failure messages."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SitetoSiteVPN_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VPN troubleshooting: IKE debug and tunnel utility

```
vpn debug trunc                     # start fresh $FWDIR/log/vpnd.elg and ike.elg
vpn debug ikeon
# reproduce the failure
vpn debug ikeoff ; vpn debug off
ls -l $FWDIR/log/ike.elg $FWDIR/log/vpnd.elg
vpn tu                              # 1) list IKE SAs  2) list IPSec SAs  6) delete SAs of peer
vpn tu del 203.0.113.9              # (confirm syntax)
fw ctl zdebug + drop | grep 203.0.113.9
```
- Open `ike.elg` in the **IKEView** tool (Windows) to read Phase 1/2 exchanges; errors: "No proposal chosen" (encryption/DH mismatch), "Invalid ID" or "Invalid Selectors" (encryption domain mismatch), "Authentication failed" (PSK mismatch, certificate/time), "Peer doesn't respond" (UDP 500/4500 blocked or NAT-T).
- Phase 1 works but no traffic: check routing (a tunnel needs the destination to route toward the gateway), the VPN column in the rule, and **Link Selection** (which IP the gateway uses as source).
- Always disable debug afterwards; leaving it on fills disks.
- Compare policy at both ends. For interoperable devices, ask the other side to share their proposal or log.
- Gotcha: cluster members use the cluster VIP for IKE; both members need the VIP in "Link Selection" or peers talk to a member IP and fail on failover.

Verify: `vpn tu` shows the IKE SA and two IPSec SAs (inbound/outbound) with a growing packet count; `cpstat vpn -f ...` (confirm); a ping across the tunnel passes while the log shows `Encrypt`.
