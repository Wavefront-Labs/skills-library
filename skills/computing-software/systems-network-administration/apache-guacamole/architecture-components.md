---
id: computing-software.systems-network-administration.apache-guacamole.architecture-components
name: architecture-components
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, architecture, guacd, web-application, client-plugins, libguac, guacamole-protocol, clientless-remote-desktop]
level: intro
status: docs-checked
description: "How Guacamole's browser client, Java web app, guacd, protocol plugins and libguac fit together, and the browser-to-desktop request flow."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-architecture.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guacamole architecture and components

Goal: know which piece does what before debugging or sizing a deployment.

| Piece | Role |
|---|---|
| Client (browser) | JavaScript served by the web app; talks Guacamole protocol over HTTP/WebSocket |
| Web application | Server side written in Java. Provides the web interface and authentication layer and forwards protocol traffic to guacd. Knows nothing about RDP/VNC itself |
| guacd | Daemon ("heart of Guacamole"). Listens for TCP connections from the web app, loads a client plugin per connection, passes it the arguments |
| Client plugins | Dynamically loaded modules (for example RDP, VNC) translating the remote protocol to the Guacamole protocol; once loaded a plugin runs independently of guacd |
| libguac | Shared C library used by guacd and every plugin |
| Guacamole protocol | Text protocol for display rendering and event transport |

Request flow:
1. Browser loads the JS client from the web app.
2. Client connects back to the server over HTTP using the Guacamole protocol (an HTTP tunnel is used if WebSocket cannot be used).
3. Web app authenticates the user and forwards protocol data to guacd over TCP.
4. guacd loads the matching plugin, which connects to the target desktop.
5. The plugin streams display and input both ways.

Implications: guacd connects to the remote desktop servers on behalf of the user, so it must reach the targets; the browser talks only to the web server.

Verify: you can name the host and port where each of the three processes runs.

## Checked

2026-11-08. Read the whole of the Implementation and architecture page (guacamole-architecture.html) and confirmed the roles of client, web application, guacd, client plugins, libguac and the Guacamole protocol, and the HTTP tunnel fallback when WebSocket cannot be used. Removed the Tomcat remark, the plugin list beyond the RDP and VNC examples, the claim that buffering proxies break the tunnel, and the different-hosts remark (none on the page).
Method: documentation only; no commands were run.
