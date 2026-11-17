---
id: computing-software.messaging-and-integration.apache-activemq-artemis.proxy-protocol
name: proxy-protocol
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,proxy-protocol,proxyprotocolenabled,haproxy,client-ip,acceptor,activemq-artemis]
level: practitioner
status: docs-checked
description: "Show real client IPs behind HAProxy or nginx by enabling proxyProtocolEnabled on an acceptor; versions 1 and 2 are supported."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/proxy-protocol.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PROXY protocol support

**Goal:** have the broker see the real client address when connections arrive through a reverse proxy (HAProxy, nginx) that speaks the PROXY protocol, rather than seeing the proxy's address.

Both PROXY protocol versions 1 and 2 are supported, with any messaging protocol, with or without TLS.

## Configure (per acceptor)
```xml
<acceptor name="proxy-artemis">tcp://0.0.0.0:61616?proxyProtocolEnabled=true</acceptor>
```

## Security rule
Support must be explicit. An acceptor with `proxyProtocolEnabled=true` accepts only PROXY-protocol connections, and one without it accepts only non-PROXY connections; the broker does not guess. A violation logs a warning with code `AMQ224151`. The PROXY specification says the receiver should ensure only trusted proxies can use the protocol, otherwise untrusted parties could spoof addresses, so keep such an acceptor reachable only from the proxy.

## Management
Proxied connections carry two extra fields: `proxyAddress` (address and port of the proxy) and `proxyProtocolVersion` (`V1` or `V2`). They appear in `listConnections` on `ActiveMQServerControl` and in the web console Connections tab.

## Checked

Method: docs-checked 2026-11-09 against proxy-protocol.adoc (read in full). Removed the Verify step.
