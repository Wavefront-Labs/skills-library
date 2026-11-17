---
id: computing-software.systems-network-administration.apache-guacamole.docker-guacamole-webapp
name: docker-guacamole-webapp
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, docker, guacamole-image, environment-variables, guacd-hostname, webapp-context, remote-ip-valve, guacamole-home, container-configuration]
level: practitioner
status: docs-checked
description: "Run the guacamole/guacamole image: GUACD_HOSTNAME/PORT, WEBAPP_CONTEXT, property-to-environment mapping, REMOTE_IP_VALVE_ENABLED proxy variables and custom GUACAMOLE_HOME."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-docker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# guacamole/guacamole container

```
docker run --network=some-network --name some-guacamole \
  -e GUACD_HOSTNAME=some-guacd -d -p 8080:8080 guacamole/guacamole
```
(Tomcat 9 with WebSocket.) `GUACD_HOSTNAME` is the guacd container's name; `GUACD_PORT` defaults to 4822.

Rules:
- At least one auth mechanism (MySQL, PostgreSQL or LDAP) must be configured or the image will not start.
- Database schema is not auto-created; generate it with `initdb.sh` (see apache-guacamole.mysql-auth-setup).
- `WEBAPP_CONTEXT` sets the URL path; default `/guacamole/`; `ROOT` serves at `http://HOSTNAME:8080`.
- Any `guacamole.properties` property is available as an env var: uppercase, dashes to underscores (`guacd-hostname` becomes `GUACD_HOSTNAME`), including third-party extension properties.

Reverse proxy (Tomcat RemoteIpValve), all ignored unless `REMOTE_IP_VALVE_ENABLED=true`:
- `PROXY_ALLOWED_IPS_REGEX` (default: private addresses)
- `PROXY_BY_HEADER` (`X-Forwarded-By`), `PROXY_IP_HEADER` (`X-Forwarded-For`), `PROXY_PROTOCOL_HEADER` (`X-Forwarded-Proto`)

`GUACAMOLE_HOME` defaults to `/etc/guacamole`; point it at your own directory for custom config and extensions (read-only is fine).

Verify: `http://HOSTNAME:8080/guacamole/` shows the login; otherwise `docker logs some-guacamole`.

## Checked

2026-11-04. Confirmed against the Guacamole manual page guacamole-docker: Tomcat 9.x image, GUACD_HOSTNAME/GUACD_PORT (4822), WEBAPP_CONTEXT and ROOT, property-to-environment naming, at least one auth mechanism required, tables not auto-created, REMOTE_IP_VALVE_ENABLED and the PROXY_* variables with their default headers, GUACAMOLE_HOME default /etc/guacamole and no write access needed. Nothing removed.

Method: documentation only; no commands were run.
