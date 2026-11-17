---
id: computing-software.messaging-and-integration.mosquitto.dynsec-groups-and-anonymous
name: dynsec-groups-and-anonymous
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [creategroup, addgroupclient, setanonymousgroup, anonymous-access]
level: practitioner
status: docs-checked
description: "Manage Dynamic Security groups and route unauthenticated devices to a restricted group with setAnonymousGroup."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share roles across clients and control anonymous access.

Group commands:

```
mosquitto_ctrl <options> dynsec createGroup <groupname>
mosquitto_ctrl <options> dynsec deleteGroup <groupname>
mosquitto_ctrl <options> dynsec addGroupClient <groupname> <username> <priority>
mosquitto_ctrl <options> dynsec removeGroupClient <groupname> <username>
mosquitto_ctrl <options> dynsec addGroupRole <groupname> <rolename> <priority>
mosquitto_ctrl <options> dynsec removeGroupRole <groupname> <rolename>
mosquitto_ctrl <options> dynsec getGroup <groupname>
mosquitto_ctrl <options> dynsec listGroups
```

The priority in `addGroupClient` is the priority of the group within the client's list of groups; in `addGroupRole` it is the role's priority within the group. `modifyGroup` exists in the topic API but not in mosquitto_ctrl.

Anonymous access: the documentation otherwise assumes no unauthenticated access. To allow clients that connect without a username while still using the plugin, an automatic anonymous group applies:

```
mosquitto_ctrl <options> dynsec setAnonymousGroup <groupname>
mosquitto_ctrl <options> dynsec getAnonymousGroup
```

Anything connecting without a username is assigned to that group, so roles on the group control what anonymous devices can reach. Default 2.1 configs create a group named `unauthenticated` for this purpose.

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Group commands, group-client priority, the anonymous group commands and the 2.1 unauthenticated group match. The role priority meaning in addGroupRole is inferred from the page's priority description rather than stated for that command.

Method: documentation only; no commands were run.
