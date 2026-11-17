---
id: computing-software.systems-network-administration.network-design.firewall-rule-testing-packet-tracer
name: firewall-rule-testing-packet-tracer
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, firewall-design, rule-testing, asa-packet-tracer, policy-simulation, change-validation]
level: practitioner
status: docs-checked
description: "Test firewall rules before and after changes with simulation tools: ASA packet-tracer, Palo Alto test security-policy-match, plus live connection tests."
sources:
  - https://www.cisco.com/c/en/us/td/docs/security/asa/asa-cli-reference/I-R/asa-command-ref-I-R/pa-pn-commands.html
  - https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-cli-quick-start/use-the-cli/test-the-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing firewall rules with packet-tracer and friends

## Cisco ASA
```
packet-tracer input inside tcp 10.1.1.10 51000 192.0.2.80 443 detailed
packet-tracer input outside tcp 198.51.100.7 51000 203.0.113.10 443 xml
```
Output is a numbered list of phases (the ASA command reference example shows CAPTURE and
ROUTE-LOOKUP phases) ending in a final result for the simulated packet.

## Palo Alto
```
test security-policy-match application ssl source 10.1.1.10 destination 192.0.2.80 destination-port 443
```
The PAN-OS CLI quick start shows this command with application, source, destination and
destination-port arguments.

## Other vendors
Use the vendor's own policy-simulation or flow-debug tool (for example FortiGate flow debug);
its commands are not reproduced here because they were not confirmed.

## Process
1. Before the change: simulate the intended flow (expect deny), and a sample of existing flows
   that must keep working.
2. Apply; re-run simulations (expect allow) and a real test (`curl`, `Test-NetConnection`, `nc -vz`).
3. Check hit counters on the new rule and logs.
4. Keep the test commands in the change ticket for repeatability.

Simulation does not test the return path, upstream ACLs, or application-layer inspection fully;
always finish with a live test.

## Verify
- [ ] Change ticket includes pre/post simulation output and a live test result for each requested flow.

## Checked

- Date: 2026-10-28
- Confirmed: ASA packet-tracer syntax with detailed and xml keywords and the Phase/ROUTE-LOOKUP output (ASA command reference); PAN-OS test security-policy-match (CLI quick start).
- Removed: FTD and FMC packet-tracer claims, asp-drop capture, test nat-policy-match and the pre-NAT/post-NAT remark, the whole FortiGate block (the cited Fortinet link redirects to an unrelated article), the Fortinet source.

Method: documentation only; no commands were run.
