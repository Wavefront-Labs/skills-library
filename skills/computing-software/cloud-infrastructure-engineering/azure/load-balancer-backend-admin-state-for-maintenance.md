---
id: computing-software.cloud-infrastructure-engineering.azure.load-balancer-backend-admin-state-for-maintenance
name: load-balancer-backend-admin-state-for-maintenance
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, load-balancer, admin-state, drain, maintenance, backend-pool]
level: practitioner
status: docs-checked
description: "Take a backend out of (or force it into) Azure Load Balancer rotation with admin state Down/Up, regardless of health probes, for patching and incident response."
sources: ["https://learn.microsoft.com/azure/load-balancer/admin-state-overview", "https://learn.microsoft.com/azure/load-balancer/manage-admin-state-how-to", "https://learn.microsoft.com/cli/azure/network/lb/address-pool/address"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backend admin state

**Goal:** drain a VM for patching without editing app health endpoints or removing it from the pool.

## States
| Admin state | Effect |
|---|---|
| None (default) | Health probe decides |
| **Down** | LB stops sending **new** connections to the backend even if probes pass |
| **Up** | LB sends new connections even if probes fail (use carefully, e.g. probe bug during incident) |
Admin state overrides probe status for new flows; check the docs for how existing flows are handled for your
rule type before relying on it for zero-downtime draining.

## Set it
IP-based backend pool:
```bash
az network lb address-pool address update -g rg --lb-name lb-app --pool-name be-web -n web01 --admin-state Down
# patch, reboot, validate...
az network lb address-pool address update -g rg --lb-name lb-app --pool-name be-web -n web01 --admin-state None
```
NIC-based pools: admin state cannot be set while creating the pool; set it afterwards (portal or the Load Balancer admin state how-to).

## Typical runbook
1. Set Down on one instance; watch connection metrics fall (byte/packet count to that backend).
2. Patch/reboot; validate locally (curl the app).
3. Set back to None; confirm probe status 100% for it.
4. Next instance.

## Gotchas
- Leaving an instance in **Up** hides real failures from the LB - always return to None.
- Admin state applies per backend per pool; the same VM in another pool/LB needs its own setting.
- Admin state is not supported with inbound NAT rules.

## Verify
- [ ] With Down set, new requests never reach the instance (app logs); after None, it receives traffic again.

## Checked

2026-10-28. Confirmed on the Load Balancer admin state overview and how-to: Up, Down and None values, Down blocks new connections regardless of probe, Up always treats the instance as eligible, admin state not supported with inbound NAT rules, cannot be set during creation of a NIC-based pool, az network lb address-pool address update with --admin-state (command check). Removed: the Standard-SKU-only claim and the ARM property path (not confirmed).

Method: documentation only; no commands were run.
