---
id: computing-software.systems-network-administration.apache-tomcat.manager-text-interface-deploy
name: manager-text-interface-deploy
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, manager, text-interface, deploy, undeploy, war-deployment, curl, parallel-deployment, remote-deploy]
level: practitioner
status: docs-checked
description: "Deploy, undeploy, reload, start and stop Tomcat 10.1 apps via the Manager text interface with curl: PUT uploads, local war= deploys, update, version and list output."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/manager-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manager text interface: deploy and lifecycle

Base: `http://host:port/manager/text/{command}?{params}`; needs the `manager-script` role. Replies are `text/plain` starting `OK` or `FAIL`. Common params: `path` (`/` for ROOT), `version` (parallel deployment), `war`.

```bash
curl -u deployer:<pw> "http://localhost:8080/manager/text/list"
# upload a WAR (PUT body); add update=true to replace
curl -u deployer:<pw> -T foo.war "http://localhost:8080/manager/text/deploy?path=/foo&update=true"
# deploy from the server's filesystem
curl -u deployer:<pw> "http://localhost:8080/manager/text/deploy?path=/foo&war=file:/path/to/foo.war"
curl -u deployer:<pw> "http://localhost:8080/manager/text/undeploy?path=/foo"
curl -u deployer:<pw> "http://localhost:8080/manager/text/stop?path=/foo"
curl -u deployer:<pw> "http://localhost:8080/manager/text/start?path=/foo"
curl -u deployer:<pw> "http://localhost:8080/manager/text/reload?path=/foo"
```

Facts:
- `list` shows `path:status:sessions:name`.
- Local deploy forms: `war=file:/path/foo` (directory), `war=file:/path/bar.war`, `war=bar.war` (in appBase), `config=file:/path/context.xml`; extra params `update`, `tag`.
- `undeploy` shuts the app down and removes it, deleting its WAR, its directory in appBase and its XML Context definition under `$CATALINA_BASE/conf/[enginename]/[hostname]/`; use `stop` to only take an app out of service.
- `reload` is not supported for apps deployed directly from a WAR file, only from an unpacked directory; undeploy and deploy, or deploy with `update`, instead.
- `stop` leaves the app deployed but returns 404.
- The `deploy` PUT form installs the uploaded WAR into the Host appBase; `update=true` undeploys an existing app on that path first (default false).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Manager how-to (Supported Manager Commands: common parameters, deploy forms, list, reload, stop, undeploy). Expanded the undeploy and reload notes to match the page; removed the generic verify line.

Method: documentation only; no commands were run.
