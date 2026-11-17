---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.port-binding
name: port-binding
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, twelve-factor, port-binding, self-contained-service, embedded-server, port-env-var, container-port]
level: intro
status: docs-checked
description: "Apply factor VII: make the app self-contained, exporting HTTP (or other protocols) by binding to a port from config, with no injected web server container at runtime."
sources: ["https://12factor.net/port-binding", "https://cloud.google.com/run/docs/container-contract#port"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor VII — Export services via port binding

**Rule:** the app embeds its server (Gunicorn/Uvicorn, Node `http`, embedded Tomcat/Jetty/Netty,
Kestrel) and listens on a port; it isn't deployed *into* an external app server.

## Steps
1. Read the port from env (`PORT`), defaulting to 8080 locally. Cloud Run injects the `PORT`
   environment variable (requests go to 8080 by default) and requires listening on `0.0.0.0`.
2. Bind `0.0.0.0` inside containers: Cloud Run states the ingress container must not listen on `127.0.0.1`.
3. Declare the port in the container spec (`containerPort` or the image's exposed port) and keep it equal to the port the app reads from config.
4. The routing layer (LB, ingress, platform router) maps public hostnames to the port.
5. Non-HTTP services do the same (the factor names XMPP and Redis), and one app can be the backing service of another by handing its URL to the consumer as config.

## Gotchas
- Prefer a high port such as 8080 and map it externally, so the container need not run as root.
- Legacy WAR deployments into shared Tomcat break this factor; package with embedded server
  (Spring Boot fat jar) during replatforming.

## Checked
2026-10-28. Confirmed against 12factor.net/port-binding (self-contained app, no injected webserver, routing layer, non-HTTP examples XMPP and Redis, app as backing service) and the Cloud Run container contract (`PORT` injected, listen on `0.0.0.0` not `127.0.0.1`, 8080 default). Removed: App Service `WEBSITES_PORT`, Heroku, the `EXPOSE` remark and the privileged-port rule (not in the sources).
Method: documentation only; no commands were run.

## Verify
- [ ] `PORT=9000 ./run` listens on 9000.
- [ ] Container runs as non-root on a high port.
