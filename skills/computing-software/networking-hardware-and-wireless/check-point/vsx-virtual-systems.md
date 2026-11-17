---
id: computing-software.networking-hardware-and-wireless.check-point.vsx-virtual-systems
name: vsx-virtual-systems
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, vsx, virtual-systems, vsenv]
level: practitioner
status: draft
description: "Navigate Check Point VSX virtual systems with vsenv, vsx stat and per-VS troubleshooting commands."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ClusterXL_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VSX virtual systems: vsenv and vsx stat

```
vsx stat -v                           # list VS IDs, names, policy, SIC state
vsenv 3                                # switch the shell context to VS 3
vsenv 0                                # back to VS0 (the VSX gateway)
fw ctl zdebug + drop                   # run per-VS after vsenv
fw monitor -e "accept host(10.1.1.1);"  # per-VS capture
cphaprob stat                           # VS cluster state, per-VS
```
- VSX runs many virtual firewalls on one gateway. **VS0** is the VSX gateway itself (management of physical interfaces, routing to Virtual Switches); other **VS IDs** are virtual systems, each with its own interfaces, policy and routing, connected through **Virtual Switches/Routers**.
- Every kernel and routing command acts on the *current VS context*: after `vsenv N` the prompt changes `[Expert@gw:N]`. Forgetting this is the main trap; `fw ctl zdebug` in VS0 shows nothing for traffic of VS3.
- In SmartConsole, a VS is an object of type "Virtual System"; **VSX Cluster** members hold the same VSs, each VS in its own HA state (`cphaprob stat` per VS; `vsx stat`).
- Create VS through the **VSX wizard** or `vsx_util` and `mgmt_cli add vsx-gateway` (confirm); changes to interfaces need `vsx_util reconfigure` in some cases and policy install on VS0.
- Resource control: `fw ctl multik stat` per VS and VS limits per licence. Use "Resource Control" for CPU/memory per VS (confirm).
- Gotcha: after a reboot, `vsenv` returns to VS0; scripts must call `vsenv` first.

Verify: `vsx stat -v` shows each VS with `Policy installed` and `SIC trust`; `vsenv 3; fw stat` shows the VS-specific policy.
