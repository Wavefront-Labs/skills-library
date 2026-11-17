---
id: computing-software.cloud-infrastructure-engineering.azure.load-balancer-health-probe-design
name: load-balancer-health-probe-design
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, load-balancer, health-probes, probe-design, http-probe, probe-threshold, 168-63-129-16]
level: practitioner
status: docs-checked
description: "Design Azure Load Balancer health probes: TCP vs HTTP/HTTPS, deep vs shallow health endpoints, interval and threshold maths, NSG/firewall requirements and probe-down triage."
sources: ["https://learn.microsoft.com/azure/load-balancer/load-balancer-custom-probe-overview", "https://learn.microsoft.com/azure/load-balancer/load-balancer-troubleshoot-health-probe-status", "https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load Balancer health probe design

**Goal:** the LB removes a backend when it can't serve, and doesn't remove all backends at once
because a shared dependency hiccuped.

## Probe types
| Type | Healthy when | Use |
|---|---|---|
| TCP | Handshake completes | Non-HTTP services, NVAs |
| HTTP | 200 from path within timeout | Web/API — preferred |
| HTTPS | 200 over TLS (certificates need a SHA256 or stronger signature hash across the chain) | When only TLS port is open |
Probe source is **168.63.129.16** (`AzureLoadBalancer` service tag) — NSGs, guest firewalls and app
allow-lists must permit it.

## Timing
`intervalInSeconds` (minimum 5; the default is 5 s in the portal and 15 s from ARM, REST, CLI and PowerShell) and `probeThreshold` (consecutive results needed to change state).
For TCP probes detection time is about interval × threshold (5 s × 2 = 10 s). For HTTP/HTTPS probes an explicit 200 or non-200 response changes state at once and the threshold only applies when the probe times out (the HTTP/S timeout is 30 s, or the interval if shorter).
```bash
az network lb probe create -g rg --lb-name lb-web -n hp-http --protocol Http --port 8080 \
  --path /healthz --interval 5 --probe-threshold 2
```

## Health endpoint design
- **Shallow** (`/healthz`): process up, can accept requests, local resources OK. Use for LB probes.
- **Deep** (`/ready` checking DB, cache): risky for LB probes — a DB blip marks **every** backend down → LB has no healthy instance and stops sending new flows (established TCP flows continue) — a full outage caused by the probe. Keep dependency checks out of the LB probe and degrade gracefully in the app.
- Return non-200 during graceful shutdown to drain: a probe-down signal stops new connections, while established TCP flows on Standard LB continue until idle timeout or close.
- Keep it cheap (no auth, no heavy queries); the probe runs at the configured interval.

## NVA / HA ports
Probe the appliance's own health, not a port it proxies or translates to other VMs behind it (one healthy VM would then keep a failed appliance in rotation, and a blip can cascade). For active/standby, use a port that answers only on the active instance. With an HA ports rule one probe response must reflect the whole instance, and a multi-NIC VM must answer on the interface the probe arrived on.

## Probe-down triage
1. Metrics: *Health Probe Status* split by backend IP.
2. From the VM: `curl -i http://localhost:8080/healthz`; confirm the app is listening on the probe port.
3. NSG/OS firewall allows 168.63.129.16; Linux `iptables`, Windows Firewall.
4. HTTP probe redirects (301/302) count as unhealthy — probe a path that returns 200 directly.
5. Mismatched ports (probe 80, app 8080).

## Verify
- [ ] Health Probe Status = 100% for all backends in steady state.
- [ ] Stopping the app on one VM drops it from rotation within a few probe intervals; traffic continues on others.

## Checked

2026-10-31. Confirmed against the Learn Load Balancer custom probe overview (protocols, 200-only HTTP success, 30 s HTTP/S timeout, 5 s portal and 15 s CLI default intervals, minimum 5 s, threshold behaviour for TCP and HTTP, probe-down behaviour for established flows, 168.63.129.16 and the AzureLoadBalancer tag, HA ports and NVA probing guidance, SHA256 certificate note) and the health probe status troubleshooting page. Corrected: the threshold does not delay HTTP probes that get explicit responses. Removed: the default threshold of 1, the 127.0.0.1 remark and the "no cert validation" claim (not in the docs). Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
