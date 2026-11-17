---
id: computing-software.systems-network-administration.apache-tomcat.manager-app-roles-and-access
name: manager-app-roles-and-access
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, manager, manager-gui, manager-script, manager-jmx, manager-status, tomcat-users, remotecidrvalve, csrf, access-restriction]
level: practitioner
status: docs-checked
description: "Grant and restrict access to the Tomcat 10.1 Manager web app: the four manager roles, a tomcat-users.xml user, RemoteCIDRValve, new virtual hosts and the CSRF caution."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/manager-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manager app: roles and access

Roles (no user has them by default, so the Manager is off until you add one):

| Role | Gives |
|---|---|
| `manager-gui` | HTML interface `/manager/html` |
| `manager-status` | Server Status page only |
| `manager-script` | Text interface `/manager/text/...` plus Server Status |
| `manager-jmx` | `/manager/jmxproxy` plus Server Status |

Never give `manager-script` or `manager-jmx` to a user who also has `manager-gui`.

`conf/tomcat-users.xml`:
```xml
<user username="deployer" password="<STRONG_PASSWORD>" roles="manager-script"/>
```
Any BASIC-auth user with the role works; for hashed passwords see `computing-software.systems-network-administration.apache-tomcat.credential-handler-password-digest`.

Restrict by IP with a valve in the Manager's Context:
```xml
<Context privileged="true" antiResourceLocking="false"
         docBase="${catalina.home}/webapps/manager">
  <Valve className="org.apache.catalina.valves.RemoteCIDRValve"
         allow="127.0.0.0/8,::1/128"/>
</Context>
```
(`RemoteHostValve` can filter by host name.) For a new virtual host, install `manager.xml` in `$CATALINA_BASE/conf/[enginename]/[hostname]/`.

CSRF: the text and JMX interfaces cannot be CSRF-protected. If you log in with a browser using these roles, close all browser windows afterwards.

Verify: `curl -u deployer:<pw> http://localhost:8080/manager/text/list` returns `OK - Listed applications for virtual host localhost`.

## Checked

2026-11-04. Read the Tomcat 10.1 Manager App How-To (manager-howto.html): confirmed the four manager roles and what each grants, access disabled by default, the tomcat-users.xml user example, BASIC authentication, the RemoteCIDRValve and RemoteHostValve restriction, manager.xml for new hosts, and the CSRF caution. Removed the META-INF/context.xml location and the 403 claim, which the page does not state.

Method: documentation only; no commands were run.
