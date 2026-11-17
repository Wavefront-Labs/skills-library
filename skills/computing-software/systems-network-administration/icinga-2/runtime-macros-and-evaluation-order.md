---
id: computing-software.systems-network-administration.icinga-2.runtime-macros-and-evaluation-order
name: runtime-macros-and-evaluation-order
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, runtime-macros, evaluation-order, host-state, service-output, notification-type, env]
level: practitioner
status: docs-checked
description: Use Icinga 2 runtime macros in commands - lookup order across user, service, host, command and IcingaApplication, available macros, env.* and dollar escaping.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runtime macros and evaluation order
Macros like `$address$` or `$ping_wrta$` read object attributes and custom variables when a command runs. A literal single dollar must be written `$$`.

**Lookup order** for a macro name:
1. User object (notifications only)
2. Service
3. Host
4. Command
5. IcingaApplication

So defaults can live in the command object and be overridden on the service, for example `vars.ping_packets = 10` on a Service overriding the command default. An undefined variable yields an empty value and a warning in the log. A full name such as `$service.vars.ping_wrta$` skips the lookup rules and returns empty if the service lacks it.

Available macros:
- Host: `host.name`, `host.display_name`, `host.state`, `host.state_id`, `host.state_type`, `host.check_attempt`, `host.last_state`, `host.output`, `host.perfdata`, `host.num_services_ok` and others.
- Service: `service.name`, `service.state`, `service.state_id`, `service.state_type`, `service.output`, `service.perfdata`, `service.latency` and others.
- Command: `command.name`. User: `user.name`, `user.display_name`.
- Notification: `notification.type`, `notification.author`, `notification.comment`.
- Global: `icinga.timet`, `icinga.long_date_time`, `icinga.short_date_time`, `icinga.date`, `icinga.time`, `icinga.uptime`, and counters such as `icinga.num_services_ok` or `icinga.num_hosts_down`.
- Environment variables of the Icinga process: `$env.<name>$`, e.g. `$env.ProgramFiles$`; the `env.` prefix is required.

Host and service object attributes are also accessible.

## Checked

2026-11-04. Confirmed against the Icinga 2 monitoring basics chapter: macro lookup order, $$ escape, available macros and the env. prefix for environment variables ($env.ProgramFiles$).

Method: documentation only; no commands were run.
