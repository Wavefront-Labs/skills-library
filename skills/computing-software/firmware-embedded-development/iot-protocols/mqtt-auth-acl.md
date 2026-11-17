---
id: computing-software.firmware-embedded-development.iot-protocols.mqtt-auth-acl
name: mqtt-auth-acl
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mqtt-auth-acl, mqtt-security, mqtt, acl, password-file, authorization, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT authentication and ACL: Restrict who can publish or subscribe where."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
  - https://mosquitto.org/man/mosquitto_passwd-1.html
  - https://docs.emqx.com/en/emqx/latest/access-control/authn/authn.html
  - https://docs.emqx.com/en/emqx/latest/access-control/authz/authz.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT authentication and ACL

**Goal:** Restrict who can publish or subscribe where.

## Steps
1. Mosquitto: allow_anonymous defaults to false when listeners are defined; set it explicitly to false and point password_file at a file made with mosquitto_passwd
2. Create users with `mosquitto_passwd -c file user` (-c overwrites an existing file; leave it out to add users)
3. acl_file lines: `user alice` then `topic readwrite dev/alice/#`; access is read, write, readwrite or deny, and ACLs are keyed by username, not client id
4. Pattern rules: `pattern readwrite dev/%c/#` substitutes the client id, `%u` the username; the substitution must be the only text at its topic level, and pattern ACLs apply to all users
5. The manual suggests the mosquitto_password_file and mosquitto_acl_file plugins over these options
6. EMQX authenticators include built-in database, MySQL, PostgreSQL, MongoDB, Redis, HTTP and JWT; its authorization uses a chain of authorizers tried in order

## Gotcha
A wildcard ACL that is too broad lets one compromised device read the whole fleet; always scope by device id with %c or %u.

## Verify
- [ ] Device A cannot read device B topics
- [ ] Anonymous connect refused
- [ ] SIGHUP reloads password and ACL files without dropping connected clients' sessions (the manual says connected clients are not affected by the password reload)

## Checked

2026-11-03. Confirmed in the mosquitto.conf(5) and mosquitto_passwd(1) man pages and the EMQX authentication and authorization pages: allow_anonymous default, mosquitto_passwd -c, acl_file syntax, pattern substitution with %c and %u, reload on signal, plugin recommendation, EMQX authenticator types and authorization chain. Removed: HiveMQ authenticator claims (HiveMQ authentication pages were not reachable).
Method: documentation only; no commands were run.
