---
id: computing-software.cloud-infrastructure-engineering.google-cloud.connectivity-tests-network-topology-analyzer-and-vm-network-debugging
name: connectivity-tests-network-topology-analyzer-and-vm-network-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-intelligence-center, connectivity-tests-run, reachability-analysis, network-topology, network-performance-dashboard, network-analyzer, network-troubleshooting-gce, firewall-debugging]
level: practitioner
status: docs-checked
description: "Debug connectivity on Google Cloud: Connectivity Tests, effective firewalls and routes, Network Topology, Performance Dashboard, Network Analyzer and in-VM checks."
sources: ["https://docs.cloud.google.com/network-intelligence-center/docs/connectivity-tests/how-to/running-connectivity-tests", "https://docs.cloud.google.com/network-intelligence-center/docs/performance-dashboard/concepts/overview", "https://docs.cloud.google.com/vpc/docs/using-firewalls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connectivity tests, topology, Network Analyzer and VM network debugging

## 1. Connectivity Test (config analysis, no packets sent)
```bash
gcloud network-management connectivity-tests create app-to-db \
  --source-instance=projects/<P>/zones/<Z>/instances/app-1 \
  --destination-ip-address=10.20.0.5 --destination-port=5432 --protocol=TCP
gcloud network-management connectivity-tests describe app-to-db \
  --format='yaml(reachabilityDetails.result,reachabilityDetails.traces[0].steps)'
gcloud network-management connectivity-tests rerun app-to-db      # after a fix
```
Result `REACHABLE` / `UNREACHABLE` / `AMBIGUOUS` / `UNDETERMINED` (analysis did not complete, for example a permissions error),
with the traced steps. Keep tests for critical paths and rerun them after network changes.

## 2. Effective rules on a VM
```bash
gcloud compute instances network-interfaces get-effective-firewalls app-1 --zone=<Z>
gcloud compute routes list --filter='network:prod' --sort-by=priority
gcloud compute instances describe app-1 --zone=<Z> --format='yaml(networkInterfaces,tags,serviceAccounts)'
```
Check inherited firewall policies as well as VPC rules, and turn on Firewall Rules Logging on the suspect rule to see hits.

## 3. Inside the VM
```bash
ss -tlnp | grep 5432                 # is the service listening on the right interface?
sudo iptables -S; sudo nft list ruleset   # OS firewall
curl -v telnet://10.20.0.5:5432       # TCP reachability
sudo tcpdump -ni ens4 host 10.20.0.5 and port 5432
ip link show ens4                     # check the interface MTU against the VPC MTU
```

## 4. Wider view
- **Performance Dashboard**: packet loss and latency between zones where you have VMs (current data and the past six weeks;
  up to five regions selected), plus a Google Cloud-wide view to compare against your project.
- Network Topology and Network Analyzer are further Network Intelligence Center tools; read their docs before relying on them.

## Gotchas
- Connectivity Tests analyse configuration, not the guest OS or the application; REACHABLE + timeout points to the VM/app.
- Health-check probe ranges (`35.191.0.0/16`, `130.211.0.0/22`) must be allowed to reach load balancer backends.

## Verify
- [ ] The test for each critical path is REACHABLE and rerun after changes.

## Checked
2026-10-28. Confirmed: Network Management API v1 discovery document (`reachabilityDetails.result` values), Performance Dashboard overview
(packet loss and latency, six weeks, five regions), health-check ranges on the load-balancing health-check page. Commands verified against
the gcloud reference. Removed: Network Analyzer insight type and command, Topology description, MTU default, IAP range, hierarchical
policy order, supported-scenarios list, asymmetric-routing note.
Method: documentation only; no commands were run.
