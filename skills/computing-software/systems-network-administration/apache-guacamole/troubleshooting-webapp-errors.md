---
id: computing-software.systems-network-administration.apache-guacamole.troubleshooting-webapp-errors
name: troubleshooting-webapp-errors
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, troubleshooting, blank-display, proxy-buffering, tunnel-errors, tomcat-logs, catalina-out, user-mapping-errors, authentication-errors]
level: practitioner
status: draft
description: "Diagnose Guacamole web-app problems from servlet container logs: blank display behind proxies, Unicode connections, tunnel messages, auth errors and missing required properties."
sources:
  - https://guacamole.apache.org/doc/gug/troubleshooting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Troubleshooting: web app and tunnel

Logs: the web app writes to the servlet container log (Tomcat `catalina.out` or `localhost.log`); guacd goes to syslog (apache-guacamole.troubleshooting-guacd-errors).

Symptoms:
- **"Connecting, waiting for first update..." then disconnect / no graphics**: a buffering proxy, firewall, antivirus or virtualisation layer. Make it flush immediately (Nginx `proxy_buffering off`, Apache `flushpackets=on`) or use HTTPS, which proxies pass through untouched.
- **Unicode-named connections "do not exist"**: set `URIEncoding="UTF-8"` on all connectors.
- `Property PROPERTY is required`: a required property is missing for your provider or extension.
- user-mapping.xml errors: see apache-guacamole.user-mapping-xml.

Authentication:
- `Cannot connect - user not logged in`, `Requested configuration is not authorized`: session lost or no permission.
- `User has no session`: not logged in.

Tunnel:
- `No such tunnel` / `Tunnel is closed` / `Tunnel reached end of stream`: leftover client messages after disconnect; harmless unless constant.
- `No tunnel created`: usually authorisation failure.
- `No query string provided`: HTTP-tunnel bug.
- `End of stream during initial handshake`: guacd closed early; read syslog.
- `Element terminator of instruction was not ';' nor ','` / `Non-numeric character in element length`: corrupted transmission; a plugin, guacd or libguac bug.

Proxy configs: apache-guacamole.nginx-reverse-proxy, apache-guacamole.apache-httpd-reverse-proxy.

Verify: reproduce the action with the logs open in a second terminal and confirm the message disappears.
