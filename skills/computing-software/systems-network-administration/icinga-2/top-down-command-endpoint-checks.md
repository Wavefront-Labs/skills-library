---
id: computing-software.systems-network-administration.icinga-2.top-down-command-endpoint-checks
name: top-down-command-endpoint-checks
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, command-endpoint, agent-endpoint, remote-checks, maxconcurrentchecks, log-duration, accept-commands]
level: practitioner
status: docs-checked
description: "Run Icinga 2 checks remotely with command_endpoint: objects on the master, CheckCommands on the agent, agent_endpoint var, MaxConcurrentChecks."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# top down command endpoint checks
In this mode the scheduler stays on the parent while a command execution event is sent to the endpoint. Host and service objects live on the master/satellite; the agent needs only CheckCommand definitions, best delivered through a global config zone.

Advantages: no local checks on the agent, light-weight asynchronous execution, no replay log needed, checks can be pinned to a specific endpoint. Disadvantages: if the agent is disconnected no checks run, it needs an extra attribute on host/service objects and local CheckCommand definitions. Every endpoint has its own remote check queue; limit it with the `MaxConcurrentChecks` constant, and note requests may be discarded when the queue is full.

Both nodes need Zone and Endpoint objects in `zones.conf` (each agent its own zone, parent `master`; use the agent FQDN for all names). The agent must accept commands in its api feature, and should disable `conf.d`. Set `log_duration = 0` on the agent Endpoint to disable the replay log.

Host and service pattern (the host name equals the endpoint name; versions before 2.11 used `client_endpoint`):
```
object Host "icinga2-agent1.localdomain" {
  check_command = "hostalive"
  address = "192.168.56.111"
  vars.agent_endpoint = name
}
apply Service "disk" {
  check_command = "disk"
  command_endpoint = host.vars.agent_endpoint
  assign where host.vars.agent_endpoint
}
```
Flow: the master validates, restarts and schedules; the agent receives the execute event with parameters, maps them to its local check command, runs it and sends back the result. No reload is needed on the agent.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/. No commands were run.
