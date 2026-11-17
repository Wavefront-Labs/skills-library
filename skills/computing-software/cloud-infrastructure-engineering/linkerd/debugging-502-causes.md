---
id: computing-software.cloud-infrastructure-engineering.linkerd.debugging-502-causes
name: debugging-502-causes
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, troubleshooting, 502, connections, timeouts]
level: practitioner
status: docs-checked
description: "Diagnose HTTP 502 responses that appear after injection by checking server idle timeouts and half-closed connection handling."
sources:
  - https://linkerd.io/2.19/tasks/debugging-502s/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd turns connection errors into HTTP 502 responses, which can make previously hidden issues visible. It also reuses persistent connections and adds connection tracking, which can expose application or infrastructure problems such as misconfigured connection timeouts.

The proxy only sees its connection to the application refused or closed without explanation, so it cannot return a more informative error. If 502s began when you added Linkerd, suspect connection reuse or tracking.

Common causes:

- Connection idle timeouts. A server that closes connections idle for a set time, as the Go HTTP server can, fails requests that were already in flight when the close began. This is likely if you have traffic with a regular period, such as liveness checks, equal to the idle timeout. Raise the server's idle timeout so it does not close connections that are actively in use.
- Half-closed connection timeouts. When one side of a TCP connection is closed and the other is not, the operating system's connection tracker can lose track of connections that stay half-closed too long. Responses may then not be delivered, and new connections can hit port conflicts that show up as 502s. The docs link a script for detecting half-closed connections.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/debugging-502s/.

Removed or reworded: Closing advice not on the page.

Method: documentation only; no commands were run.
