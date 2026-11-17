---
id: computing-software.systems-network-administration.cisco-networking.cef-tcam-and-sdm-templates
name: cef-tcam-and-sdm-templates
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, catalyst-9300, cef, fib, sdm-template, show-sdm-prefer, exact-route, hardware-forwarding, table-capacity]
level: advanced
status: docs-checked
description: "CEF FIB and adjacency terms, show ip cef and exact-route, and Catalyst 9300 SDM templates (access, nat): how to read and change them, and why a reload is required."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipswitch_cef/configuration/xe-16/isw-cef-xe-16-book/isw-cef-load-balancing.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/configuring_sdm_templates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CEF and SDM templates

## CEF terms (from the Cisco load-balancing module glossary)
- FIB: the forwarding information base, conceptually similar to a routing table; the router uses the FIB lookup table for destination-based switching decisions and keeps a mirror image of the forwarding information in the IP routing table.
- Distributed CEF: line cards keep identical copies of the FIB and adjacency tables and do the express forwarding between port adapters.
- CEF is enabled by default on most Cisco platforms running IOS 12.0 or later. `show ip cef` prints `%CEF not running` when it is off; `ip cef` enables central CEF and `ip cef distributed` enables distributed CEF.
- Load balancing is per-destination by default (packets of one source-destination pair take the same path). Per-packet load balancing can reorder packets and the page does not recommend it. The algorithm is chosen with `ip cef load-sharing algorithm` (original, universal (default), tunnel, include-ports).
- `show ip cef exact-route <source> <destination>` shows the path selected for a flow; the page documents optional `src-port`/`dest-port` and `gtp-teid` keywords.

## SDM templates on Catalyst 9300 (IOS XE 17.9)
SDM templates configure system resources to optimise support for specific features. The 9300 supports the `access` and `nat` templates.
```
configure terminal
 sdm prefer access          ! or: sdm prefer nat
 end
reload
show sdm prefer
```
- The change takes effect after `reload`. Before the reload, `show sdm prefer` shows both the template in use and the one that becomes active after the reload. `show sdm prefer access` and `show sdm prefer nat` print each template's limits.
- The chapter's sample output lists, per template, entries such as Security Access Control Entries, QoS Access Control Entries, Policy Based Routing ACEs, Netflow ACEs, directly connected routes, indirect routes, tunnels and MAC addresses. The numbers differ between the access and nat templates and between models (for example C9300-24UB/24UXB/48UB differ from other models), so read them from `show sdm prefer` on your own switch rather than from this skill.
- The sample output states that its numbers are typical for L2 and IPv4 features and that features such as IPv6 use double the entry size, so only half as many entries can be created.
- Templates contain only commands defined as part of the template; a related command a template enables indirectly may show in `show running-config`, and is removed with the template and then needs configuring explicitly.

## Not covered by the cited pages
FED platform commands (`show platform hardware fed ...`), TCAM utilisation output, punt-cause counters, syslog message names for TCAM exhaustion, the `distribution` and `core` templates (not listed for the 9300 in this chapter), `show adjacency` and `glean`/`punt` adjacency meanings. Take these from the platform's own troubleshooting guide before relying on them.

## Verify
- [ ] `show sdm prefer` after the reload shows the template you set.
- [ ] `show ip cef exact-route <src> <dst>` shows the path you expect for a test flow.

## Checked
Date: 2026-11-08. Read in full: Configuring SDM Templates (Catalyst 9300, 17.9.x, about 16k characters) and the sections of "Configuring a Load-Balancing Scheme" on platform support, load-balancing types and algorithms, GTP exact-route and the glossary (the 31k-character module was read through the first half and the glossary, not the later configuration tasks).
Confirmed: access and nat templates, `sdm prefer access | nat`, reload requirement and `show sdm prefer` behaviour before and after, template note on implied commands, IPv6 double-entry note, FIB and dCEF definitions, default-on CEF, `%CEF not running`, per-destination default, per-packet caveats, algorithm names, `show ip cef exact-route` syntax.
Removed: the RIB/adjacency/TCAM model (ENCOR reference), `show ip cef <prefix> detail`, `show adjacency` and adjacency types, FED commands, error message names, `distribution`/`core` templates, the "80 percent" threshold, `no ip cef` production advice and the CPU/punt diagnostics (none on the cited pages). The first source was a book index page and was replaced by the load-balancing module that was read.
Method: documentation only; no commands were run.
