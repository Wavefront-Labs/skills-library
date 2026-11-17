---
id: computing-software.cloud-infrastructure-engineering.aws.direct-connect-ordering-cross-connects-and-hosted-connections
name: direct-connect-ordering-cross-connects-and-hosted-connections
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, direct-connect, cross-connect, loa-cfa, hosted-connection, dx-partner, dx-provisioning]
level: advanced
status: docs-checked
description: "Provision Direct Connect end to end: dedicated vs hosted connections, location choice, LOA-CFA and the colo cross-connect, partner hosted VIFs, light levels and first BGP."
sources: ["https://docs.aws.amazon.com/directconnect/latest/UserGuide/dedicated_connection.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/hosted_connection.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/Colocation.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/Troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ordering Direct Connect: dedicated and hosted

## 1. Choose the model
| | Dedicated connection | Hosted connection |
|---|---|---|
| Speeds | 1, 10, 100, 400 Gbps ports | 50, 100, 200, 300, 400, 500 Mbps, 1, 2, 5, 10, 25 Gbps (1 Gbps and up only from partners that met extra requirements; 25 Gbps only where 100 Gbps ports exist) |
| Who owns the port | You (port in your AWS account) | A Direct Connect Partner, who allocates you capacity |
| You need | Presence (or a carrier circuit) in the DX location | A partner contract |
| MACsec | Optional, chosen at creation; read the MACsec prerequisites for dedicated connections first | Check the partner and the hosted-connection page |
Pick DX locations per your resiliency model (two locations for high resiliency, two
connections in each of two locations for maximum).

## 2. Dedicated connection steps
1. Request:
```bash
aws directconnect create-connection --location EqLD5 --bandwidth 10Gbps \
  --connection-name dc1-ld5-a --request-mac-sec   # optional
aws directconnect describe-locations   # codes and available port speeds
```
2. State goes `requested`, then `pending` while AWS allocates the port.
3. Download the **LOA-CFA** (Letter of Authorization and Connecting Facility Assignment):
   `aws directconnect describe-loa --connection-id dxcon-... --output text --query loaContent | base64 -d > loa.pdf`.
   It names the AWS cage, patch panel and port. If the cross-connect is not completed
   within 90 days the LOA-CFA authority expires; download it again from the console to renew it.
4. Give the LOA to the colocation provider (if you are in the facility) or your network
   carrier, who orders the **cross-connect** from your equipment (or their meet-me room
   demarc) to the AWS port. Match the optics to the port speed and check the
   connection requirements in the Direct Connect User Guide before ordering.
5. When the cross-connect is in, the connection goes `available` once AWS sees light.

## 3. Hosted connection steps
1. Order from a partner in the partner portal/contract, giving your AWS account ID.
2. Partner creates the hosted connection; it appears in your account as `ordering`.
3. Accept it: `aws directconnect confirm-connection --connection-id dxcon-...`
4. Create the VIF (private, public or transit). With "hosted VIFs" on a partner's
   dedicated connection instead, you accept the VIF with `confirm-private-virtual-interface`
   and attach it to your VGW or DX gateway.

## 4. Bring-up checks
- Physical: `describe-connections` state `available`; optical light levels via the
  **ConnectionLightLevelRx/Tx** CloudWatch metrics (unit dBm). No light: cross-connect not
  patched or Tx/Rx swapped.
- Layer 2: correct VLAN on the subinterface; ARP for the AWS peer IP resolves.
- BGP: neighbor addresses, ASN and MD5 key match the VIF;
  `describe-virtual-interfaces` shows `bgpStatus: up`.
- Test failover before production traffic (DX resiliency toolkit failover test).

## Gotchas
- Port-hour billing starts when the port is active or 90 days after the LOA is issued,
  whichever comes first. Delete unused requests before then. If the port is not up after
  90 days and no LOA-CFA was issued, AWS emails that the port will be deleted in 10 days.
- Cross-connect fees are billed by the colo, not AWS.

## Verify
- [ ] Connection `available`, light levels in range, no errors (`ConnectionErrorCount`).
- [ ] VIF `available` with BGP `up` and expected prefixes received.
- [ ] Failover test passes with traffic on the second path.

## Checked
2026-10-28. Confirmed against the dedicated_connection and hosted_connection pages: port speeds 1/10/100/400 Gbps, hosted speed list and 25 Gbps rule, 90-day LOA/billing rule and 10-day deletion notice, the ConnectionLightLevelRx/Tx metrics (unit dBm; monitoring-cloudwatch page), `--request-mac-sec` (the CLI flag, from the botocore model; the earlier `--request-macsec` does not exist). Removed as unconfirmed: 72-hour allocation, lead times, VIF counts and the one-VIF hosted rule, MACsec speed list, optic types and auto-negotiation, Rx light range, charges-on-acceptance, upgrade limits.
Method: documentation only; no commands were run.
