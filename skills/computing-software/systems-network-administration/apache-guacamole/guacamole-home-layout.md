---
id: computing-software.systems-network-administration.apache-guacamole.guacamole-home-layout
name: guacamole-home-layout
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, guacamole-home, guacamole-properties, extensions-directory, lib-directory, logback-xml, configuration-location]
level: intro
status: draft
description: "Where Guacamole reads configuration: GUACAMOLE_HOME default /etc/guacamole, three ways to relocate it, and the roles of guacamole.properties, extensions, lib and logback.xml."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GUACAMOLE_HOME

Default: `/etc/guacamole`. Override with any one of:
1. A `.guacamole` directory in the home of the user running the servlet container (used automatically if present).
2. The `GUACAMOLE_HOME` environment variable (full path).
3. The `guacamole.home` Java system property (full path).
The manual does not state precedence; use only one.

Contents:
| Path | Purpose |
|---|---|
| `guacamole.properties` | main config (guacd location, extension settings) |
| `logback.xml` | optional logging config (see apache-guacamole.guacamole-properties-reference) |
| `extensions/` | extension `.jar` files, loaded at startup |
| `lib/` | libraries extensions need, e.g. JDBC drivers |

Other files that live here: `user-mapping.xml`, `ssh_known_hosts`, `ldap-servers.yml`, `ksm-token-mapping.yml`, `guacamole.properties.ksm`, `radius.key`/`ca.crt`, `guacd.conf` (default location of guacd's own config).

Config and extensions are read only at Tomcat startup: restart Tomcat after changes. Restarting disconnects every user; guacd needs no restart. Check Tomcat logs if it fails to come back.

Docker: `GUACAMOLE_HOME` defaults to `/etc/guacamole`; mount a custom directory and set the variable (see apache-guacamole.docker-guacamole-webapp).

Verify: Tomcat's log at startup lists each extension loaded from `extensions/`.
