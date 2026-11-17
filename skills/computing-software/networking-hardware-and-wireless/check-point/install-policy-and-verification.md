---
id: computing-software.networking-hardware-and-wireless.check-point.install-policy-and-verification
name: install-policy-and-verification
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, install-policy, policy-verify, fw-fetch]
level: practitioner
status: draft
description: "Install policy from SmartConsole or mgmt_cli, interpret verification errors, and recover a gateway with fw fetch or unloadlocal."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Install policy, verification errors and fetch

```
mgmt_cli -r true install-policy policy-package "Standard" access true threat-prevention true targets.1 "gw1" --format json
mgmt_cli -r true show task task-id "<id>"
fw stat                         # on the gateway: shows installed policy name and time
fw fetch <mgmt-ip>              # gateway pulls policy from management
fw unloadlocal                  # remove policy, gateway opens (lab/emergency only)
cpstat fw -f policy
```
- SmartConsole runs a verification first: anti-spoofing conflicts, invalid objects, unsupported blade combinations, and "gateway not reachable" (SIC). Fix errors rather than choosing "Install anyway"; warnings may be ignored.
- Install on cluster members is staged: by default "For gateway clusters, if installation on a cluster member fails, do not install on that cluster" is ticked, protecting the cluster from partial installs.
- Policy install with `Install on all selected gateways, if it fails do not install on any`. Use the **Access Control** and **Threat Prevention** options together to avoid inconsistent states.
- Failure with "Load on module failed": check `$FWDIR/log/fwd.elg` on the gateway and `$FWDIR/log/cpm.elg`/`$FWDIR/log/install_policy_report.txt` on the management.
- `fw unloadlocal` leaves the gateway unprotected and forwarding with the ruleset removed; on a cluster use only with a plan, and install policy again at once.
- Gotcha: after a large change, installation can take minutes and gateways briefly drop only new connections; schedule it.

Verify: `fw stat` prints the new policy name and install time; `cpstat fw -f policy` shows the `Policy name`; check **Logs & Monitor > Tasks** for succeeded.
