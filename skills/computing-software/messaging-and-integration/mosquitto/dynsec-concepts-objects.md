---
id: computing-software.messaging-and-integration.mosquitto.dynsec-concepts-objects
name: dynsec-concepts-objects
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [dynamic-security, clients, groups, roles]
level: practitioner
status: docs-checked
description: "Understand the Dynamic Security plugin objects (clients, groups, roles), their attributes and the $CONTROL topic API."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: learn the model before configuring role based access.

The Dynamic Security plugin provides role based authentication and access control that can be updated while the broker runs, through a topic based API at `$CONTROL/dynamic-security/v1`. It is supported since Mosquitto 2.0 and is available in all installations but not activated by default.

Clients (devices or users that connect) have:
- Username: unique across the plugin and the primary key; duplicates error.
- Password: may be unset at creation, in which case devices cannot connect as that client.
- Client ID: optional. If empty, any client id may use the username; if set, username, password and client id must all match.
- Groups and roles (any number of each), optional text name and description, and a disabled flag. Disabling disconnects connected devices and blocks reconnection.

Groups hold multiple clients and can be assigned roles; attributes are group name, roles, text name and description.

Roles contain multiple ACLs and attach to clients and/or groups; the role name is the key.

Control is through the topic API, but mosquitto_ctrl implements the API, as does the separate open source Management Center for Mosquitto (not part of the Mosquitto project).

The `modifyClient`, `modifyGroup` and `modifyRole` commands exist in the topic API but are not currently available in mosquitto_ctrl.

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Client, group and role attributes, topic API path, 2.0 support, mosquitto_ctrl and Management Center notes, and the modify* gaps all match. Claims unchanged.

Method: documentation only; no commands were run.
