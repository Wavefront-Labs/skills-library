---
id: computing-software.systems-network-administration.network-design.network-runbooks-and-sops
name: network-runbooks-and-sops
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-documentation, runbook, sop, operations, incident-response, on-call, knowledge-base]
level: practitioner
status: draft
description: "Write network runbooks and SOPs that on-call engineers can follow at 3 a.m.: structure, decision points, exact commands with expected output, escalation, and keeping them tested."
sources:
  - https://sre.google/workbook/on-call/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network runbooks and SOPs

- SOP (standard operating procedure): a routine task done the same way every time (add a VLAN,
  onboard a branch, rotate SNMP credentials).
- Runbook: what to do when an alert fires or a known failure happens (WAN circuit down, BGP session
  down, DHCP pool exhausted).

## Structure that works
```
Title: BGP session to ISP-A down (alert BGP_PEER_DOWN, edge-rtr-01)
Impact: internet traffic fails over to ISP-B; no user impact expected unless ISP-B also degraded.
Urgency: P2 during business hours, P3 out of hours if ISP-B healthy.
Prerequisites: SSH via jump host, ISP-A NOC number and circuit ID (CID 123/ABC).
Steps:
 1. Confirm: `show ip bgp summary | include 203.0.113.1`  expect: Idle/Active = down.
 2. Check link: `show interfaces Gi0/0/0 | include line protocol|errors`.
    - Link down -> step 5 (circuit fault).
    - Link up -> step 3.
 3. Check reachability: `ping 203.0.113.1 source Gi0/0/0`.
 4. Check logs for BGP notification: `show logging | include BGP` (hold timer, MD5, max-prefix).
 5. Raise a fault with ISP-A: phone, CID, timestamps, our tests.
Verify recovery: session Established, prefixes received ~ 950k, traffic back on ISP-A (or per policy).
Escalation: network on-call lead after 30 min; ISP-A account manager after 4 h.
Last tested: 2026-09-12 by J. Smith (game day).
```

## Writing rules
- Exact commands and the expected output for healthy and broken states; no "check the router".
- Decision points as explicit branches.
- Safe by default: read-only diagnostics first; risky actions marked and require approval.
- Links to diagrams, circuit IDs, vendor contacts and the monitoring dashboard.
- One runbook per alert type; link it from the alert itself so on-call lands on it directly.

## Keep them alive
- Review after every incident where the runbook was used (was it right? fast enough?).
- Test quarterly in game days or maintenance windows.
- Store in version control or a wiki with owners and review dates; stale runbooks are worse than
  none.
- Automate repeated steps into scripts and keep the runbook as the wrapper.

## Verify
- [ ] Every paging alert has a linked runbook tested within the last six months.
