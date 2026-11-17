---
id: computing-software.cloud-infrastructure-engineering.azure.network-watcher-diagnostics-and-flow-logs
name: network-watcher-diagnostics-and-flow-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, network-watcher, network-troubleshooting, connection-troubleshoot, ip-flow-verify, nsg-diagnostics, next-hop, effective-routes, effective-security-rules, packet-capture, connection-monitor, vnet-flow-logs, nsg-flow-logs, traffic-analytics, topology, asymmetric-routing, kql, azurenetworkanalytics, ntfa, ip-flow, nsg-diag, next-hop-check, effective-route-table, connection-troubleshoot-use, connectivity-check, packet-capture-use, pcap]
level: practitioner
status: docs-checked
description: "Diagnose Azure connectivity: effective routes and NSG rules, IP flow verify, next hop, connection troubleshoot, packet capture, VNet flow logs, Traffic Analytics."
sources: ["https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview", "https://learn.microsoft.com/en-us/azure/network-watcher/connection-troubleshoot-overview", "https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview", "https://learn.microsoft.com/en-us/azure/network-watcher/nsg-flow-logs-overview", "https://learn.microsoft.com/en-us/azure/network-watcher/traffic-analytics", "https://learn.microsoft.com/en-us/azure/network-watcher/traffic-analytics-schema", "https://learn.microsoft.com/en-us/azure/network-watcher/packet-capture-overview", "https://learn.microsoft.com/en-us/azure/network-watcher/connection-monitor-overview", "https://learn.microsoft.com/en-us/cli/azure/network/watcher", "https://learn.microsoft.com/en-us/cli/azure/network/watcher/packet-capture"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Network Watcher — answer "why can't A reach B" in five commands

**Goal:** a repeatable triage path from a connectivity complaint to the exact NSG rule,
route or missing service that blocks it, plus flow logs that answer the question after the fact.

## 1. The five-command triage (run from your laptop, no agent needed except step 5)
```bash
NIC=$(az vm show -g rg -n vm-app -d --query "networkProfile.networkInterfaces[0].id" -o tsv)
# 1. what routes apply?   (look for the destination prefix; next hop VirtualAppliance/VirtualNetworkGateway/None = black hole)
az network nic show-effective-route-table --ids $NIC -o table
# 2. what NSG rules apply (subnet + NIC merged, with service tags expanded)?
az network nic list-effective-nsg --ids $NIC -o table
# 3. would this packet be allowed?  (direction, protocol, local/remote IP:port)
az network watcher test-ip-flow --vm vm-app -g rg --direction Outbound --protocol TCP --local 10.1.2.4:50000 --remote 10.2.0.4:1433
# 4. where does Azure send it?
az network watcher show-next-hop --vm vm-app -g rg --source-ip 10.1.2.4 --dest-ip 10.2.0.4
# 5. end-to-end (preview command; needs the Network Watcher agent extension on the source VM unless you use the agentless preview experience)
az network watcher test-connectivity --source-resource vm-app -g rg --dest-address 10.2.0.4 --dest-port 1433 --protocol TCP
```
- Step 3 names the **rule** that allows/denies (`DenyAllOutBound`, custom). Step 4 answers
  `VirtualAppliance` (firewall/NVA — check *its* logs next), `VirtualNetworkGateway`,
  `VnetLocal`, `Internet`, or **`None`** (a UDR black hole or missing peering).
- Step 5 returns per-hop status, latency, and the blocking resource (NSG/UDR/user firewall);
  destinations can be an IP, FQDN, or another VM.
- **NSG diagnostics** (`az network watcher run-configuration-diagnostic --resource <vm-id> --direction Inbound --protocol TCP --source 203.0.113.5 --destination 10.1.2.4 --port 443`) evaluates **all** NSGs in path with the matched rule per NSG — better than ip-flow when multiple NSGs/ASGs are involved.
- Check the guest too: `ss -tlnp`/`netstat -ano`, host firewall, and whether the service is bound to `0.0.0.0`.

## 2. Flow logs and Traffic Analytics
```bash
az network watcher flow-log create -g rg -n fl-vnet-prod -l uksouth --vnet vnet-prod --storage-account <st-id> --retention 30 \
  --traffic-analytics true --workspace <law-id> --interval 10 --format JSON --log-version 2
```
- **VNet flow logs** (replace NSG flow logs, which retire on 2027-09-30 and no longer support creating new ones): each record has the network interface, 5-tuple, direction, flow state, encryption state and throughput; they avoid enabling logging at both subnet and NIC level.
- Traffic Analytics processing interval is 60 minutes by default, or 10 minutes; tables `NTANetAnalytics` (flows) and `NTAIpDetails` replace the `AzureNetworkAnalytics_CL` tables used with NSG flow logs.
```kusto
NTANetAnalytics | where TimeGenerated > ago(1h) and FlowStatus == "Denied"
| summarize denied=sum(FlowCount) by SrcIp, DestIp, DestPort, AclRule, FlowDirection | order by denied desc
```
- Use it for: proving which rule denies a flow at 03:00, finding chatty east-west, building an allow-list before tightening NSGs.
- Cost: Traffic Analytics ingests into Log Analytics — set `--interval 60` on quiet VNets, 10 on security-sensitive ones; exclude dev VNets.

## 3. Packet capture
```bash
az network watcher packet-capture create -g rg --vm vm-app -n pc-sql --storage-account <st> --time-limit 300 --capture-size 128 --capture-limit 1073741824 \
  --filters '[{"protocol":"TCP","remoteIPAddress":"10.2.0.4","remotePort":"1433"}]'
az network watcher packet-capture show-status -l uksouth -n pc-sql ; az network watcher packet-capture stop -l uksouth -n pc-sql
```
The capture is written to the storage account (or a file path on the VM) — open in Wireshark. Needs the
Network Watcher agent extension (`AzureNetworkWatcherExtension`); `--target-type AzureVMSS` captures on scale sets.
Capture at **both ends** when you suspect asymmetric routing: SYN seen at destination, SYN-ACK leaves but never arrives = return path via a different NVA/route.

## 4. Connection Monitor (continuous)
Source (VM/Arc/VMSS with agent, or Log Analytics agent on-prem) → test group → destinations
(VM, FQDN, IP, URL) with protocol-specific tests at a frequency you choose (30 seconds to 30 minutes in the portal); thresholds on checks-failed % and RTT;
results in Log Analytics and metrics `ChecksFailedPercent`,
`RoundTripTimeMs`; topology hop view shows where loss starts. Standard uses: VPN/ER
on-prem ↔ Azure latency, app tier → database, outbound to a SaaS URL, cross-region.
Alert when `ChecksFailedPercent > 5` for 5 min — it finds a half-broken ER link long before users do.

## 5. Other tools
- **Topology** (`az network watcher show-topology -g rg`) — generated diagram of VNet/subnet/NIC/NSG relationships.
- **VPN troubleshoot** for gateway/connection state dumps; **Effective security rules** blade in the portal for a human-readable merge.
- Network Watcher is automatically enabled in a virtual network's region when you create or update a virtual network.

## Gotchas
- `test-ip-flow` evaluates NSGs only — it ignores Azure Firewall/NVAs and UDR black holes; pair with next-hop.
- `None` next hop with a route to a peered VNet usually means the peering is `Disconnected` or address spaces changed after peering (re-sync peering).
- Flow log states `B`/`C`/`E` (begin/continue/end): `B` carries no statistics and `C`/`E` counts are aggregates since the previous tuple, so don't sum all states blindly.
- Packet capture without a filter on a busy VM fills the session limit quickly; always filter.
- Service tag expansion in effective NSG output is long; prefer `-o json` with a query over table output.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Network Watcher overview, connection troubleshoot, VNet and NSG flow logs, Traffic Analytics and schema, packet capture, Connection Monitor, next hop, `az network watcher` and `packet-capture` references): next-hop types, agent extension name, NSG flow log retirement 2027-09-30, flow states, Traffic Analytics 60/10 minute interval and table names, Connection Monitor 30 s frequency option and metrics, auto-enablement. Corrected: `run-configuration-diagnostic --port`, packet-capture `--capture-size`/`--capture-limit`, `show-status -l -n`, test-connectivity is preview. Removed: June 2025 date, topology table, storage path and tuple format, Arc and alert-trigger claims, NSG rule counter logs, deallocated-VM claim.
Method: documentation only; no commands were run.

## Verify
- [ ] For a reported failure, the five-command triage identifies a single blocking element (rule/route/firewall/guest) reproducibly.
- [ ] `NTANetAnalytics` has rows for the production VNet within the last interval; a deliberate blocked flow appears with the NSG rule name.
- [ ] Connection Monitor test to the DB from the app tier shows `ChecksFailedPercent` 0 and RTT within budget; alert fires when the DB NSG is temporarily closed.
- [ ] Packet capture file opens in Wireshark with the expected 3-way handshake (or shows exactly where it stops).
