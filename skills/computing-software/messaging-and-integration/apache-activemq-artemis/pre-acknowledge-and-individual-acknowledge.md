---
id: computing-software.messaging-and-integration.apache-activemq-artemis.pre-acknowledge-and-individual-acknowledge
name: pre-acknowledge-and-individual-acknowledge
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,pre-acknowledge,preacknowledge,individual-acknowledge,acknowledge-modes,activemq-artemis,jms]
level: practitioner
status: docs-checked
description: "Use the two extra JMS acknowledge modes: PRE_ACKNOWLEDGE (ack before delivery, may lose messages) and INDIVIDUAL_ACKNOWLEDGE."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/pre-acknowledge.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extra acknowledge modes

Beyond JMS `AUTO_ACKNOWLEDGE`, `CLIENT_ACKNOWLEDGE` and `DUPS_OK_ACKNOWLEDGE`, Artemis supports `PRE_ACKNOWLEDGE` and `INDIVIDUAL_ACKNOWLEDGE`.

## PRE_ACKNOWLEDGE
The server acknowledges a message before delivering it to the client. This saves network traffic and CPU, but a crash after the server ack and before client delivery loses the message permanently. A suitable use is stock-price updates, where the next update supersedes a lost one. It also gives up transactional semantics for consumption, because messages are acknowledged on the server first rather than at commit.

Enable it with the boolean connection URL parameter `preAcknowledge=true`, or in the JMS API:
```java
Session session = connection.createSession(false, ActiveMQJMSConstants.PRE_ACKNOWLEDGE);
```

## INDIVIDUAL_ACKNOWLEDGE
Behaves like Client Acknowledge, except each message is acknowledged on its own. Use it when you do your own scheduling and do not know when each message's processing finishes. Prefer one consumer per worker thread where possible. Create the session with `ActiveMQJMSConstants.INDIVIDUAL_ACKNOWLEDGE`. It is not supported through MDBs or the inbound resource adapter, because an MDB must finish processing inside the bean.

## Checked

Method: docs-checked 2026-11-09 against pre-acknowledge.adoc (read in full). Removed the Verify step.
