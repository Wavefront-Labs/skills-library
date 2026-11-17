---
id: computing-software.firmware-embedded-development.iot-protocols.node-red-flows
name: node-red-flows
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [node-red-flows, iot-gateway, node-red, flow, mqtt-in, function-node, iot-protocols]
level: practitioner
status: docs-checked
description: "Node-RED IoT flows: Prototype and run gateway logic in Node-RED."
sources:
  - https://nodered.org/docs/user-guide/runtime/securing-node-red
  - https://nodered.org/docs/user-guide/runtime/configuration
  - https://nodered.org/docs/user-guide/context
  - https://nodered.org/docs/user-guide/projects/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node-RED IoT flows

**Goal:** Prototype and run gateway logic in Node-RED.

## Steps
1. Parse payload strings with the JSON node, transform in a function node, route with the Switch node (rules evaluated per message)
2. Flows are stored in the file named by the flowFile setting (default flows_<hostname>.json under userDir, default $HOME/.node-red); back that file up
3. Context shares state outside messages at node, flow or global scope; it is memory-only by default and lost on restart
4. To keep context across restarts set contextStorage in settings.js, for example default module localfilesystem (files under ~/.node-red/context/, flushed about every 30 s)
5. Secure the editor and admin API with the adminAuth setting in settings.js (username/password or OAuth/OpenID); the default is no security
6. uiHost sets the interface the editor listens on (default 0.0.0.0, all IPv4 interfaces); uiPort defaults to 1880
7. Use the https setting (key and cert) to serve the editor over HTTPS
8. If the Projects feature is used, encrypt the credentials file with a key that is not stored in the project

## Gotcha
By default anyone who can reach the Node-RED editor's IP address can open it and deploy changes; only run that way on a trusted network. Enable adminAuth and restrict uiHost.

## Verify
- [ ] Message flows end to end
- [ ] Editor requires login
- [ ] Flow backup in version control

## Checked
Confirmed 2026-11-08 against nodered.org user guide pages "Securing Node-RED" (first 62 lines read, adminAuth and default-insecure statements), "Configuration" (read in full to the dashboard section: flowFile, userDir, uiHost, uiPort, https, adminAuth, functionGlobalContext), "Working with context" (read in full) and "Projects" (credentials encryption note, search only). Removed as unconfirmed on these pages: mqtt in/out nodes with TLS broker config, the delay/rate-limit node, credentialSecret, and the claim that the flow file is named flows.json by default (the page gives flows_<hostname>.json).
Method: documentation only; no commands were run.
