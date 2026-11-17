---
id: computing-software.messaging-and-integration.mosquitto.dynsec-client-commands
name: dynsec-client-commands
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [createclient, setclientpassword, addclientrole, disableclient]
level: practitioner
status: docs-checked
description: "Create, secure, disable and delete Dynamic Security clients with mosquitto_ctrl dynsec commands."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage the users that connect to the broker.

All commands take connection options before `dynsec`:

```
mosquitto_ctrl -u admin -h localhost dynsec <command> ...
```

- `createClient <username>` creates a client without a client id; you are asked for the new client's password before the admin password, so read the prompts. `createClient <username> -i <client id>` adds a client id.
- `deleteClient <username>` and `disableClient <username>` both disconnect clients using those credentials.
- `enableClient <username>` lets credentials log in again.
- `setClientPassword <username>` prompts; `setClientPassword <username> <password>` takes it inline.
- `addClientRole <username> <rolename> <priority>` and `removeClientRole <username> <rolename>`.
- `getClient <username>` and `listClients` (prints one username per line).

If you omit `-P`, mosquitto_ctrl asks for the admin password when needed. The docs say providing it with `-P` is not recommended and that connections should be encrypted so new passwords are not sent in plain text.

Devices typically cannot update their own passwords; only a client with the correct access can.

`modifyClient` exists in the topic API but not in mosquitto_ctrl.

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Client commands, prompts, -P advice, encryption advice and the modifyClient gap match. Claims unchanged.

Method: documentation only; no commands were run.
