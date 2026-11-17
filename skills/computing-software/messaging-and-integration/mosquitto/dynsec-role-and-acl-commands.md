---
id: computing-software.messaging-and-integration.mosquitto.dynsec-role-and-acl-commands
name: dynsec-role-and-acl-commands
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [createrole, addroleacl, removeroleacl, getrole]
level: practitioner
status: docs-checked
description: "Build Dynamic Security roles with createRole, addRoleACL and removeRoleACL using topic filter, allow or deny, and priority."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define what a role may do.

Commands:

```
mosquitto_ctrl <options> dynsec createRole <rolename>
mosquitto_ctrl <options> dynsec deleteRole <rolename>
mosquitto_ctrl <options> dynsec addRoleACL <rolename> <acltype> <topic filter> allow|deny <priority>
mosquitto_ctrl <options> dynsec removeRoleACL <rolename> <acltype> <topic filter>
mosquitto_ctrl <options> dynsec getRole <rolename>
mosquitto_ctrl <options> dynsec listRoles
```

`acltype` is one of publishClientSend, publishClientReceive, subscribeLiteral, subscribePattern, unsubscribeLiteral and unsubscribePattern.

Example from the page:

```
mosquitto_ctrl <options> dynsec addRoleACL <rolename> publishClientSend client/topic allow 5
mosquitto_ctrl <options> dynsec removeRoleACL <rolename> publishClientSend client/topic
```

The topic filter is the key for removal, together with the ACL type.

Roles have a name (the key), an optional text name and optional text description. The role is then attached with `addClientRole` or `addGroupRole`. `getRole` shows the ACL order used when priorities tie. `modifyRole` exists in the topic API but not in mosquitto_ctrl.

A typical bundle, created by the 2.1 default config, includes `client` (read/write on `#`) and `topic-observe` (read-only on `#`).

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Role commands, ACL type list, the example, removal key, getRole ordering, modifyRole gap and the 2.1 default roles match. Claims unchanged.

Method: documentation only; no commands were run.
