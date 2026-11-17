---
id: computing-software.cloud-infrastructure-engineering.azure.on-premises-vpn-device-configuration
name: on-premises-vpn-device-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vpn-gateway, vpn-device-config, device-configuration-script, ipsec, ike-policy, site-to-site]
level: advanced
status: docs-checked
description: "Configure on-premises VPN devices for Azure site-to-site tunnels: validated devices, device scripts, IPsec/IKE policy matching, policy-based selectors and BGP."
sources: ["https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpn-devices", "https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-download-vpndevicescript", "https://learn.microsoft.com/azure/vpn-gateway/ipsec-ike-policy-howto", "https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-connect-multiple-policybased-rm-ps", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-connection", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-connection/ipsec-policy"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# On-premises VPN device configuration for Azure S2S

**Goal:** bring up a stable IPsec tunnel between an on-premises VPN device and an Azure VPN gateway.

## Steps
1. Check the device in the validated VPN devices table (vendor, family, minimum firmware, and whether it is tested for PolicyBased and RouteBased). Recommended algorithms on that page: IKE AES256, SHA256, DH2; IPsec AES256GCM. Unlisted devices may still work; the vendor supports them.
2. Download a device script. Portal: gateway, Connections, the connection, Download configuration, then pick vendor, device family and firmware version. CLI (marked Preview in the reference, returns XML):
```bash
az network vpn-connection show-device-config-script -g rg -n cn1   --vendor "Cisco" --device-family "Cisco-ISR(IOS)" --firmware-version "Cisco-ISR-15.x-- IKEv2+BGP"
```
   PowerShell can list valid names with `Get-AzVirtualNetworkGatewaySupportedVpnDevice`. Search the script for `REPLACE` and check those values (interface numbers, ACL numbers, policy names) against your device. Some templates have a commented-out CLEANUP section.
3. Match IPsec/IKE parameters. Without a custom policy the gateway offers its default proposals (see the VPN devices page tables). To pin one, add a custom policy to the connection. All parameters must be set together:
```bash
az network vpn-connection ipsec-policy add -g rg --connection-name cn1   --ike-encryption GCMAES256 --ike-integrity SHA384 --dh-group DHGroup24   --ipsec-encryption GCMAES256 --ipsec-integrity GCMAES256 --pfs-group PFS24   --sa-lifetime 27000 --sa-max-size 102400000
```
   - Custom policy needs VpnGw1-5, VpnGw1AZ-5AZ, Standard or HighPerformance; one policy per connection; partial policies are not allowed.
   - If IPsec encryption is a GCMAES algorithm, IPsec integrity must be the same GCMAES algorithm and key length.
   - The device must match or include the IKE encryption, IKE integrity, DH group, IPsec encryption, IPsec integrity and PFS group (and traffic selectors if used). SA lifetimes are local and need not match. IKE Main Mode SA lifetime is fixed at 28,800 seconds.
   - Once a custom policy is set, the gateway sends and accepts only that proposal on that connection, so a mismatch stops the tunnel coming up.
   - Quick Mode SA lifetime: minimum 300 seconds (default 27,000) and 1,024 KB (default 102,400,000). DPD timeout: 9 to 3,600 seconds, default 45; the page generally recommends 30 to 45, because shorter values rekey more aggressively and the connection can appear to drop. DPD is set in the portal or PowerShell, not by this CLI command.
4. Policy-based devices: route-based gateway plus policy-based traffic selectors on the connection, which makes the gateway use prefix-pair selectors. Your device must define every combination of local network gateway prefix to Azure virtual network prefix (not any-to-any), and the on-premises networks can reach the VNet but cannot transit to each other through the gateway. The policy-based devices must support IKEv2. The multiple-devices article says you must create an IPsec/IKE policy to enable the option, while the IPsec/IKE policy article says the option can be used with the default policy; check which applies when you set it:
```bash
az network vpn-connection update -g rg -n cn1 --use-policy-based-traffic-selectors true
```
5. BGP: the gateway's default ASN is 65515. Do not use Azure-reserved ASNs for the on-premises side: public 8074, 8075, 12076; private 65515, 65517, 65518, 65519, 65520 (VPN Gateway FAQ).

## Notes
- IKE versions: policy-based Basic gateways IKEv1 only; route-based Basic IKEv2; route-based VpnGw1AZ-5AZ IKEv1 and IKEv2.
- Azure clamps TCP MSS bidirectionally on the gateway (1360 bytes IPv4 over the Internet, 1250 over an ExpressRoute gateway).
- ESP NULL encryption is possible on RouteBased gateways but gives no protection; use the default algorithms across the Internet.

## Verify
- [ ] The connection status in the portal shows Connected after you apply the device config.
- [ ] If it won't connect, compare the device proposals with the connection's custom policy parameters one by one.

## Checked

2026-11-07. Read in full: About VPN devices and IPsec/IKE parameters, Download VPN device configuration scripts, Configure custom IPsec/IKE policies (portal), Connect a VPN gateway to multiple on-premises policy-based VPN devices, and the `ipsec-policy add` and `show-device-config-script` sections of the CLI references (the full `vpn-connection` reference is large and was searched for these commands and `--use-policy-based-traffic-selectors`, not read end to end). Reserved ASNs come from the VPN Gateway FAQ page, read for that section only. Snippets in the other tabs of the policy page (PowerShell steps) were not run.
Corrected or removed: the claim that policy-based selectors require a custom policy (the two articles disagree, now stated); the UDP 500/4500 plus ESP bullet (it is a point-to-site fact, not on the S2S pages), ESP fragmentation, active-active two-tunnel advice, the IKEDiagnosticLog and `troubleshooting start` verify steps, the `bgpSettings.bgpPeeringAddress` property and the "IKEv2 preferred" advice; DPD is not a flag of the CLI `ipsec-policy add`.

Method: documentation only; no commands were run.
