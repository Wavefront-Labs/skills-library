---
id: computing-software.systems-network-administration.apache-guacamole.security-hardening-overview
name: security-hardening-overview
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, security, hardening, ssl-termination, tls, brute-force, fail2ban, guacd-exposure, securing-guacamole]
level: intro
status: draft
description: "The Guacamole manual's baseline for securing an install: TLS terminated at a reverse proxy, brute-force protection, and keeping guacd unexposed."
sources:
  - https://guacamole.apache.org/doc/gug/security.html
  - https://guacamole.apache.org/doc/gug/guacamole-docker.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Securing a Guacamole install

The security page makes two recommendations; related pages add more.

1. Encrypt all user-to-Guacamole traffic with TLS. Terminate it at a reverse proxy (Apache httpd or Nginx) instead of configuring SSL in Tomcat. See apache-guacamole.nginx-reverse-proxy and apache-guacamole.apache-httpd-reverse-proxy.
2. Deploy brute-force protection ("highly recommended"): the auth-ban extension (enabled by default in the Docker image; see apache-guacamole.auth-ban-brute-force) or fail2ban at the firewall.

Further steps documented elsewhere in the manual:
- guacd does no authentication. Keep it on a private network or bound to localhost; if the web app is remote, enable TLS (`guacd-ssl`, see apache-guacamole.guacd-conf-options).
- Proxies must forward the real client IP so bans and restrictions work (apache-guacamole.tomcat-remoteipvalve).
- Change `guacadmin`/`guacadmin` at once after loading a database schema.
- Header-based SSO requires the proxy to strip the header from untrusted requests (apache-guacamole.header-auth).
- Add MFA (apache-guacamole.totp-mfa, apache-guacamole.duo-mfa) or SSO.
- Restrict quickconnect parameters such as drive redirection (apache-guacamole.quickconnect).

The page gives no firewall rules or other hardening steps.

Verify: the site loads only over HTTPS, port 4822 is unreachable from clients, and repeated bad logins get banned.
