---
id: computing-software.systems-network-administration.apache-tomcat.ajp-connector-secure
name: ajp-connector-secure
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, ajp, ajp-connector, secret, secretrequired, allowedrequestattributespattern, packetsize, tomcatauthentication, mod-jk]
level: practitioner
status: docs-checked
description: "Configure the Tomcat 10.1 AJP/1.3 connector safely: loopback address, secret and secretRequired, allowedRequestAttributesPattern, packetSize, tomcatAuthentication."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/ajp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AJP connector (secure setup)

AJP exposes more of Tomcat's internals than HTTP, so lock it down.

| Attribute | Default | Notes |
|---|---|---|
| `protocol` | none (required) | `AJP/1.3`, or `org.apache.coyote.ajp.AjpNioProtocol` / `AjpNio2Protocol` |
| `address` | loopback | Keep it on loopback or a private interface |
| `secret` | null | ASCII; workers must send it whenever it is set |
| `secretRequired` | true | Only controls whether the connector starts without a secret; false only on a trusted network |
| `allowedRequestAttributesPattern` | null | Proxy-sent attributes not matching this regex get 403 |
| `packetSize` | 8192 | Max 65536; values below 8192 are ignored; match mod_jk `max_packet_size` |
| `tomcatAuthentication` | true | false: principal comes from the web server as `REMOTE_USER`, no roles |
| `tomcatAuthorization` | false | true: principal treated as authenticated, roles from the Realm |

Example (not from the page; port is the stock value):
```xml
<Connector protocol="AJP/1.3" address="127.0.0.1" port="8009"
           secret="<LONG_RANDOM_ASCII>" secretRequired="true"/>
```
Put the same secret in the web server's AJP worker configuration; check that product's docs for the directive name.

Large client certificate chains may need a bigger `packetSize` on both sides.

Verify: `netstat` shows the AJP port bound only to the chosen address, and a proxy worker without the matching secret is rejected.

For the wider hardening checklist see the cybersecurity `tomcat-hardening` skill.

## Checked

2026-11-04. Read the Tomcat 10.1 AJP Connector page (config/ajp.html): confirmed protocol values, address default loopback, secret and secretRequired semantics, allowedRequestAttributesPattern (403 on non-matching attributes), packetSize (default and minimum 8192, maximum 65536, mod_jk max_packet_size) and tomcatAuthentication/tomcatAuthorization. Removed the mod_jk and mod_proxy_ajp directive names and the log-entry claim, which the page does not state.

Method: documentation only; no commands were run.
