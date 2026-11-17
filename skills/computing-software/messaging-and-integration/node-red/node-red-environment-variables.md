---
id: computing-software.messaging-and-integration.node-red.node-red-environment-variables
name: node-red-environment-variables
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, environment-variables, env, typedinput, subflow-properties, systemd, secrets, config]
level: practitioner
status: docs-checked
description: "Use environment variables in Node-RED node properties, JSONata, Function nodes and subflows, and set them on flows, groups, subflows, the process and systemd."
sources: ["https://nodered.org/docs/user-guide/environment-variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment variables in Node-RED

Set a node property from an environment variable by making its whole value `${ENV_VAR}`. The runtime substitutes it when loading flows. It only works when it replaces the entire property: `CLIENT-${HOST}` is not possible. If a node's dialog has no text input for the property, hand-edit the flow file.

Other places to read them:
- TypedInput widget, type "environment variable": with no `${}` the whole value is the variable name (`FOO` reads `process.env.FOO`); with `${}` the variable is substituted into the text (`Hello ${FOO}`).
- JSONata (for example in a Change node): `$env('ENV_VAR')`.
- Function node: `env.get("FOO")`.
- Template node (since Node-RED 3.0): `{{env.COLOUR}}`.

Where they can be defined:
- Subflow instance properties (since 0.20) appear as environment variables inside the subflow, customised per instance.
- Flow or group level (since 2.1), in the edit dialog of the flow or group.
- Global (since 3.1), in the editor's User Settings dialog.
- In a subflow Node-RED searches the subflow properties, then the flow containing the subflow (which may itself be a subflow). Prefix a name with `$parent.` to read the parent level's value instead of the local one.

Running as a service from the install script: the service does not see variables defined only in the calling process. Either add `process.env.FOO='World';` to the settings file outside `module.exports`, or put lines like `ENV_VAR='foobar'` in a file named `environment` in the Node-RED user directory (`~/.node-red`) for the systemd service.

Built-in variables (since 2.2): `NR_NODE_ID`, `NR_NODE_NAME`, `NR_NODE_PATH` (slash-delimited IDs of the flow, enclosing subflows and the node), `NR_GROUP_ID`, `NR_GROUP_NAME`, `NR_FLOW_ID`, `NR_FLOW_NAME`. Since 3.1 also `NR_SUBFLOW_ID`, `NR_SUBFLOW_NAME`, `NR_SUBFLOW_PATH`. IDs are unique but names are not; an unnamed node, flow or group, or a node outside any group, gives an empty string.

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Using environment variables. Removed: the precedence order claim (page gives only subflow-then-containing-flow), the Environment= unit-lines suggestion, the read-only wording and the closing credentials remark.

Method: documentation only; no commands were run.
