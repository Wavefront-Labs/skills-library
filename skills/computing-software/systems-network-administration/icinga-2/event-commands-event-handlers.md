---
id: computing-software.systems-network-administration.icinga-2.event-commands-event-handlers
name: event-commands-event-handlers
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, eventcommand, event-command, event-handler, soft-state, restart, curl]
level: practitioner
status: docs-checked
description: Attach an Icinga 2 EventCommand to a host or service to react to state changes, when it fires, where it runs, and a curl example.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# event commands (event handlers)
Unlike notifications, an event command is called on every check execution when:
- the host/service is in a soft state,
- it changes into a hard state, or
- it recovers from a soft or hard state to OK/Up.

EventCommand objects are referenced with the `event_command` attribute on Host and Service. The command line should evaluate runtime macros such as `$service.state_type$` and `$service.state$`. If the object is monitored through a command endpoint, the event command runs on the client itself, like the check command.

Use cases from the docs: restart a service after a failing HTTP check, restart an unresponsive application, or forward more detail on state changes than notifications carry.

Example sending data from the master:
```
object EventCommand "send_to_businesstool" {
  command = [ "/usr/bin/curl", "-s", "-X PUT" ]
  arguments = {
    "-H" = {
      value = "$businesstool_url$"
      skip_key = true
    }
    "-d" = "$businesstool_message$"
  }
  vars.businesstool_url = "http://localhost:8080/businesstool"
  vars.businesstool_message = "$host.name$ $service.name$ $service.state$ $service.state_type$ $service.check_attempt$"
}
object Service "businessprocess" {
  host_name = "businessprocess"
  check_command = "icingacli-businessprocess"
  event_command = "send_to_businesstool"
}
```
Test by catching the request with `nc -l 8080`, or enable the debug log and run `tail -f /var/log/icinga2/debug.log | grep EventCommand`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Event Commands section of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page) through the send-from-master example. Confirmed the three conditions, the event_command attribute, runtime macros, execution on the command endpoint, the use cases, and the curl example with its test commands. Nothing was removed. No commands were run.
