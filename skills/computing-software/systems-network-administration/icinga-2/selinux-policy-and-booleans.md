---
id: computing-software.systems-network-administration.icinga-2.selinux-policy-and-booleans
name: selinux-policy-and-booleans
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, selinux, icinga2-selinux, icinga2-t, setsebool, plugin-domains, permissive]
level: advanced
status: docs-checked
description: Run Icinga 2 under SELinux - install icinga2-selinux, confirm the icinga2_t domain, label plugins into nagios plugin domains, and use booleans like icinga2_can_connect_all.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/22-selinux/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELinux policy and booleans
The policy targets Red Hat Enterprise Linux 7 and derivatives running the targeted policy.

**Install:** `yum install icinga2-selinux`, restart the service, and confirm the daemon runs in its own domain with `ps -eZ | grep icinga2` (expect `icinga2_t`). Manual install from the repository uses `tools/selinux/icinga.sh` and needs `git`, `selinux-policy-devel` and `audit`.

**Troubleshooting:** `sestatus` shows the mode. Instead of disabling SELinux, put only Icinga's domain in permissive mode with `semanage permissive -a icinga2_t`, then report policy bugs. Any plugin domain can be made permissive the same way.

**Labels:** log files `icinga2_log_t`; the command pipe `icinga2_command_t`; the API port `icinga2_port_t`. Plugins run in their own domains, for example `nagios_services_plugin_exec_t` (network services), `nagios_system_plugin_exec_t`, `nagios_checkdisk_plugin_exec_t`, `nagios_mail_plugin_exec_t`, `nagios_admin_plugin_exec_t`, `nagios_unconfined_plugin_exec_t`. A manually installed plugin is unconfined by default; relabel with `chcon -t nagios_services_plugin_exec_t /path/to/plugin`.

**Booleans:**
- `icinga2_can_connect_all`: connect to all ports, for example Graphite on a non-default port or InfluxDB.
- `icinga2_run_sudo`: allow plugins via sudo (off by default; otherwise `execvpe(sudo) failed: Permission denied`).
- `httpd_can_write_icinga2_command` and `httpd_can_connect_icinga2_api`: on by default; disable if unused.

Set with `setsebool -P icinga2_can_connect_all true`.

## Checked

2026-11-04. Confirmed against the Icinga 2 SELinux chapter: RHEL 7 target, icinga2-selinux install, icinga2_t, labels, plugin domain table, semanage permissive, chcon, booleans and setsebool -P. Corrected the sudo error text to execvpe.

Method: documentation only; no commands were run.
