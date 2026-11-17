---
id: computing-software.systems-network-administration.apache-tomcat.remote-cidr-valve
name: remote-cidr-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, remotecidrvalve, remoteaddrvalve, ip-allow-list, allow, deny, denystatus, cidr, access-control]
level: practitioner
status: docs-checked
description: "Restrict Tomcat 10.1 access by client IP with RemoteCIDRValve: allow/deny CIDR lists, denyStatus, addConnectorPort, invalidAuthenticationWhenDeny; RemoteAddrValve is deprecated."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RemoteCIDRValve (IP allow/deny)

Class `org.apache.catalina.valves.RemoteCIDRValve`.

- `allow`: comma-separated IPv4/IPv6 addresses or CIDR blocks; if set the client must match.
- `deny`: same format; if set the client must not match.
- `denyStatus`: 403 by default.
- `addConnectorPort` (false): compare against `ADDRESS;PORT`, e.g. `10.0.0.0/8;8009`.
- `invalidAuthenticationWhenDeny`: send invalid auth so a downstream Basic authenticator challenges instead of 403; needs `preemptiveAuthentication="true"` on the Context.
- `usePeerAddress`: use the peer address rather than the forwarded one.

Syntax limits: use `192.168.1.0/24`; dotted-quad netmasks and shorthand like `10.10.` are not supported. No prefix means a single IP.

Typical use, lock the Manager app to localhost in `webapps/manager/META-INF/context.xml`:
```xml
<Valve className="org.apache.catalina.valves.RemoteCIDRValve"
       allow="127.0.0.1, ::1"/>
```

`RemoteAddrValve` (regex `allow`/`deny`) is deprecated and removed in Tomcat 12; prefer CIDR.

Behind a proxy, place `computing-software.systems-network-administration.apache-tomcat.remote-ip-valve` first so the filter sees the client address.

Verify: request from an allowed host gets 200, from another gets 403.

## Checked

2026-11-04. Read the Remote CIDR Valve and Remote Address Valve sections of the Tomcat 10.1 Valve page (config/valve.html): confirmed allow and deny lists, denyStatus 403, addConnectorPort, invalidAuthenticationWhenDeny with preemptiveAuthentication, usePeerAddress, the CIDR syntax limits, the localhost example, and the RemoteAddrValve deprecation (removal in Tomcat 12). Nothing removed.

Method: documentation only; no commands were run.
