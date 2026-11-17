---
id: computing-software.networking-hardware-and-wireless.opnsense.firewall-diagnostics-aliases-states
name: firewall-diagnostics-aliases-states
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [firewall-diagnostics, pf-states, sessions, pftop]
level: practitioner
status: docs-checked
description: "Use Firewall > Diagnostics on OPNsense: alias contents and find references, sessions via pftop, state table search and kill, state names and statistics."
sources: ["https://docs.opnsense.org/manual/diagnostics_firewall.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Firewall diagnostics

Aliases: shows each loaded alias and its contents (and statistics if enabled for the alias). You can add entries with Quick add address or remove them with the delete button, but deletion is not persistent; the normal update process may put the entry back. "Find references" tests whether an address matches any alias, including network membership (10.0.0.2 fits 10.0.0.0/24), which is handy for debugging.

Sessions: uses pftop for active sessions with counters. Columns: Dir (in -> or out <-), Proto, Source, Gateway (the NAT-translated address and port), Destination, State, Age (sec), Expires (sec), Pkts, Bytes, Rule.

States: view, search and remove entries of the pf state table. You can reset all states and the source tracking table, but resetting states drops every active connection, so use it carefully. After a grid search, or via the Inspect button on the firewall rules page, a button kills all states matching the criteria. Rule association is by pf rule number, so it may be inaccurate after rules change. Columns add State id, Int (all unless Bind states to interface is set under Firewall > Settings > Advanced), Nat and a Command button to drop one state.

TCP states follow RFC 793: LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT, CLOSED. UDP and other protocols use NO_TRAFFIC, SINGLE (source sent more than one packet, destination never replied) and MULTIPLE (both sides sent).

Statistics presents pfctl data: per-interface packet counters, memory limits, timeouts and detailed active rules.

## Checked

2026-11-03. Read the Firewall Diagnostics manual page (diagnostics_firewall.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
