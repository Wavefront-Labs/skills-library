---
id: computing-software.systems-network-administration.zabbix.agent2-core-configuration
name: agent2-core-configuration
category: computing-software
field: systems-network-administration
product: zabbix
tags: [agent2, zabbix-agent2, serveractive, hostname, persistent-buffer]
level: practitioner
status: docs-checked
description: "Set the key Zabbix agent 2 parameters: Server, ServerActive, Hostname, buffer, control socket and Include rules."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_agent2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Agent 2 is configured in its zabbix_agent2.conf file. The parameters that matter first:

- Server: comma-separated IPs (CIDR allowed) or DNS names of servers and proxies allowed to connect for passive checks. If unset, passive checks are disabled and the agent listens on no TCP port.
- ServerActive: where to fetch active checks, as address[:port]. If unset, active checks are disabled. Use commas for independent servers and semicolons for cluster or proxy-group members, for example ServerActive=proxy1.example.com;proxy2.example.com.
- Hostname: required for active checks and must match the host name configured on the server (case-sensitive). If unset it comes from HostnameItem, default system.hostname. Allowed characters are alphanumerics, dot, space, underscore and dash, up to 128 characters.
- ListenPort: default 10050.
- RefreshActiveChecks: default 5 seconds, range 1-86400. After a failed refresh the retry is 60 seconds.
- BufferSize: default 1000 values (2-65535), used only when EnablePersistentBuffer=0. With EnablePersistentBuffer=1 set PersistentBufferFile (a full filename for the SQLite database) and PersistentBufferPeriod.
- ControlSocket: default /tmp/agent.sock, used for runtime commands with -R.
- LogType: file, system or console. LogFile defaults to /tmp/zabbix_agent2.log.
- StatusPort: serves http://localhost:<port>/status.

Include accepts files or a wildcard directory. Include order is not defined, so never set the same parameter in two included files, and watch for editor backup files such as .BAK being picked up.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (appendix/config/zabbix_agent2): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
