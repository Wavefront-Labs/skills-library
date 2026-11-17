---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.irules-events-and-structure
name: irules-events-and-structure
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, irules, irule-events, event-priority]
level: practitioner
status: draft
description: "Write BIG-IP iRules with the right events (CLIENT_ACCEPTED, HTTP_REQUEST, LB_SELECTED), priorities and a profile prerequisite check."
sources:
  - https://clouddocs.f5.com/api/irules/HTTP__header.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iRules events, priorities and structure

```
when CLIENT_ACCEPTED priority 100 {
  set start [clock clicks -milliseconds]
}
when HTTP_REQUEST {
  if { [HTTP::uri] starts_with "/admin" } { reject }
}
when LB_SELECTED {
  log local0. "member [LB::server addr] for [IP::client_addr]"
}
```
```
tmsh create ltm rule irule_demo from-file /var/tmp/irule_demo.tcl
tmsh modify ltm virtual vs_web rules { irule_demo }
```
- Events fire in lifecycle order: `CLIENT_ACCEPTED`, `CLIENTSSL_HANDSHAKE`, `HTTP_REQUEST`, `LB_SELECTED`, `SERVER_CONNECTED`, `HTTP_RESPONSE`, `CLIENT_CLOSED`. An event needs its profile: no HTTP profile means `HTTP_REQUEST` never fires.
- With several rules on one VS, rules run in listed order per event; `priority N` (default 500, lowest first) reorders handlers across rules.
- Variables set with `set` are local to the event; share between events using `static::` (global, read-only after RULE_INIT) or per-connection variables of the same name (TCL variables persist across events of the same connection).
- Use curly braces around every `if`/`expr` condition (`if { ... }`) so Tcl does not double-substitute: braces are also a security and performance rule.
- Gotcha: `log` calls at line rate drown syslog and cost CPU; guard with a `static::debug` flag. Syntax errors block the save; `tmsh load sys config` rejects the rule at load.

Verify: `tmsh show ltm rule irule_demo` for executions, failures and aborts, and tail `/var/log/ltm` for the log line. `tmsh modify ltm rule irule_demo ... ` with `profile-stats` is not needed; Check `Failures` stays 0.
