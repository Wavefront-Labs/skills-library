---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-connectivity-troubleshooting-timeouts-mtu
name: vpc-connectivity-troubleshooting-timeouts-mtu
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, network-troubleshooting, connection-timeout, asymmetric-routing, mtu-troubleshooting, pmtud, security-groups, vpc]
level: practitioner
status: docs-checked
description: "Diagnose AWS connectivity failures systematically: timeout vs refused, SG/NACL/route checks, asymmetric routing through appliances, and MTU/PMTUD black holes over VPN and TGW."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/network_mtu.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting connectivity: timeouts, asymmetric routing, MTU

## 1. Read the symptom
| Symptom | Means | Look at |
|---|---|---|
| `Connection refused` (RST) quickly | packet reached the host, nothing listening / host firewall | service status, `ss -lntp`, iptables/Windows Firewall |
| **Timeout** | packet dropped somewhere | SG, NACL, route tables, NAT/IGW, appliance |
| Connects, small requests work, large ones hang | **MTU / PMTUD** | ICMP, MSS clamping |
| Works one direction / intermittently through firewall | **asymmetric routing** | route tables both ways, appliance mode |
| Name doesn't resolve | DNS | VPC DNS attributes, PHZ association, Resolver rules |

## 2. Timeout checklist (in order)
1. Run **Reachability Analyzer** source → destination/port — it names the blocking component.
2. Flow logs on the destination ENI: no record = never arrived (routing upstream); `REJECT` =
   SG/NACL; `ACCEPT` inbound but no outbound = host or return-route problem.
3. Return path: NACL outbound ephemeral ports; destination subnet route back to the source
   (especially over TGW/peering/VPN).
4. Internet: public subnet has `0.0.0.0/0 → igw` and instance has a public IP; private subnet → NAT.

## 3. Asymmetric routing
Typical: inbound via firewall/GWLB in AZ a, response leaves via a route that skips it or uses
AZ b's appliance → stateful device drops it. Fixes: enable TGW **appliance mode** on the
inspection attachment; per-AZ route tables pointing at the same-AZ endpoint; ingress routing
(gateway route table) for IGW traffic. Verify with flow logs on both appliance ENIs: you must
see both directions of the same 5-tuple on one appliance.

## 4. MTU
- Inside a VPC: up to 9001 (jumbo frames). 1500 over an internet gateway, over VPN connections and between
  Regions unless a transit gateway is used; 8500 over an inter-region VPC peering connection. A transit
  gateway supports 8500 between VPCs, Direct Connect, Connect and peering attachments, but VPN traffic is 1500.
- PMTUD needs ICMP "fragmentation needed" (type 3 code 4; ICMPv6 Packet Too Big, type 2) back to the
  sender; a NACL denying ICMP, or a SG rule set that drops it, creates black holes. Allow it from the path,
  clamp MSS on the VPN device, or lower the instance MTU to 1500.
```bash
tracepath 10.20.1.10                      # shows pmtu per hop
ping -M do -s 1472 10.20.1.10             # 1472+28 = 1500; reduce until it passes
```

## Gotchas
- SGs are stateful but NACLs are not; most "random" timeouts after a NACL edit are ephemeral ports.
- Instances with multiple ENIs in different subnets reply out of the wrong interface (OS
  routing) → asymmetric; use policy routing or a single ENI.
- Source/dest check must be disabled on any instance forwarding traffic.

## Verify
- [ ] The failing flow has a Reachability Analyzer result and flow-log evidence identifying the hop.
- [ ] After the fix, a large transfer completes across the VPN/TGW path.
- [ ] Appliance flow logs show symmetric flows.

## Checked
2026-10-31. Confirmed against the EC2 User Guide MTU page (1500 for internet gateway, VPN and cross-Region traffic; 8500 for inter-region VPC peering; 9001 jumbo; ICMP type 3 code 4 and ICMPv6 type 2; NACL can block ICMP) and the Transit Gateway quotas and appliance-mode pages (8500 MTU, 1500 over VPN, appliance mode keeps flows in one AZ). Corrected: inter-region peering is 8500, not 1500. Removed: the 1399-1436 VPN tunnel range, the `tcp adjust-mss 1379` value, the 100 KB test size (not in the docs).
Method: documentation only; no commands were run.
