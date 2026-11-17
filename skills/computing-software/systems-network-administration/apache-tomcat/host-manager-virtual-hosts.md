---
id: computing-software.systems-network-administration.apache-tomcat.host-manager-virtual-hosts
name: host-manager-virtual-hosts
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, host-manager, admin-script, admin-gui, virtual-host, storeconfiglifecyclelistener, persist, text-interface]
level: practitioner
status: docs-checked
description: "Add, stop, start, remove and persist Tomcat 10.1 virtual hosts at runtime with the Host Manager text interface and the admin-script role, including enabling persist."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/host-manager-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Host Manager

Roles: `admin-gui` (HTML) and `admin-script` (text interface at `/host-manager/text/{COMMAND}`).
```xml
<user username="hostadmin" password="<STRONG_PASSWORD>" roles="admin-script"/>
```

| Command | Parameters |
|---|---|
| `list` | none |
| `add` | `name` (required), `aliases`, `appBase`, `manager`, `autoDeploy`, `deployOnStartup`, `deployXML`, `copyXML` |
| `remove`, `start`, `stop`, `persist` | `name` (required) |

`manager=true` adds the Manager app to the new host (reachable at `/manager`). `autoDeploy`, `deployOnStartup`, `deployXML` and `copyXML` are booleans; `appBase` may be relative or absolute.

```bash
curl -u hostadmin:<pw> "http://localhost:8080/host-manager/text/add?name=www.example.com&aliases=example.com&appBase=/path/to/appDir&deployOnStartup=true"
curl -u hostadmin:<pw> "http://localhost:8080/host-manager/text/stop?name=www.example.com"
curl -u hostadmin:<pw> "http://localhost:8080/host-manager/text/persist?name=www.example.com"
```

- Changes may be persisted with `persist`, which writes the virtual host into `server.xml`.
- `persist` is disabled by default; to enable it, configure the listener in `server.xml`:
```xml
<Listener className="org.apache.catalina.storeconfig.StoreConfigLifecycleListener"/>
```
- The role is set up like the Manager's (`computing-software.systems-network-administration.apache-tomcat.manager-app-roles-and-access`).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Host Manager text-interface how-to: roles, commands, add parameters, persist and StoreConfigLifecycleListener. Reworded the runtime-only and parameter-mapping claims; removed the access-restriction advice and the generic verify line.

Method: documentation only; no commands were run.
