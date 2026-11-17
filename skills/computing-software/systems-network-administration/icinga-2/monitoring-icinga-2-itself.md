---
id: computing-software.systems-network-administration.icinga-2.monitoring-icinga-2-itself
name: monitoring-icinga-2-itself
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, self-monitoring, icinga-checkcommand, ido-check, health-checks, certificate-monitoring]
level: practitioner
status: docs-checked
description: "What to monitor around an Icinga 2 install: system, database and web checks, the icinga and ido CheckCommands, cluster health, TLS expiry."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# monitoring Icinga 2 itself
Icinga runs like any server application, so predictable problems such as low disk space hurt monitoring. Also verify that features and backends keep storing data: the database behind Icinga Web 2, metrics to Graphite or InfluxDB, and the distributed setup.

The docs table suggests, by type:
- System: `disk`, `mem`, `swap`, `procs`, `iostat`, `users`, `ntp_time`, `apt`, `yum`, `nwc_health`, hardware and VMware checks.
- Icinga: the `icinga` CheckCommand for status and runtime stats (forward to a graphing solution), plus cluster health checks.
- Database: `mysql_health`, `postgres`, housekeeping of size and growth, and the `ido` check.
- Web server: `http` for availability, certificates and authorization.
- Notifications: `smtp`, `mailq`, SMS modem checks.
- Metrics: `graphite`, InfluxDB, `elasticsearch`, Graylog.

Example IDO check:
```
apply Service "ido-mysql" {
  check_command = "ido"
  vars.ido_type = "IdoMysqlConnection"
  vars.ido_name = "ido-mysql"
  assign where match("master*.localdomain", host.name)
}
```
`ido_name` is the name defined in `/etc/icinga2/features-enabled/ido-mysql.conf`.

For more metrics, query the REST API and write a custom plugin, or use the built-in object accessor functions to compute stats in memory. Distributed setups should include the specific health checks, and TLS certificate expiry can be covered by the Icinga certificate monitoring module.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Icinga 2 Advanced Topics chapter: the Monitoring Icinga 2 section (rationale, the check table, the icinga CheckCommand, the ido example and closing notes) was read in full; other sections were not. Confirmed: the system, Icinga, database, web server, notification and metrics check suggestions listed in the skill, the ido apply rule with ido_type and ido_name, REST API or object accessor functions for more metrics, health checks for distributed setups, and certificate expiry via the certificate monitoring module.
