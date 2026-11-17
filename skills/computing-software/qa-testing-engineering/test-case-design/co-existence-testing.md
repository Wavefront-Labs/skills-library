---
id: computing-software.qa-testing-engineering.test-case-design.co-existence-testing
name: co-existence-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [co-existence-testing, compatibility-testing, iso-25010, shared-environment, resource-contention]
level: practitioner
status: gated
description: "Test co-existence: the system shares hosts, ports, libraries, databases or devices with other software without harming it or being harmed by it."
sources:
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Co-existence testing

**Goal:** ISO 25010 compatibility / co-existence: the product performs its functions while sharing an environment and resources with other products, without detrimental impact on any of them (gated: unconfirmed, source is paywalled or blocked).

## Identify the neighbours
Inventory what runs alongside it in production: other apps on the same VM or node, shared DB servers, message brokers, shared libraries/DLLs, browser extensions, antivirus/EDR agents, VPN clients, other apps on the same phone.

## Test ideas
- **Resource contention:** run the neighbour's typical load at the same time (CPU, memory, disk IO, connections). Measure both products' response times vs running alone.
- **Ports and names:** default port already taken, named pipes, mutex names, temp file names, scheduled task names colliding.
- **Shared dependencies:** a different version of a shared runtime or DLL installed by the neighbour (Java on PATH, Python site-packages). Installing or uninstalling ours must leave theirs working.
- **Shared database:** our migrations do not lock or alter shared schemas; connection pool limits leave room for others.
- **Security agents:** EDR/antivirus scanning slowing file IO or quarantining our binaries; corporate proxy TLS interception.
- **Mobile:** another app holding the camera or audio focus; battery savers killing background jobs.
- **Browser:** ad blockers and password managers altering the DOM.

## Method
Baseline alone, then together, then install/uninstall order permutations. Record resource metrics for both sides.

## Verify
Both products meet their SLOs when co-located at expected load, and install/uninstall in either order leaves the other functional.

## Checked

2026-10-28. Confirmed: Nothing; the ISO 25000 page could not be fetched. Gated: the ISO 25010 co-existence definition. Removed: Erroring ISTQB source link.

Method: documentation only; no commands were run.
