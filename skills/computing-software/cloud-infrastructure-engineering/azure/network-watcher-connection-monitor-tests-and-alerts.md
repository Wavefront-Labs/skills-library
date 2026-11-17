---
id: computing-software.cloud-infrastructure-engineering.azure.network-watcher-connection-monitor-tests-and-alerts
name: network-watcher-connection-monitor-tests-and-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, network-watcher, connection-monitor, connection-monitor-setup, connection-monitor-tests, test-groups, synthetic-monitoring, checks-failed-percent, round-trip-time, network-latency, hybrid-monitoring]
level: practitioner
status: docs-checked
description: "Set up Network Watcher Connection Monitor: sources, destinations, TCP/HTTP/ICMP test configs, thresholds, Log Analytics results and alerts on ChecksFailedPercent and RTT."
sources: ["https://learn.microsoft.com/en-us/azure/network-watcher/connection-monitor-overview", "https://learn.microsoft.com/en-us/azure/network-watcher/connection-monitor-create-using-portal", "https://learn.microsoft.com/en-us/cli/azure/network/watcher/connection-monitor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection Monitor — continuous synthetic network tests with alerts

**Goal:** always-on probes for the paths that matter (app → DB, Azure ↔ on-prem, Azure → SaaS),
so latency and loss are measured and alerted rather than discovered from user tickets.

## 1. Prerequisites
- Azure VM/VMSS sources need the **Network Watcher agent** extension
  (`AzureNetworkWatcherExtension`, Linux or Windows). On-prem/other-cloud sources use
  **Azure Arc** (Arc-enabled hosts are the only supported on-premises source) + Azure Monitor Agent; the Log Analytics agent is no longer supported for on-premises monitoring.
- Network Watcher enabled in the source region; a Log Analytics workspace for results.
- NSGs/firewalls must allow the probe traffic (TCP port of choice, ICMP if used).

## 2. Create
```bash
az network watcher connection-monitor create -n cm-app-to-sql -l uksouth \
  --endpoint-source-name vm-app1 --endpoint-source-resource-id <vm-app1-id> \
  --endpoint-dest-name sql-prod --endpoint-dest-address sql-prod.privatelink.database.windows.net \
  --test-config-name tcp1433 --protocol Tcp --tcp-port 1433 --frequency 30 \
  --threshold-failed-percent 5 --threshold-round-trip-time 20 \
  --workspace-ids <law-id> --test-group-name app-to-db
az network watcher connection-monitor endpoint add ...       # more sources/destinations into the same test group
az network watcher connection-monitor test-configuration add --protocol Http --http-method Get --http-path /health --http-valid-status-codes 200 ...
```
Structure: **monitor** (one region) → **test groups** (sources × destinations × test
configurations) → every combination is a test. Keep groups per path type so alerts are meaningful.

Test configurations:
- **TCP**: port (`--tcp-port`, `--tcp-port-behavior`).
- **HTTP/HTTPS**: method (`Get`/`Post`), path, valid status codes.
- **ICMP**: latency/loss only; many appliances deprioritise ICMP, so prefer TCP for SLAs.
- Frequency: the portal offers 30 seconds, 1, 5, 15 or 30 minutes, or custom; thresholds: checks failed % and RTT ms. A test is *Warning* above 80 % of a threshold and fails when it is exceeded; with no threshold set, the service assigns one (750 ms RTT for TCP/ICMP).

## 3. Results and alerts
- Metrics on the monitor: `ChecksFailedPercent`, `RoundTripTimeMs`, `TestResult`
  (dimensions: SourceName, DestinationName, TestGroupName, TestConfigurationName).
- Check results are also stored in the Log Analytics workspace you attached; confirm the table and column names in the workspace before writing queries.
```bash
az monitor metrics alert create -g rg-net -n cm-app-to-sql-fail --scopes <connection-monitor-id> \
  --condition "avg ChecksFailedPercent > 5 where TestGroupName includes app-to-db" --window-size 5m --evaluation-frequency 1m --action <ag-id>
```
- Topology view (portal → Connection Monitor → test → *Topology*) shows the hop where loss
  or latency appears — gateway, firewall, or the on-prem edge.

## Gotchas
- *Indeterminate* means no data reached the Log Analytics workspace (for example a deallocated VM or missing agent), not failed; endpoint status is re-evaluated once every 24 hours.
- Probes from a VM behind a firewall test the firewall path; probe from the same subnet as the app or results mislead.
- Private Link destinations: use the private FQDN and confirm the source resolves it privately.
- Results ingest into Log Analytics, so prune unused source/destination combinations.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Connection Monitor overview, create using the portal) and the `az network watcher connection-monitor` reference: Arc plus Azure Monitor Agent for on-premises sources, Log Analytics agent unsupported, frequency choices, Warning/Indeterminate semantics, metrics `ChecksFailedPercent`/`RoundTripTimeMs`/`TestResult`, create and test-configuration flags. Removed: disableTraceRoute, per-table names, 1-day maximum frequency, per-test billing and monitoringStatus claims.
Method: documentation only; no commands were run.

## Verify
- [ ] `az network watcher connection-monitor show -l uksouth -n cm-app-to-sql` shows the monitor running.
- [ ] The workspace receives results at the configured frequency for each test.
- [ ] Temporarily denying port 1433 on the DB NSG turns the test red and fires the alert within 5 minutes.
