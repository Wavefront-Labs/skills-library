---
id: computing-software.messaging-and-integration.mosquitto.dynsec-priority-evaluation
name: dynsec-priority-evaluation
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [priority, acl-ordering, evaluation-order, roles]
level: sme
status: docs-checked
description: "Predict which Dynamic Security ACL wins by applying priorities for client roles, groups, group roles and ACLs."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand check order with multiple roles and groups.

Each client group, each client or group role, and each ACL within a role has a priority. The default is -1 and the maximum is 100000. Checks run from highest to lowest numerical value. Equal priorities within the same object type are checked lexicographically by username/groupname/rolename, but unique priorities per object type are advised. ACLs with identical priority are evaluated in the order shown by `getRole`.

On an event, the ACLs for that type are checked in order until one matches the topic; that first match decides.

Order: the client's own roles first (priority order), then each client group in priority order, with all that group's roles (priority order) checked before the next group.

Example from the page: client `sensor`, groups temperature (priority 2) and humidity (priority 1), role hallway. Group temperature has roles input (5) and output (1). The checking order is: hallway ACLs, then temperature/input, then temperature/output, then humidity/humidity. Within a role, higher priority first (`Z` priority 3 before `A` priority 1); in `input`, both are 3, so `A` then `Z` alphabetically.

The page advises using as simple a setup as possible.

Priority arguments: `addClientRole <username> <rolename> <priority>`, `addGroupClient <groupname> <username> <priority>`, `addGroupRole <groupname> <rolename> <priority>`, and the final argument of `addRoleACL`.

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Default -1 and maximum 100000 priorities, ordering rules, getRole tie-break and the sensor example match. Claims unchanged.

Method: documentation only; no commands were run.
