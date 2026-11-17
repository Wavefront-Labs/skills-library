---
id: computing-software.cloud-infrastructure-engineering.azure.load-balancer-standard-rules-probes-and-outbound
name: load-balancer-standard-rules-probes-and-outbound
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, load-balancer, azure-load-balancer, standard-load-balancer, health-probes, outbound-rules, snat, snat-port-exhaustion, ha-ports, floating-ip, direct-server-return, internal-load-balancer, public-load-balancer, backend-pool, session-persistence, tcp-reset, idle-timeout, gateway-load-balancer, nva-ha, basic-lb-retirement]
level: practitioner
status: docs-checked
description: "Configure Standard Load Balancer: public vs internal, probes, HA ports and floating IP for NVAs/SQL AG, outbound rules and SNAT port math, Gateway LB."
sources: ["https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview", "https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-custom-probe-overview", "https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-outbound-connections", "https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-ha-ports-overview", "https://learn.microsoft.com/en-us/azure/load-balancer/gateway-overview", "https://learn.microsoft.com/en-us/cli/azure/network/lb/rule", "https://learn.microsoft.com/en-us/cli/azure/network/lb/probe", "https://learn.microsoft.com/en-us/cli/azure/network/lb/outbound-rule"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Standard Load Balancer: L4 balancing, probes and outbound SNAT done deliberately

**Goal:** a layer-4 front for VMs/VMSS/NVAs that fails over on a probe reflecting application health and does not run out of SNAT ports.

## 1. Build
```bash
az network public-ip create -g rg -n pip-lb --sku Standard --zone 1 2 3 --allocation-method Static
az network lb create -g rg -n lb-web --sku Standard --public-ip-address pip-lb --frontend-ip-name fe --backend-pool-name be
az network lb probe create -g rg --lb-name lb-web -n p-http --protocol Http --port 8080 --path /healthz --interval 15
az network lb rule create -g rg --lb-name lb-web -n r-https --protocol Tcp --frontend-port 443 --backend-port 443 \
  --frontend-ip-name fe --backend-pool-name be --probe-name p-http --idle-timeout 15 --enable-tcp-reset true --load-distribution Default
```
Add instances with `az network nic ip-config address-pool add` (or `az network lb address-pool address add` for IP-based pools).
- **Standard** SKU only: Basic Load Balancer was retired on 30 September 2025. The SKUs now are Standard and Gateway.
  Standard load balancers and public IPs are closed to inbound connections by default, so NSGs must explicitly allow the traffic.
- The load balancer operates at layer 4 (TCP/UDP). A public LB gives inbound and outbound; an internal LB balances inside a VNet (also from on-premises).
- `--load-distribution` accepts `Default`, `SourceIP`, `SourceIPProtocol`.
- `--idle-timeout` on a load-balancing rule: the CLI reference says 4 to 30 minutes, default 4, TCP only. `--enable-tcp-reset`
  gives a bidirectional TCP reset on idle timeout or unexpected termination.

## 2. Probes
- Protocols on Standard: TCP, HTTP, HTTPS. HTTP/HTTPS probes use GET on a path and are up only on HTTP 200 (a 403/404/500, no response
  within the timeout, or a TCP reset fails them); the HTTP/S timeout is 30 seconds. TCP probes only prove a listener answers.
- Interval: portal default 5 s; ARM/REST/CLI/PowerShell default 15 s (minimum 5). The `--probe-threshold` option is described in the
  CLI reference as preview, not recommended for production, default 1. For HTTP probes explicit 200/non-200 answers override the threshold.
- Probe source is `168.63.129.16` (IPv6: link-local `fe80::1234:5678:9abc`); the `AzureLoadBalancer` service tag covers it. Allow it in
  NSGs and guest firewalls; blocking it is unsupported. Do not use a VNet range containing 168.63.129.16.
- Down behaviour (Standard): one instance down means new TCP connections go to the remaining healthy ones and established ones
  continue; all down means no new flows but established TCP flows continue (more than one backend instance); UDP flows to an all-down pool terminate.
- Probe a port that reflects instance and application health (ports need not match, same is generally recommended). Do not proxy a probe to
  other VMs behind an appliance; probe the appliance itself. With multiple NICs, answer on the interface that received the probe.
- Limits: HTTPS probes do not support client-certificate mutual auth; HTTP probes do not support hostnames and cannot use ports 19, 21, 25, 70, 110, 119, 143, 220, 993.
- Inbound NAT rules do not need a probe. Stopped instances are not probed.

## 3. HA ports and floating IP (NVAs, SQL AG)
- **HA ports rule** (`--protocol All --frontend-port 0 --backend-port 0`) on an **internal** Standard LB balances every TCP/UDP flow per
  five-tuple: the pattern for active/active NVAs (spokes force-tunnel through the NVAs behind the internal LB). Add NVA instances to
  the backend pool; one health probe response must reflect the whole instance. Confirm supported scenarios with the NVA vendor.
- Restrictions: a non-HA-ports rule and an HA-ports rule on the same backend ipconfig on one frontend only if both have floating IP; multiple HA-ports
  rules need distinct private frontend IPs, each floating IP enabled; IP fragmenting is unsupported; TCP idle timeout is not supported for ILB HA ports when a UDR forwards to the ILB.
- Flow symmetry is supported for a single internal LB with one backend pool of NVAs (one IP configuration per NIC), not across two LBs, pools or frontends: use Gateway Load Balancer there.
- **Floating IP** (`--floating-ip true`): the CLI reference describes it as required for SQL Always On availability groups and not changeable after creation.

## 4. Outbound: SNAT ports
Order of preference: **NAT Gateway** on the subnet (best, takes precedence over LB, instance public IPs and Azure Firewall) > public IP on the VM (OK) >
LB frontend **with outbound rules** (production-capable but not at scale) > LB frontend without outbound rules (worst) > default outbound access (worst, insecure,
IPs can change). On 31 March 2026 new virtual networks default to private subnets, so choose an explicit method.
```bash
az network lb outbound-rule create -g rg --lb-name lb-web -n ob --frontend-ip-configs fe --address-pool be --protocol All \
  --idle-timeout 4 --outbound-ports 8000 --enable-tcp-reset true
```
- Each frontend public IP gives 64,000 SNAT ports; each port in a load-balancing or inbound NAT rule consumes a block of eight of them.
- Manual allocation: ports per instance = frontend IPs x 64K / backend instances (preferred for VMs); for scale sets allocate by "maximum number of
  backend instances", otherwise scale-out can be blocked or new VMs get too few ports.
- Default allocation (no outbound rules; or `allocatedOutboundPorts` 0 / `disableOutboundSnat` false on the rule) per frontend IP: 1-50 VMs 1,024, 51-100 512,
  101-200 256, 201-400 128, 401-800 64, 801-1,000 32; capped at 1,024 per VM. The page says not to use it for production.
- Exhaustion: every connection to the same destination IP and port needs its own SNAT port; new outbound connections fail until a port frees up.
  Fixes from the page: connection reuse, Private Link to Azure PaaS (no SNAT), NAT Gateway, more ports via outbound rules. Idle ports release after 4 to 120 minutes (set via outbound rules).
- Outbound rules do not support secondary IPv4 configurations of a NIC; fragmented packets are dropped unless the VM has an instance-level public IP.

## 5. Specials
- **Inbound NAT rules**: see the load-balancer-inbound-nat-rules skill. Prefer Bastion for admin access.
- **Gateway Load Balancer**: SKU for third-party NVAs; its frontend is private; rules are HA-ports only (up to two backend pools, up to two tunnel interfaces per pool);
  traffic is VXLAN-encapsulated. A Standard public LB frontend or VM public IP configuration chains to it, and no UDRs are needed. Its frontend cannot be a UDR next hop,
  it does not work with the Global tier, and cross-tenant chaining is not supported in the portal. For outbound inspection chain it to the frontends used by outbound rules.

## Gotchas
- NSGs must allow the `AzureLoadBalancer` tag for probes and the client source for the data port.
- A probe on one port while the app serves another can report healthy while the app is broken: probe what you serve.
- A probe definition is only validated in the portal; CLI/PowerShell/templates will not warn about a missing one.

## Verify
- [ ] Each backend instance reports healthy for the probe, and an NSG that blocks the probe port makes it unhealthy (the page's way to simulate failure).
- [ ] Outbound connections from a backend VM show the intended public IP, and no connection failures at peak.

## Checked

2026-11-07. Re-read in full: Load Balancer overview, health probes, outbound connections (SNAT), HA ports overview, Gateway Load Balancer overview.
For the CLI reference pages of `az network lb rule`, `probe` and `outbound-rule` I searched the flags used (`--idle-timeout`, `--enable-tcp-reset`, `--load-distribution`, `--floating-ip`, `--disable-outbound-snat`, `--interval`, `--probe-threshold`, `--outbound-ports`, `--frontend-ip-configs`) and read their descriptions, not the whole pages. Every command was also run through the repo's command checker (all flags exist).
- Corrected: rule idle timeout was "4-100 minutes"; CLI reference says 4 to 30 (default 4). Probe interval/threshold example removed (threshold is preview, default 1). Default-outbound note no longer cites API versions.
- Removed (not on the pages): backend pool limit 5,000, NIC-based vs IP-based pool claims and zone-redundancy claims for frontends, session-affinity advice, "fail-open vs drop" remark, NAT Gateway "64,512 ports / 16 IPs", loopback requirement for floating IP, probe port per AG listener, SNAT metric names and alert thresholds, cross-region LB description, SKU/availability-set/NIC-pool gotchas, "deleting the public IP removes SNAT", the internal-LB-has-no-outbound claim, effective-route and traceroute Verify steps.
- Not read: the Azure limits page, SNAT metrics page and the Load Balancer components article.

Method: documentation only; no commands were run.
