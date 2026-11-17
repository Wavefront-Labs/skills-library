---
id: computing-software.messaging-and-integration.mosquitto.dynsec-default-acl-access
name: dynsec-default-acl-access
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [default-acl-access, setdefaultaclaccess, publishclientsend, subscribe]
level: practitioner
status: docs-checked
description: "Read and change the default allow/deny behaviour for publish, receive, subscribe and unsubscribe events in Dynamic Security."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set what happens when no ACL matches.

ACL checks occur on four events: `publishClientSend` (device publishes to the broker), `publishClientReceive` (device is due to receive a PUBLISH), `subscribe` and `unsubscribe`. If no matching ACL is found, the default behaviour applies. After first configuration:

- publishClientSend: deny
- publishClientReceive: allow
- subscribe: deny
- unsubscribe: allow

Change them with mosquitto_ctrl:

```
mosquitto_ctrl <options> dynsec setDefaultACLAccess publishClientSend deny
mosquitto_ctrl <options> dynsec setDefaultACLAccess publishClientReceive deny
mosquitto_ctrl <options> dynsec setDefaultACLAccess subscribe deny
mosquitto_ctrl <options> dynsec setDefaultACLAccess unsubscribe deny
```

Inspect one with:
```
mosquitto_ctrl <options> dynsec getDefaultACLAccess unsubscribe
```

The page notes some overlap between publishClientReceive and subscribe: usually a subscribe ACL is enough, but combining both lets you allow a wildcard subscription like `topic/#` while denying receipt of a specific topic within it such as `topic/secret`.

The admin role created by `mosquitto_ctrl dynsec init` (2.0) includes publishClientReceive and unsubscribePattern entries that the page says are not needed with the default behaviours but are there in case the defaults are set to deny.

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Event defaults, setDefaultACLAccess and getDefaultACLAccess and the receive/subscribe overlap match. Rewrote the closing sentence, which wrongly said the admin role grants publishClientReceive and subscribePattern on # and $SYS/# in case defaults deny; the page says that only of the publishClientReceive and unsubscribePattern entries.

Method: documentation only; no commands were run.
