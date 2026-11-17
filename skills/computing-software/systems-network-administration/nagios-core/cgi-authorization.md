---
id: computing-software.systems-network-administration.nagios-core.cgi-authorization
name: cgi-authorization
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, cgi-authorization, cgi-cfg, use-authentication, authorized-for-all-hosts, authorized-for-system-commands, htpasswd, default-user-name]
level: practitioner
status: docs-checked
description: "Configure Nagios Core CGI access: htpasswd users, use_authentication, default rights for authenticated contacts, and the authorized_for_* grants in cgi.cfg."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cgiauth.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configcgi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CGI authentication and authorization

- Add a web user: `htpasswd /usr/local/nagios/etc/htpasswd.users <username>`. Make the username equal an existing contact's short name.
- `use_authentication=1` in `cgi.cfg` (default 1; 0 turns off auth AND command access).

## Default rights
- **Authenticated contact:** status, config, history, notifications and commands for hosts/services they are a contact of (a host's contact also covers its services).
- **Other authenticated users:** nothing.
- **Everyone, by default denied:** system/process information, process commands, all configuration info (showlog, process info in extinfo, cmd restarts, hostgroup/contact/timeperiod/command definitions in config).

## Grants (comma-separated users, also `authorized_contactgroup_for_*`)
`authorized_for_system_information`, `authorized_for_system_commands`, `authorized_for_configuration_information`, `authorized_for_all_hosts`, `authorized_for_all_host_commands`, `authorized_for_all_services`, `authorized_for_all_service_commands`, plus read-only variants.

## Warning
`default_user_name` gives unauthenticated visitors that user's full rights; use only on a secure server where everyone is authenticated.

Other `cgi.cfg` keys: `lock_author_names` (default 1), `refresh_rate`, `escape_html_tags`, `default_statusmap_layout` (0-6).

## Checked

2026-11-04. Confirmed against the CGI authentication page (htpasswd command, use_authentication=1, default permission table, the four default-denied items, the seven authorized_for_* variables, default_user_name warning) and the CGI configuration page (use_authentication default 1, authorized_contactgroup_for_* and read-only variants, lock_author_names default 1, default_statusmap_layout 0 to 6, refresh_rate, escape_html_tags). Nothing removed.

Method: documentation only; no commands were run.
