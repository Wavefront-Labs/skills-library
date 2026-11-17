---
id: computing-software.systems-network-administration.apache-guacamole.auth-ban-brute-force
name: auth-ban-brute-force
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, auth-ban, brute-force, ban-max-invalid-attempts, ban-address-duration, fail2ban, ip-ban, security]
level: practitioner
status: docs-checked
description: "Block Guacamole brute-force logins with the auth-ban extension: ban-max-invalid-attempts, ban-address-duration, ban-max-addresses, BAN_ENABLED in Docker, and the proxy-IP pitfall."
sources:
  - https://guacamole.apache.org/doc/gug/auth-ban.html
  - https://guacamole.apache.org/doc/gug/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brute-force protection (auth-ban)

The extension tracks failed logins per client IP and temporarily blocks an address once it reaches the threshold. All properties are optional.

| Property | Docker env | Default |
|---|---|---|
| `ban-max-invalid-attempts` | `BAN_MAX_INVALID_ATTEMPTS` | 5 |
| `ban-address-duration` | `BAN_ADDRESS_DURATION` | 300 s |
| `ban-max-addresses` | `BAN_MAX_ADDRESSES` | 10485670 |

When the table is full the least-recently-used address is dropped.

Docker: installed by default in `guacamole/guacamole`; set `BAN_ENABLED=false` to turn it off. Native: after changing properties restart Tomcat (not guacd). Restart disconnects all users.

Pitfall: it keys on the IP Guacamole sees. The manual says to make sure Guacamole receives the correct client addresses, particularly behind a reverse proxy. Fix the proxy first (see apache-guacamole.tomcat-remoteipvalve).

Alternative from the security page: fail2ban (third party), which blocks at the firewall instead of in the app. Brute-force protection is described as highly recommended.

Verify: five bad logins from a test host (the default threshold) are followed by blocked logins from that address for the ban duration.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages auth-ban and security: extension introduced in 1.6.0, per-IP tracking, the three properties with their Docker variables and defaults (5, 300 seconds, 10485670 with LRU discard), enabled by default in the Docker image with BAN_ENABLED=false to disable, restart of the web application, the reverse-proxy client-IP warning, and fail2ban as a firewall-level alternative. Removed: the unsupported claim about what happens to bans behind a proxy without forwarding.

Method: documentation only; no commands were run.
