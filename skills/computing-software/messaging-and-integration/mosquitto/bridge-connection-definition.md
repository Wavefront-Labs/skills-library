---
id: computing-software.messaging-and-integration.mosquitto.bridge-connection-definition
name: bridge-connection-definition
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [bridge, connection, address, round-robin]
level: practitioner
status: docs-checked
description: "Define a Mosquitto bridge with connection, address and credentials, and choose failover with round_robin."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect this broker to another one.

A bridge starts with `connection name`, which names the bridge and marks the start of its settings.

```
connection test-mosquitto-org
address test.mosquitto.org
remote_username user1
remote_password PASSWORD
topic clients/total in 0 test/mosquitto/org/ $SYS/broker/
```

- `address address[:port] [address[:port]]` (or `addresses`) is required for each bridge. The default port is 1883; with an IPv6 address the port is not optional.
- `remote_username` and `remote_password` authenticate to a broker requiring them; the password option is only valid if a username is also supplied. The older `username` and `password` names remain valid.
- `remote_clientid` defaults to `name.hostname`, and `local_clientid` defaults to `local.<remote_clientid>`; when bridging a broker to itself they must differ.
- `local_username` and `local_password` are used when connecting the bridge to the local broker, important when authentication and ACLs are in use.

With several addresses, `round_robin false` (default) treats the first as the main connection and tries the others in turn, retrying the main one periodically. `round_robin true` treats all as equals and stays on whichever connected until it fails.

Bridge settings are reloaded on the reload signal.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Claims unchanged; all match the page.
