---
id: computing-software.systems-network-administration.apache-guacamole.login-restrictions
name: login-restrictions
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, auth-restrict, login-restrictions, connection-restrictions, time-windows, allowed-hosts, denied-hosts, cidr, access-control]
level: practitioner
status: docs-checked
description: "Limit when and from where Guacamole users log in or use connections with the restrict extension: time windows, host/CIDR, deny-wins rules."
sources:
  - https://guacamole.apache.org/doc/gug/auth-restrict.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Login and connection restrictions (guacamole-auth-restrict, 1.6.0)

It decorates another extension that can store extra data on users, groups, connections and balancing groups; only the JDBC database extensions qualify.

Install: `guacamole-auth-restrict-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `RESTRICT_ENABLED=true`.

New options appear in the admin UI for users, groups, connections and balancing groups:
- allowed/denied time windows (e.g. 9-5 daily; deny all Saturday and Sunday)
- allowed/denied hosts: hostnames, IPv4/IPv6, or CIDR (`192.168.123.0/24`)

Evaluation:
- No rules: allowed. Only allow rules: denied outside them. Only deny rules: allowed outside them.
- Deny beats allow (including an IP in a denied subnet).
- User rules beat group rules; all effective groups, including nested, are evaluated.
- Time is checked before host; both must pass. If both deny, the error names the time.
- Administrators bypass login restrictions (a warning is logged); connection restrictions apply to everyone.

Gotchas:
- Windows are entered in your local time but stored in UTC, so daylight saving shifts the effective local hours.
- Hostnames must resolve from the Guacamole server; an unresolvable name with no other match denies login.
- Behind a proxy all clients look like the proxy unless forwarding is set up (apache-guacamole.tomcat-remoteipvalve).

Verify: an account with a deny rule for your test IP is refused with the restriction message.

## Checked

2026-11-08. Read the whole of the restrictions page (auth-restrict.html) and confirmed the 1.6.0 jar name, GUACAMOLE_HOME/extensions, RESTRICT_ENABLED, the JDBC-only decorating requirement, the evaluation rules (implicit allow, allow-only, deny-only, deny precedence, user over group, nested groups, time before host, administrator exemption), UTC storage with the daylight saving shift, and hostname resolution failure denying login. Nothing removed.
Method: documentation only; no commands were run.
