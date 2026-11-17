---
id: computing-software.systems-network-administration.apache-tomcat.automatic-deployment-rules
name: automatic-deployment-rules
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, automatic-deployment, autodeploy, deployignore, hot-deploy, war-deployment, redeploy, reload, appbase]
level: practitioner
status: docs-checked
description: "How Tomcat 10.1 Host auto-deploys apps: precedence of context XML, WAR and directory, same-basename rule, redeploy vs reload, docBase placement and deployIgnore."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/host.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automatic application deployment

With `deployOnStartup` and/or `autoDeploy` true, the Host scans `appBase` and `xmlBase`.

Precedence (each app is identified once):
1. Apps with a context XML file in `xmlBase`.
2. Apps with a WAR in `appBase` not found in step 1.
3. Apps with a directory in `appBase` not found in 1 or 2.

Rules:
- Context XML, WAR and directory for one app must share the same base name and follow the context naming convention (see `computing-software.systems-network-administration.apache-tomcat.context-naming-and-versions`).
- With `autoDeploy`, deployed apps are monitored and, depending on what changes, are redeployed or reloaded. Redeploy creates a new web application, so with the standard session manager sessions are not retained; reload reuses the app, re-parses web.xml and reloads classes, and with the standard session manager sessions are persisted. `deployOnStartup` runs the same code but treats all files as new.
- An XML context's `docBase` should be outside `appBase`, otherwise the app may deploy twice or fail.
- If contexts are defined in `server.xml`, disable automatic deployment or set `deployIgnore` on the Host to avoid double deployment.
- `deployIgnore` is a regex relative to `appBase`, anchored to the entire file or directory name: `foo` matches only `foo`, not `foo.war`, `foobar` or `myfooapp`; use `.*foo.*` for anything containing foo.
- `undeployOldVersions="true"` removes superseded parallel-deployment versions during auto deployment.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Host reference (Automatic Application Deployment, deployIgnore, undeployOldVersions). Rewrote the redeploy/reload triggers and the deployIgnore example to match the page. Removed the production-habit advice and the generic verify line.

Method: documentation only; no commands were run.
