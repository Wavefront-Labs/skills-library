---
id: computing-software.systems-network-administration.apache-guacamole.run-guacd-service
name: run-guacd-service
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, guacd, systemd, sysv-init, start-guacd, daemon, native-installation]
level: intro
status: draft
description: "Start and enable the guacd daemon after a source install with systemd or SysV init, and what make install does not do."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-native.html
  - https://guacamole.apache.org/doc/gug/troubleshooting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Run guacd as a service

`make install` installs guacd but does not start it.

systemd (needs `--with-systemd-dir` at configure time):
```
systemctl start guacd
systemctl enable guacd    # start at boot
```
SysV init (needs `--with-init-dir`):
```
service guacd start
```
If you configured without either option no unit or init script is installed; start `guacd` yourself (add `-f` to stay in the foreground, see apache-guacamole.guacd-conf-options).

Notes:
- guacd and client plugins log to syslog, not to the Tomcat logs.
- Default listen port is 4822 and the web app expects `guacd-hostname: localhost`, `guacd-port: 4822` unless changed in `guacamole.properties`.
- After changing guacd settings restart guacd; after changing `guacamole.properties` restart Tomcat. They are independent.
- If you see `Unable to bind socket to any addresses` another service holds port 4822; stop it or start guacd with `-l PORT` and set `guacd-port` to match.

Verify: `systemctl status guacd` is active and syslog shows guacd listening on 4822.
