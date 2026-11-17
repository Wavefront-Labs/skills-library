---
id: computing-software.systems-network-administration.apache-tomcat.host-element-attributes
name: host-element-attributes
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, host, virtual-host, appbase, xmlbase, unpackwars, autodeploy, deployonstartup, copyxml, deployxml, host-alias]
level: practitioner
status: docs-checked
description: "Tomcat 10.1 Host element: appBase, xmlBase, autoDeploy, deployOnStartup, unpackWARs, copyXML, deployXML, workDir, startStopThreads, error report valve and Alias names."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/host.html
  - https://tomcat.apache.org/tomcat-10.1-doc/virtual-hosting-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Host element

| Attribute | Default | Notes |
|---|---|---|
| `name` | none | Lowercased; no wildcards; `defaultHost` on the Engine must match one Host |
| `appBase` | webapps | Relative = under `$CATALINA_BASE` |
| `xmlBase` | conf/<engine>/<host> | Where context descriptors live |
| `autoDeploy` | true | Periodic scan for new/changed apps |
| `deployOnStartup` | true | Deploy at start |
| `unpackWARs` | true | false runs WARs in place (slower) |
| `copyXML` | false | Copy `META-INF/context.xml` to `xmlBase`; needs `deployXML` |
| `deployXML` | true (false under a security manager) | false ignores the app's embedded context.xml |
| `createDirs` | true | Create appBase/xmlBase; failure is logged, not fatal |
| `undeployOldVersions` | false | Remove old parallel-deployed versions (needs autoDeploy) |
| `workDir` | under `$CATALINA_BASE/work` | Exposed as `jakarta.servlet.context.tempdir` |
| `failCtxIfServletStartFails` | false | Fail context if a load-on-startup servlet fails |
| `startStopThreads` | 1 | Parallel context start |
| `errorReportValveClass` | `org.apache.catalina.valves.ErrorReportValve` | Empty string disables error reports |

Aliases (wildcards allowed here, not in `name`; all names must resolve to this server):
```xml
<Host name="www.example.com" appBase="webapps-example">
  <Alias>example.com</Alias>
  <Alias>*.example.net</Alias>
</Host>
```

Directory structures under each host's `appBase` should not overlap, and a context's `docBase` should never be the same as a host's `appBase` (virtual hosting how-to).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Host reference (common and StandardHost attributes, Host Name Aliases) and the Virtual Hosting how-to. Removed the generic verify line.

Method: documentation only; no commands were run.
