---
id: computing-software.systems-network-administration.audiobookshelf.reverse-proxy-pfsense-haproxy
name: reverse-proxy-pfsense-haproxy
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [reverse-proxy, pfsense, haproxy, health-check, acl]
level: advanced
status: docs-checked
description: "Configure the pfSense HAProxy package for Audiobookshelf and fix the health check method that breaks forwarding."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/9.ha-pf-proxy-setup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pfSense HAProxy is configured graphically, with Health checking enabled.

Access Control Lists: Name `audiobookshelf`, Expression `Host starts with:`, Value `audiobookshelf.`.

Actions: Action `Use Backend`, Parameters `audiobookshelf`, Condition acl names `audiobookshelf`. The condition ACL name must match the ACL created above.

Backend: Name `audiobookshelf` (must match the action's Parameters), then add the server in the server list.

Health checking is on by default, and the check method `OPTIONS` is **not supported** by Audiobookshelf. If the health check fails, data will not be forwarded, so the site appears down. Fix it one of two ways:

- Set `Health check method` to `none` to disable checking.
- Set `Http check method` to `HEAD` or `GET` so the check works.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: pfSense + HAProxy page.

Method: documentation only; no commands were run.
