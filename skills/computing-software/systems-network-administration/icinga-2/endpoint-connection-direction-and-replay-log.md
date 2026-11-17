---
id: computing-software.systems-network-administration.icinga-2.endpoint-connection-direction-and-replay-log
name: endpoint-connection-direction-and-replay-log
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, endpoint, host-attribute, log-duration, replay-log, connection-direction, firewall]
level: advanced
status: docs-checked
description: Control which Icinga 2 node opens the cluster connection via the Endpoint host attribute, disable the replay log for command endpoint agents, and open port 5665.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# endpoint connection direction and replay log
An endpoint attempts to connect to another when its local Endpoint object has a valid `host` attribute (FQDN or IP). Choose one direction:
```
// master connects to the agent
object Endpoint "icinga2-agent1.localdomain" {
  host = "192.168.56.111"
  log_duration = 0
}
// agent does not connect to the master: leave out host
object Endpoint "icinga2-master1.localdomain" {
  log_duration = 0
}
```
Icinga 2 only uses one connection and closes the second if both sides open one, wasting CPU and blocking resources until a timeout. Let either master/satellite connect to agents or vice versa.

**Replay log.** It keeps history (check results, notifications) identical when nodes disconnect and reconnect. It is not needed when a master or satellite sends check execution events to an agent used as command endpoint, so set `log_duration` lower or to `0` on the Endpoint objects, on both the master and the agent side, to disable log replay while the agent is offline.

**Windows firewall** from the docs: ICMP echo requests are disabled by default; add a rule to allow them. If masters or satellites actively connect to a Windows agent, open TCP port 5665. If `check_nscp_api` queries NSClient++, open its port 8443, preferably only for local connection from the Icinga agent; remote connections to the legacy HTTP API are not recommended.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: Endpoint host direction, single connection, log_duration and replay log, Windows firewall notes.

Method: documentation only; no commands were run.
